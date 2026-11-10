"""Unit tests for the cross-lingual loop extension (offline: no API calls)."""

import json
from types import SimpleNamespace

import pytest

from evaloop.core.config import EvaluationConfig, PROMPT_SETS
from evaloop.evaluation.cycle import BatchEvaluationCycle
from evaloop.models.base import BaseLLM
from evaloop.models.vertex_ai import ERROR_PREFIX, VertexAILLM
from evaloop.tasks import CodeGenerationTask, CrossLingualSummarizationTask, TaskFactory
from evaloop.tasks.crosslingual_summarization import resolve_language

from conftest import ASSERT_LINE, MBPP_STYLE_PROMPT


# --------------------------------------------------------------------------- task
class TestCrossLingualSummarizationTask:
    def test_registered(self):
        task = TaskFactory().create_task({"type": "crosslingual_summarization", "language": "hi"})
        assert isinstance(task, CrossLingualSummarizationTask)
        assert task.produces_testable_code is False

    def test_language_codes_resolve(self):
        assert resolve_language("zh") == "Simplified Chinese"
        assert resolve_language("HI") == "Hindi"
        assert resolve_language("Klingon") == "Klingon"
        with pytest.raises(ValueError):
            resolve_language("  ")

    def test_prompt_names_language_and_embeds_code(self):
        task = CrossLingualSummarizationTask({
            "type": "crosslingual_summarization", "language": "zh",
            "prompt_template": PROMPT_SETS["data_package"]["crosslingual_summarization"],
        })
        prompt = task.create_prompt("def f(x): return x")
        assert "def f(x): return x" in prompt
        assert prompt.count("Simplified Chinese") == 2

    def test_prompt_differs_from_standard_only_by_language_clause(self):
        std = PROMPT_SETS["data_package"]["summarization"]
        xl = PROMPT_SETS["data_package"]["crosslingual_summarization"]
        assert std.replace("description:", "description, written entirely in {language}:") \
                  .replace("Return only the summary,", "Return only the summary in {language},") == xl

    def test_repo_prompt_uses_translated_prefix(self):
        task = CrossLingualSummarizationTask({
            "type": "crosslingual_summarization", "language": "zh",
            "prompt_template": PROMPT_SETS["repo"]["crosslingual_summarization"],
        })
        prompt = task.create_prompt("def f(x): return x")
        assert prompt.count("编写一个Python函数来") == 2 and "Simplified Chinese" in prompt
        std = PROMPT_SETS["repo"]["summarization"]
        assert std.replace("Use one sentence to", "Use one sentence written in {language} to") \
                  .replace("write a python function to", "{prefix}") == \
            PROMPT_SETS["repo"]["crosslingual_summarization"]

    def test_repo_prompt_rejects_language_without_prefix(self):
        task = CrossLingualSummarizationTask({
            "type": "crosslingual_summarization", "language": "Klingon",
            "prompt_template": PROMPT_SETS["repo"]["crosslingual_summarization"],
        })
        with pytest.raises(ValueError):
            task.create_prompt("x")

    def test_postprocess_retains_assert_line(self):
        task = CrossLingualSummarizationTask({"type": "crosslingual_summarization"})
        out = task.postprocess("找出两个列表的共同元素。", {"cycle_input": MBPP_STYLE_PROMPT})
        assert out == '"""\n找出两个列表的共同元素。\n' + ASSERT_LINE + '\n"""\n'
        # The wrapped summary is a valid cycle input: re-wrapping keeps the same assert line.
        again = task.postprocess("第二轮摘要", {"cycle_input": out})
        assert again.splitlines()[-2] == ASSERT_LINE


# ------------------------------------------------------------------------- config
class TestLoopConfig:
    def test_crosslingual_task_sequence(self, tmp_path):
        cfg = EvaluationConfig(model="vertex/google/gemini-2.5-flash-lite", output_dir=str(tmp_path),
                               loop="crosslingual", summary_language="hi", prompt_set="data_package")
        tasks = cfg.get_task_configs(cfg.get_loop_task_type())
        assert [t["type"] for t in tasks] == ["code_generation", "crosslingual_summarization"]
        assert tasks[1]["language"] == "hi"
        assert tasks[0]["prompt_template"] == PROMPT_SETS["data_package"]["generation"]

    def test_standard_loop_unchanged_by_default(self, tmp_path):
        cfg = EvaluationConfig(model="gpt-4", output_dir=str(tmp_path))
        tasks = cfg.get_task_configs()
        assert tasks[1]["type"] == "code_summarization"
        assert "write a python function to" in tasks[1]["prompt_template"]

    def test_invalid_loop_rejected(self, tmp_path):
        with pytest.raises(ValueError):
            EvaluationConfig(model="gpt-4", output_dir=str(tmp_path), loop="nope")

    def test_vertex_prefix_routes_to_vertex(self, tmp_path):
        cfg = EvaluationConfig(model="vertex/openai/gpt-oss-120b-maas", output_dir=str(tmp_path),
                               vertex_project="p", max_new_tokens=1024)
        mc = cfg.get_model_config()
        assert mc["type"] == "vertex"
        assert mc["model_id"] == "openai/gpt-oss-120b-maas"
        assert mc["max_tokens"] == 1024 and mc["project"] == "p"


