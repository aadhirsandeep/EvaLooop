# Failed loops — google/gemini-3.1-flash-lite — loop=crosslingual

5 loop-induced failures (failed at cycle >= 2).


## Mbpp/63 — sustained 8, failed at cycle 9

**Original prompt**
```
"""
Write a function to find the maximum difference between available pairs in the given tuple list.
assert max_difference([(3, 5), (1, 7), (10, 3), (1, 2)]) == 7
"""
```

**Description that fed cycle 9** (model's own summary from cycle 8)
```
"""
编写一个Python函数来计算元组列表中每对元素之差的绝对值的最大值。
assert max_difference([(3, 5), (1, 7), (10, 3), (1, 2)]) == 7
"""
```

**Last passing code (cycle 8)**
```python
def max_difference(tuples_list):
    return max(abs(a - b) for a, b in tuples_list)
```

**Failing code (cycle 9)**
```python
def max_difference(tuples_list):
    flat_list = [item for t in tuples_list for item in t]
    return max(flat_list) - min(flat_list)
```

**Test outcome**
```
BASE: input=[[(3, 5), (1, 7), (10, 3), (1, 2)]]
expected=7
PLUS: input=[[(1000000, 999999), (10000000, 9999999), (100000000, 99999999), (1000000000, 999999999)]]
expected=1
```

## Mbpp/129 — sustained 1, failed at cycle 2

**Original prompt**
```
"""
Write a function to calculate whether the matrix is a magic square.
assert magic_square_test([[7, 12, 1, 14], [2, 13, 8, 11], [16, 3, 10, 5], [9, 6, 15, 4]])==True
"""
```

**Description that fed cycle 2** (model's own summary from cycle 1)
```
"""
编写一个Python函数来判断给定的矩阵是否为幻方。
assert magic_square_test([[7, 12, 1, 14], [2, 13, 8, 11], [16, 3, 10, 5], [9, 6, 15, 4]])==True
"""
```

**Last passing code (cycle 1)**
```python
def magic_square_test(matrix):
    n = len(matrix)
    if n == 0:
        return True
    
    target_sum = sum(matrix[0])
    
    for row in matrix:
        if sum(row) != target_sum:
            return False
            
    for col in range(n):
        if sum(matrix[row][col] for row in range(n)) != target_sum:
            return False
            
    if sum(matrix[i][i] for i in range(n)) != target_sum:
        return False
        
    if sum(matrix[i][n - 1 - i] for i in range(n)) != target_sum:
        return False
        
    return True
```

**Failing code (cycle 2)**
```python
def magic_square_test(matrix):
    n = len(matrix)
    if n == 0:
        return True
    
    target_sum = sum(matrix[0])
    
    for row in matrix:
        if sum(row) != target_sum:
            return False
            
    for col in range(n):
        if sum(matrix[row][col] for row in range(n)) != target_sum:
            return False
            
    if sum(matrix[i][i] for i in range(n)) != target_sum:
        return False
        
    if sum(matrix[i][n - 1 - i] for i in range(n)) != target_sum:
        return False
        
    flat_list = [num for row in matrix for num in row]
    if sorted(flat_list) != list(range(1, n * n + 1)):
        return False
        
    return True
```

**Test outcome**
```
PLUS: input=[[[7, 7], [7, 7]]]
expected=True
```

## Mbpp/286 — sustained 2, failed at cycle 3

**Original prompt**
```
"""
Write a function to find the largest sum of a contiguous array in the modified array which is formed by repeating the given array k times.
assert max_sub_array_sum_repeated([10, 20, -30, -1], 4, 3) == 30
"""
```

**Description that fed cycle 3** (model's own summary from cycle 2)
```
"""
编写一个Python函数来计算将给定数组重复k次后，其子数组的最大和。
assert max_sub_array_sum_repeated([10, 20, -30, -1], 4, 3) == 30
"""
```

**Last passing code (cycle 2)**
```python
def max_sub_array_sum_repeated(arr, n, k):
    if k == 1:
        max_so_far = float('-inf')
        current_max = 0
        for x in arr:
            current_max += x
            if max_so_far < current_max:
                max_so_far = current_max
            if current_max < 0:
                current_max = 0
        return max_so_far

    total_sum = sum(arr)
    extended_arr = arr * 2
    max_so_far = float('-inf')
    current_max = 0
    for x in extended_arr:
        current_max += x
        if max_so_far < current_max:
            max_so_far = current_max
        if current_max < 0:
            current_max = 0
            
    if total_sum > 0:
        return max_so_far + (k - 2) * total_sum
    else:
        return max_so_far
```

**Failing code (cycle 3)**
```python
def max_sub_array_sum_repeated(arr, k, n):
    if k == 1:
        max_so_far = float('-inf')
        current_max = 0
        for x in arr:
            current_max += x
            if max_so_far < current_max:
                max_so_far = current_max
            if current_max < 0:
                current_max = 0
        return max_so_far

    total_sum = sum(arr)
    extended_arr = arr * 2
    max_so_far = float('-inf')
    current_max = 0
    for x in extended_arr:
        current_max += x
        if max_so_far < current_max:
            max_so_far = current_max
        if current_max < 0:
            current_max = 0
            
    if total_sum > 0:
        return max_so_far + (k - 2) * total_sum
    else:
        return max_so_far
```

**Test outcome**
```
BASE: input=[[-1, 10, 20], 3, 2]
expected=59
PLUS: input=[[5, -2, 10, 4, -7, 3], 6, 5]
expected=69
```

## Mbpp/626 — sustained 2, failed at cycle 3

**Original prompt**
```
"""
Write a python function to find the area of the largest triangle that can be inscribed in a semicircle with a given radius.
assert triangle_area(-1) == None
"""
```

**Description that fed cycle 3** (model's own summary from cycle 2)
```
"""
编写一个Python函数来计算给定半径的圆的面积（注：代码逻辑中使用了半径的平方，通常圆面积公式应为 πr²）。
assert triangle_area(-1) == None
"""
```

**Last passing code (cycle 2)**
```python
import math

def triangle_area(radius):
    if radius < 0:
        return None
    return radius ** 2
```

**Failing code (cycle 3)**
```python
import math

def circle_area(radius):
    if radius < 0:
        return None
    return math.pi * (radius ** 2)
```

**Test outcome**
```
BASE: input=[-1]
expected=None  (stopped here: crash/timeout)
PLUS: input=[-0.5]
expected=None  (stopped here: crash/timeout)
```

## Mbpp/787 — sustained 2, failed at cycle 3

**Original prompt**
```
"""
Write a function that matches a string that has an a followed by three 'b'.
assert not text_match_three("ac")
"""
```

**Description that fed cycle 3** (model's own summary from cycle 2)
```
"""
编写一个Python函数来检查字符串中是否包含“ab”后面紧跟四个“b”的子串。
assert not text_match_three("ac")
"""
```

**Last passing code (cycle 2)**
```python
import re

def text_match_three(text):
    return bool(re.search(r'ab{4}', text))
```

**Failing code (cycle 3)**
```python
import re

def text_match_three(text):
    return bool(re.search(r'ab{5}', text))
```

**Test outcome**
```
BASE: input=['abbbba']
expected=True
```
