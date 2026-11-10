# Failed loops — google/gemini-3.5-flash — loop=standard

3 loop-induced failures (failed at cycle >= 2).


## Mbpp/286 — sustained 3, failed at cycle 4

**Original prompt**
```
"""
Write a function to find the largest sum of a contiguous array in the modified array which is formed by repeating the given array k times.
assert max_sub_array_sum_repeated([10, 20, -30, -1], 4, 3) == 30
"""
```

**Description that fed cycle 4** (model's own summary from cycle 3)
```
"""
write a python function to find the maximum subarray sum of a given array repeated $k$ times.
assert max_sub_array_sum_repeated([10, 20, -30, -1], 4, 3) == 30
"""
```

**Last passing code (cycle 3)**
```python
def max_sub_array_sum_repeated(arr, n, k):
    def kadane(a):
        max_so_far = float("-inf")
        curr_max = 0
        for x in a:
            curr_max += x
            if max_so_far < curr_max:
                max_so_far = curr_max
            if curr_max < 0:
                curr_max = 0
        return max_so_far

    if k == 1:
        return kadane(arr)

    arr_sum = sum(arr)
    if arr_sum > 0:
        return kadane(arr * 2) + (k - 2) * arr_sum
    else:
        return kadane(arr * 2)
```

**Failing code (cycle 4)**
```python
def max_sub_array_sum_repeated(arr, n, k):
    def kadane(array):
        max_so_far = float("-inf")
        curr_max = 0
        for x in array:
            curr_max += x
            if max_so_far < curr_max:
                max_so_far = curr_max
            if curr_max < 0:
                curr_max = 0
        return max_so_far

    max_single = kadane(arr)
    if k == 1:
        return max_single

    sum_arr = sum(arr)

    # Calculate max prefix sum
    max_prefix = 0
    curr_prefix = 0
    for x in arr:
        curr_prefix += x
        max_prefix = max(max_prefix, curr_prefix)

    # Calculate max suffix sum
    max_suffix = 0
    curr_suffix = 0
    for x in reversed(arr):
        curr_suffix += x
        max_suffix = max(max_suffix, curr_suffix)

    if sum_arr > 0:
        return max(max_single, max_suffix + max_prefix + (k - 2) * sum_arr)
    else:
        return max(max_single, max_suffix + max_prefix)
```

**Test outcome**
```
BASE: input=[[-1, -2, -3], 3, 3]
expected=-1
```

## Mbpp/787 — sustained 1, failed at cycle 2

**Original prompt**
```
"""
Write a function that matches a string that has an a followed by three 'b'.
assert not text_match_three("ac")
"""
```

**Description that fed cycle 2** (model's own summary from cycle 1)
```
"""
write a python function to check if a given string contains the letter 'a' followed by exactly three 'b's using regular expressions.
assert not text_match_three("ac")
"""
```

**Last passing code (cycle 1)**
```python
import re


def text_match_three(text):
    patterns = "ab{3}"
    if re.search(patterns, text):
        return True
    else:
        return False
```

**Failing code (cycle 2)**
```python
import re


def text_match_three(text):
    pattern = r"ab{3}(?!b)"
    if re.search(pattern, text):
        return True
    else:
        return False
```

**Test outcome**
```
BASE: input=['abbbba']
expected=True
```

## Mbpp/796 — sustained 6, failed at cycle 7

**Original prompt**
```
"""
Write function to find the sum of all items in the given dictionary.
assert return_sum({'a': 100, 'b':200, 'c':300}) == 600
"""
```

**Description that fed cycle 7** (model's own summary from cycle 6)
```
"""
write a python function to calculate and return the sum of all values in a dictionary.
assert return_sum({'a': 100, 'b':200, 'c':300}) == 600
"""
```

**Last passing code (cycle 6)**
```python
def return_sum(dictionary):
    return sum(dictionary.values())
```

**Failing code (cycle 7)**
```python
def return_ sum(d):
    return sum(d.values())
```

**Test outcome**
```
BASE: input=[{'a': 100, 'b': 200, 'c': 300}]
expected=600  (stopped here: crash/timeout)
PLUS: input=[{}]
expected=0  (stopped here: crash/timeout)
```