# ------------------------------------------------------------------- vertex model
class _FakeCompletions:
    def __init__(self, script):
        self.script = list(script)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        item = self.script.pop(0) if self.script else "echo"
        if isinstance(item, Exception):
            raise item
        text = kwargs["messages"][-1]["content"] if item == "echo" else item
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=text), finish_reason="stop")],
            usage=SimpleNamespace(prompt_tokens=3, completion_tokens=5),
        )


def _vertex(script, tmp_path, **cfg):
    completions = _FakeCompletions(script)
    client = SimpleNamespace(chat=SimpleNamespace(completions=completions))
    model = VertexAILLM({"model_id": "google/x", "max_retries": 2,
                         "call_log_path": str(tmp_path / "calls.jsonl"), **cfg}, client=client)
    return model, completions


class _HTTPError(Exception):
    def __init__(self, status):
        super().__init__(f"status {status}")
        self.status_code = status


class TestVertexAILLM:
    def test_batch_preserves_order(self, tmp_path):
        model, _ = _vertex([], tmp_path, concurrency=4)
        prompts = [f"p{i}" for i in range(20)]
        assert model.batch_generate(prompts) == prompts

    def test_greedy_settings_sent(self, tmp_path):
        model, completions = _vertex(["ok"], tmp_path, max_tokens=1024)
        model.generate("hi")
        call = completions.calls[0]
        assert call["temperature"] == 0.0 and call["top_p"] == 1.0 and call["max_tokens"] == 1024

    def test_retries_rate_limit_then_succeeds(self, tmp_path, monkeypatch):
        monkeypatch.setattr("evaloop.models.vertex_ai.time.sleep", lambda s: None)
        model, completions = _vertex([_HTTPError(429), "fine"], tmp_path)
        assert model.generate("x") == "fine"
        log = [json.loads(line) for line in (tmp_path / "calls.jsonl").read_text().splitlines()]
        assert log[0]["error"].startswith("_HTTPError(429)") and log[1]["finish_reason"] == "stop"

    def test_empty_answer_not_retried(self, tmp_path):
        model, completions = _vertex([""], tmp_path)
        assert model.generate("x") == ""
        assert len(completions.calls) == 1

    def test_reasoning_effort_forwarded(self, tmp_path):
        model, completions = _vertex(["ok"], tmp_path, reasoning_effort="low")
        model.generate("x")
        assert completions.calls[0]["reasoning_effort"] == "low"

    def test_non_retryable_error_returns_marker(self, tmp_path, monkeypatch):
        monkeypatch.setattr("evaloop.models.vertex_ai.time.sleep", lambda s: None)
        model, completions = _vertex([_HTTPError(400)], tmp_path)
        assert model.generate("x").startswith(ERROR_PREFIX)
        assert len(completions.calls) == 1


# ------------------------------------------------------------------ loop runner
class _ScriptedBatchModel(BaseLLM):
    """Returns code for generation prompts and a Chinese summary for summary prompts."""

    def __init__(self):
        super().__init__({"name": "scripted"})
        self.prompts = []

    def generate(self, prompt, **kwargs):
        return self.batch_generate([prompt])[0]

    def batch_generate(self, prompts, **kwargs):
        self.prompts.extend(prompts)
        return ["```python\ndef similar_elements(a, b):\n    return tuple(set(a) & set(b))\n```"
                if p.startswith("Generate") else "返回两个元组的共同元素。" for p in prompts]


def test_two_cycles_carry_chinese_summary_and_assert(tmp_path):
    cfg = EvaluationConfig(model="scripted", output_dir=str(tmp_path), loop="crosslingual",
                           summary_language="zh", prompt_set="data_package")
    factory = TaskFactory()
    tasks = [factory.create_task(c) for c in cfg.get_task_configs(cfg.get_loop_task_type())]
    model = _ScriptedBatchModel()
    runner = BatchEvaluationCycle(model, tasks)

    out1 = runner.run_single_cycle([{"task_id": "Mbpp/2", "prompt": MBPP_STYLE_PROMPT},
                                    {"task_id": "Mbpp/3", "prompt": MBPP_STYLE_PROMPT}], 1)
    summary = out1["cycle_results"][0]["task_2_output"]
    assert "返回两个元组的共同元素。" in summary and summary.splitlines()[-2] == ASSERT_LINE

    out2 = runner.run_single_cycle([{"task_id": "Mbpp/2", "prompt": summary},
                                    {"task_id": "Mbpp/3", "prompt": summary}], 2)
    gen_prompt_cycle2 = [p for p in model.prompts if p.startswith("Generate")][-1]
    assert "返回两个元组的共同元素。" in gen_prompt_cycle2 and ASSERT_LINE in gen_prompt_cycle2
    assert out2["cycle_results"][1]["task_2_output"].splitlines()[-2] == ASSERT_LINE
    assert isinstance(tasks[0], CodeGenerationTask)
