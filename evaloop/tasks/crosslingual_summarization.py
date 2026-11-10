"""Cross-lingual summarization step for the code <-> natural-language loop.

The standard EvaLoop loop alternates code generation (English description ->
code) and code summarization (code -> English description). This task keeps
the loop shape but asks the model to write the summary in another natural
language, so every cycle after the first is driven by a non-English
description that the model wrote itself:

    cycle 1:  original MBPP+ prompt (English)  -> code_1 -> summary_1 (L)
    cycle k:  summary_{k-1} (L) + assert line  -> code_k -> summary_k (L)

Design decisions
----------------
* The model's own output is the only perturbation: no external translator
  is involved, the model both writes and reads the language-L description.
* The code-generation instruction itself stays in English, so the only
  variable that changes relative to the standard loop is the language of
  the carried description.
* Function-signature stability is handled exactly like the standard loop:
  the inherited ``postprocess`` wraps the summary as a docstring and
  re-attaches the cycle's final ``assert`` line. An assert line is code,
  not natural language, so it is language-neutral and needs no translation.
* The failure condition is unchanged (the generated code fails the EvalPlus
  base or plus tests). Whether the model actually wrote in language L is
  *measured* afterwards (see ``scripts/analyze_runs.py``), not enforced, so a
  non-compliant summary does not end the loop by itself.
"""

from typing import Any, Dict

from .code_summarization import CodeSummarizationTask
from .factory import register_task

#: Short codes accepted on the command line, mapped to the name used in prompts.
LANGUAGE_NAMES = {
    "zh": "Simplified Chinese",
    "hi": "Hindi",
    "es": "Spanish",
    "de": "German",
    "fr": "French",
    "ja": "Japanese",
    "ru": "Russian",
    "ar": "Arabic",
    "bn": "Bengali",
    "sw": "Swahili",
}

#: Translation of the fixed opening "write a python function to" that the repository's standard
#: one-sentence summary prompt forces. Part of the prompt *template* (a constant written by the
#: experimenter), not of the carried content, so it is not an external perturbation.
SUMMARY_PREFIXES = {
    "Simplified Chinese": "编写一个Python函数来",
    "Hindi": "एक पायथन फ़ंक्शन लिखें जो",
    "Spanish": "escribe una función de Python para",
    "German": "schreibe eine Python-Funktion, um",
    "French": "écris une fonction Python pour",
    "Japanese": "次のことを行うPython関数を書く：",
}

DEFAULT_CROSSLINGUAL_TEMPLATE = (
    "Summarize what the following code does in a detailed description, "
    "written entirely in {language}:\n\n"
    "```\n{code}\n```\n\n"
    "Return only the summary in {language}, without explanations or comments."
)


def resolve_language(language: str) -> str:
    """Map a language code (``zh``) or name (``Simplified Chinese``) to a prompt name."""
    if not language or not language.strip():
        raise ValueError("A summary language must be given for the cross-lingual loop")
    return LANGUAGE_NAMES.get(language.strip().lower(), language.strip())


@register_task("crosslingual_summarization")
class CrossLingualSummarizationTask(CodeSummarizationTask):
    """Summarize code in a configurable natural language (default: Simplified Chinese).

    Reuses ``CodeSummarizationTask.extract_output`` (whole response, stripped)
    and ``CodeSummarizationTask.postprocess`` (docstring wrapper + retained
    assert line) unchanged; only the prompt differs.
    """

    def __init__(self, task_config: Dict[str, Any]):
        super().__init__(task_config)
        self.language = resolve_language(task_config.get("language", "zh"))

    def create_prompt(self, input_text: str) -> str:
        template = self.task_config.get("prompt_template", DEFAULT_CROSSLINGUAL_TEMPLATE)
        if "{prefix}" in template and self.language not in SUMMARY_PREFIXES:
            raise ValueError(f"No translated summary prefix for '{self.language}'")
        return template.format(code=input_text, language=self.language,
                               prefix=SUMMARY_PREFIXES.get(self.language, ""))
