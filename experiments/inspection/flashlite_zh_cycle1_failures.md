# Failed loops — google/gemini-3.1-flash-lite — loop=crosslingual

28 loop-induced failures (failed at cycle >= 1).


## Mbpp/3 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a python function to identify non-prime numbers.
assert is_not_prime(2) == False
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def is_not_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return True
    return False
```

**Test outcome**
```
BASE: input=[1]
expected=True
PLUS: input=[True]
expected=True
```

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

## Mbpp/84 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to find the nth number in the newman conway sequence.
assert sequence(10) == 6
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def sequence(n):
    if n <= 2:
        return 1
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 1
    
    for i in range(3, n + 1):
        dp[i] = dp[dp[i - 1]] + dp[i - dp[i - 1]]
        
    return dp[n]
```

**Test outcome**
```
PLUS: input=[1000000]
expected=510403
```

## Mbpp/92 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to check whether the given number is undulating or not.
assert is_undulating(1212121) == True
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def is_undulating(n):
    s = str(n)
    if len(s) < 3:
        return False
    for i in range(len(s) - 2):
        if s[i] != s[i + 2]:
            return False
    return s[0] != s[1]
```

**Test outcome**
```
PLUS: input=[82]
expected=True
```

## Mbpp/124 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to get the angle of a complex number.
assert math.isclose(angle_complex(0,1j), 1.5707963267948966, rel_tol=0.001)
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
import math
import cmath

def angle_complex(real, imag):
    return cmath.phase(complex(real, imag))
```

**Test outcome**
```
BASE: input=(0.0, 1j)
expected=1.5707963267948966
PLUS: input=(0.0, 1j)
expected=1.5707963267948966
```

## Mbpp/126 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a python function to find the sum of common divisors of two given numbers.
assert sum(10,15) == 6
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
import math

def sum_common_divisors(a, b):
    gcd = math.gcd(a, b)
    total = 0
    for i in range(1, int(math.sqrt(gcd)) + 1):
        if gcd % i == 0:
            total += i
            if i*i != gcd:
                total += gcd // i
    return total
```

**Test outcome**
```
BASE: input=[10, 15]
expected=6.0  (stopped here: crash/timeout)
PLUS: input=[27, 81]
expected=40.0  (stopped here: crash/timeout)
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

## Mbpp/160 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function that returns integers x and y that satisfy ax + by = n as a tuple, or return None if no solution exists.
assert find_solution(2, 3, 7) == (2, 1)
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def find_solution(a, b, n):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x0, y0 = extended_gcd(a, b)
    
    if n % gcd != 0:
        return None
    
    x = x0 * (n // gcd)
    y = y0 * (n // gcd)
    
    return (x, y)
```

**Test outcome**
```
BASE: input=[2, 3, 7]
expected=(2, 1)
PLUS: input=[25, 10, 500]
expected=(0, 50)
```

## Mbpp/223 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function that takes in a sorted array, its length (n), and an element and returns whether the element is the majority element in the given sorted array. (The majority element is the element that occurs more than n/2 times.)
assert is_majority([1, 2, 3, 3, 3, 3, 10], 7, 3) == True
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def is_majority(arr, n, x):
    import bisect
    
    first_idx = bisect.bisect_left(arr, x)
    
    if first_idx < n and arr[first_idx] == x:
        last_idx = first_idx + (n // 2)
        if last_idx < n and arr[last_idx] == x:
            return True
            
    return False
```

**Test outcome**
```
PLUS: input=[[], 1, 0]
expected=False
```

## Mbpp/260 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to find the nth newman–shanks–williams prime number.
assert newman_prime(3) == 7
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def newman_prime(n):
    def nsw(k):
        if k == 0: return 1
        if k == 1: return 1
        a, b = 1, 1
        for _ in range(2, k + 1):
            a, b = b, 2 * b + a
        return b
    
    count = 0
    k = 0
    while True:
        val = nsw(k)
        if is_prime(val):
            count += 1
            if count == n:
                return val
        k += 1
```

**Test outcome**
```
BASE: input=[3]
expected=7
PLUS: input=[100]
expected=94741125149636933417873079920900017937
```

## Mbpp/278 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to find the number of elements that occurs before the tuple element in the given tuple.
assert count_first_elements((1, 5, 7, (4, 6), 10) ) == 3
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def count_first_elements(tup):
    for i, element in enumerate(tup):
        if isinstance(element, tuple):
            return i
    return len(tup)
```

**Test outcome**
```
PLUS: input=[(1, 2, 3, 4, 5, 6)]
expected=5
```

## Mbpp/285 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function that checks whether a string contains the 'a' character followed by two or three 'b' characters.
assert text_match_two_three("ac")==(False)
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
import re

def text_match_two_three(text):
    return bool(re.search(r'ab{2,3}(?!b)', text))
```

**Test outcome**
```
BASE: input=['abbbba']
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

## Mbpp/300 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to find the count of all binary sequences of length 2n such that sum of first n bits is same as sum of last n bits.
assert math.isclose(count_binary_seq(1), 2.0, rel_tol=0.001)
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
import math

def count_binary_seq(n):
    count = 0
    for k in range(n + 1):
        ways = math.comb(n, k)
        count += ways * ways
    return float(count)
```

**Test outcome**
```
PLUS: input=[1000]
expected=inf
```

## Mbpp/311 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a python function to set the left most unset bit.
assert set_left_most_unset_bit(10) == 14
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def set_left_most_unset_bit(n):
    if n == 0:
        return 1
    
    m = n
    pos = 0
    while m > 0:
        if not (m & 1):
            return n | (1 << pos)
        m >>= 1
        pos += 1
    
    return n | (1 << pos)
```

**Test outcome**
```
BASE: input=[10]
expected=14
PLUS: input=[255]
expected=255
```

## Mbpp/427 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to convert a date of yyyy-mm-dd format to dd-mm-yyyy format.
assert change_date_format("2026-01-02") == '02-01-2026'
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def change_date_format(date_str):
    year, month, day = date_str.split('-')
    return f"{day}-{month}-{year}"
```

**Test outcome**
```
PLUS: input=['2021-1-026']
expected='02-1-20216'
```

## Mbpp/448 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to calculate the sum of perrin numbers.
assert cal_sum(9) == 49
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def cal_sum(n):
    if n == 0:
        return 3
    if n == 1:
        return 3
    if n == 2:
        return 3
    
    perrin = [3, 0, 2]
    for i in range(3, n + 1):
        perrin.append(perrin[i - 2] + perrin[i - 3])
    
    return sum(perrin)
```

**Test outcome**
```
PLUS: input=[2]
expected=5
```

## Mbpp/559 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to find the sum of the largest contiguous sublist in the given list.
assert max_sub_array_sum([-2, -3, 4, -1, -2, 1, 5, -3], 8) == 7
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def max_sub_array_sum(arr, n):
    max_so_far = float('-inf')
    current_max = 0
    
    for i in range(n):
        current_max += arr[i]
        if max_so_far < current_max:
            max_so_far = current_max
        if current_max < 0:
            current_max = 0
            
    return max_so_far
```

**Test outcome**
```
PLUS: input=[[], 0]
expected=0
```

## Mbpp/610 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a python function which takes a list and returns a list with the same elements, but the k'th element removed.
assert remove_kth_element([1,1,2,3,4,4,5,1],3)==[1, 1, 3, 4, 4, 5, 1]
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def remove_kth_element(lst, k):
    return lst[:k] + lst[k+1:]
```

**Test outcome**
```
BASE: input=[[1, 1, 2, 3, 4, 4, 5, 1], 3]
expected=[1, 1, 3, 4, 4, 5, 1]
PLUS: input=[[1, 2, 3, 4, 5], 1]
expected=[2, 3, 4, 5]
```

## Mbpp/622 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to find the median of two sorted lists of same size.
assert get_median([1, 12, 15, 26, 38], [2, 13, 17, 30, 45], 5) == 16.0
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def get_median(arr1, arr2, n):
    def get_median_single(arr):
        if n % 2 == 0:
            return (arr[n // 2] + arr[n // 2 - 1]) / 2
        return float(arr[n // 2])

    if n == 0:
        return 0
    if n == 1:
        return (arr1[0] + arr2[0]) / 2
    if n == 2:
        return (max(arr1[0], arr2[0]) + min(arr1[1], arr2[1])) / 2

    m1 = get_median_single(arr1)
    m2 = get_median_single(arr2)

    if m1 == m2:
        return m1

    if m1 < m2:
        if n % 2 == 0:
            return get_median(arr1[n // 2 - 1:], arr2[:n // 2 + 1], n // 2 + 1)
        return get_median(arr1[n // 2:], arr2[:n // 2 + 1], n // 2 + 1)
    else:
        if n % 2 == 0:
            return get_median(arr2[n // 2 - 1:], arr1[:n // 2 + 1], n // 2 + 1)
        return get_median(arr2[n // 2:], arr1[:n // 2 + 1], n // 2 + 1)
```

**Test outcome**
```
PLUS: input=[[1], [2], 0]
expected=0.5
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

## Mbpp/735 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a python function to toggle bits of the number except the first and the last bit. 
assert toggle_middle_bits(9) == 15
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def toggle_middle_bits(n):
    if n < 4:
        return n
    
    mask = (1 << (n.bit_length() - 1)) - 2
    return n ^ mask
```

**Test outcome**
```
PLUS: input=[True]
expected=3
```

## Mbpp/757 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to count the pairs of reverse strings in the given string list. 
assert count_reverse_pairs(["julia", "best", "tseb", "for", "ailuj"])== 2
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def count_reverse_pairs(strings):
    count = 0
    seen = set()
    for s in strings:
        reversed_s = s[::-1]
        if reversed_s in seen:
            count += 1
        seen.add(s)
    return count
```

**Test outcome**
```
PLUS: input=[['ab', 'ba', 'dc', 'ef', 'fe', 'gh', 'hg', 'ji', 'fe', 'ef']]
expected=6
```

## Mbpp/759 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to check whether a given string is a decimal number with a precision of 2.
assert is_decimal('123.11')==True
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
import re

def is_decimal(s):
    return bool(re.fullmatch(r'^\d+\.\d{2}$', s))
```

**Test outcome**
```
PLUS: input=['123']
expected=True
```

## Mbpp/777 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a python function to find the sum of non-repeated elements in a given list.
assert find_sum([1,2,3,1,1,4,5,6]) == 21
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def find_sum(lst):
    from collections import Counter
    counts = Counter(lst)
    return sum(item for item, count in counts.items() if count == 1)
```

**Test outcome**
```
BASE: input=[[1, 2, 3, 1, 1, 4, 5, 6]]
expected=21
PLUS: input=[[-1, -2, -3, -1, -1, -4, -5, -6]]
expected=-21
```

## Mbpp/785 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to convert tuple string to integer tuple.
assert tuple_str_int("(7, 8, 9)") == (7, 8, 9)
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
import ast

def tuple_str_int(tuple_str):
    return ast.literal_eval(tuple_str)
```

**Test outcome**
```
PLUS: input=['((7, 8, 9)']
expected=(7, 8, 9)
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

## Mbpp/806 — sustained 0, failed at cycle 1

**Original prompt**
```
"""
Write a function to find maximum run of uppercase characters in the given string.
assert max_run_uppercase('GeMKSForGERksISBESt') == 5
"""
```

**Description that fed cycle 1** (model's own summary from cycle 0)
```

```

**Last passing code (cycle 0)**
```python

```

**Failing code (cycle 1)**
```python
def max_run_uppercase(s):
    max_run = 0
    current_run = 0
    for char in s:
        if char.isupper():
            current_run += 1
            if current_run > max_run:
                max_run = current_run
        else:
            current_run = 0
    return max_run
```

**Test outcome**
```
PLUS: input=['Aaa']
expected=0
```
