# Failed loops — google/gemini-3.1-flash-lite — loop=standard

7 loop-induced failures (failed at cycle >= 2).


## Mbpp/162 — sustained 1, failed at cycle 2

**Original prompt**
```
"""
Write a function to calculate the sum (n - 2*i) from i=0 to n // 2, for instance n + (n-2) + (n-4)... (until n-x =< 0).
assert sum_series(6) == 12
"""
```

**Description that fed cycle 2** (model's own summary from cycle 1)
```
"""
write a python function to calculate the sum of a series that subtracts twice the index from a given integer $n$ for all values up to $n/2$.
assert sum_series(6) == 12
"""
```

**Last passing code (cycle 1)**
```python
def sum_series(n):
    return sum(n - 2 * i for i in range(n // 2 + 1))
```

**Failing code (cycle 2)**
```python
def sum_series(n):
    total = 0
    for i in range(int(n / 2) + 1):
        total += (n - 2 * i)
    return total
```

**Test outcome**
```
PLUS: input=[-1]
expected=0
```

## Mbpp/280 — sustained 1, failed at cycle 2

**Original prompt**
```
"""
Write a function that takes in an array and element and returns a tuple containing a boolean that indicates if the element is in the array and the index position of the element (or -1 if the element is not found).
assert sequential_search([11,23,58,31,56,77,43,12,65,19],31) == (True, 3)
"""
```

**Description that fed cycle 2** (model's own summary from cycle 1)
```
"""
write a python function to perform a sequential search on a list to determine if a specific element exists and return its index if found.
assert sequential_search([11,23,58,31,56,77,43,12,65,19],31) == (True, 3)
"""
```

**Last passing code (cycle 1)**
```python
def sequential_search(arr, element):
    for i in range(len(arr)):
        if arr[i] == element:
            return (True, i)
    return (False, -1)
```

**Failing code (cycle 2)**
```python
def sequential_search(arr, target):
    for index, value in enumerate(arr):
        if value == target:
            return (True, index)
    return (False, None)

assert sequential_search([11, 23, 58, 31, 56, 77, 43, 12, 65, 19], 31) == (True, 3)
```

**Test outcome**
```
PLUS: input=[[], 10]
expected=(False, -1)
```

## Mbpp/286 — sustained 1, failed at cycle 2

**Original prompt**
```
"""
Write a function to find the largest sum of a contiguous array in the modified array which is formed by repeating the given array k times.
assert max_sub_array_sum_repeated([10, 20, -30, -1], 4, 3) == 30
"""
```

**Description that fed cycle 2** (model's own summary from cycle 1)
```
"""
write a python function to calculate the maximum subarray sum of an array that is repeated k times by using Kadane's algorithm and adjusting for the total sum of the array.
assert max_sub_array_sum_repeated([10, 20, -30, -1], 4, 3) == 30
"""
```

**Last passing code (cycle 1)**
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

**Failing code (cycle 2)**
```python
def max_sub_array_sum_repeated(arr, k, n):
    def kadane(a):
        max_so_far = float('-inf')
        current_max = 0
        for x in a:
            current_max += x
            if max_so_far < current_max:
                max_so_far = current_max
            if current_max < 0:
                current_max = 0
        return max_so_far

    if k == 1:
        return kadane(arr)

    total_sum = sum(arr)
    if total_sum > 0:
        max_kadane_two = kadane(arr * 2)
        return max_kadane_two + (k - 2) * total_sum
    else:
        return kadane(arr * 2)
```

**Test outcome**
```
BASE: input=[[-1, 10, 20], 3, 2]
expected=59
PLUS: input=[[5, -2, 10, 4, -7, 3], 6, 5]
expected=69
```

## Mbpp/308 — sustained 2, failed at cycle 3

**Original prompt**
```
"""
Write a function to find the specified number of largest products from two given lists, selecting one factor from each list.
assert large_product([1, 2, 3, 4, 5, 6],[3, 6, 8, 9, 10, 6],3)==[60, 54, 50]
"""
```

**Description that fed cycle 3** (model's own summary from cycle 2)
```
"""
write a python function to calculate the products of all possible pairs from two lists and return the n largest values using a heap.
assert large_product([1, 2, 3, 4, 5, 6],[3, 6, 8, 9, 10, 6],3)==[60, 54, 50]
"""
```

**Last passing code (cycle 2)**
```python
import heapq

def large_product(list1, list2, n):
    products = []
    for x in list1:
        for y in list2:
            products.append(x * y)
    return heapq.nlargest(n, products)
```

**Failing code (cycle 3)**
```python
import heapq

def large_product(list1, list2, n):
    heap = []
    for x in list1:
        for y in list2:
            product = x * y
            if len(heap) < n:
                heapq.heappush(heap, product)
            else:
                if product > heap[0]:
                    heapq.heapreplace(heap, product)
    return sorted(heap, reverse=True)
```

**Test outcome**
```
PLUS: input=[[61.017129591114184, 19.303378474526568, 49.402419273875154, -6.658136072450631, 55.36349167122134, 6.408487552626596, -22.555835342170255, -61.03464372753109, 76.32506038662768, 61.017129591114184], [61.017129591114184, 19.303378474526568, 49.402419273875154, -6.658136072450631, 55.36349167122134, 6.408487552626596, -22.555835342170255, -61.03464372753109, 76.32506038662768, 61.017129591114184], 0]
expected=[]
```

## Mbpp/612 — sustained 2, failed at cycle 3

**Original prompt**
```
"""
Write a python function which takes a list of lists, where each sublist has two elements, and returns a list of two lists where the first list has the first element of each sublist and the second one has the second.
assert merge([['x', 'y'], ['a', 'b'], ['m', 'n']]) == [['x', 'a', 'm'], ['y', 'b', 'n']]
"""
```

**Description that fed cycle 3** (model's own summary from cycle 2)
```
"""
write a python function to transpose a matrix by swapping its rows and columns using the zip function.
assert merge([['x', 'y'], ['a', 'b'], ['m', 'n']]) == [['x', 'a', 'm'], ['y', 'b', 'n']]
"""
```

**Last passing code (cycle 2)**
```python
def merge(matrix):
    return [list(row) for row in zip(*matrix)]

assert merge([['x', 'y'], ['a', 'b'], ['m', 'n']]) == [['x', 'a', 'm'], ['y', 'b', 'n']]
```

**Failing code (cycle 3)**
```python
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

assert transpose([['x', 'y'], ['a', 'b'], ['m', 'n']]) == [['x', 'a', 'm'], ['y', 'b', 'n']]
```

**Test outcome**
```
BASE: input=[[['x', 'y'], ['a', 'b'], ['m', 'n']]]
expected=[['x', 'a', 'm'], ['y', 'b', 'n']]  (stopped here: crash/timeout)
PLUS: input=[[['x', 1], ['y', 2], [True, 'z']]]
expected=[['x', 'y', True], [1, 2, 'z']]  (stopped here: crash/timeout)
```

## Mbpp/626 — sustained 1, failed at cycle 2

**Original prompt**
```
"""
Write a python function to find the area of the largest triangle that can be inscribed in a semicircle with a given radius.
assert triangle_area(-1) == None
"""
```

**Description that fed cycle 2** (model's own summary from cycle 1)
```
"""
write a python function to calculate the area of a square given its side length, while returning None for negative inputs.
assert triangle_area(-1) == None
"""
```

**Last passing code (cycle 1)**
```python
def triangle_area(radius):
    if radius < 0:
        return None
    return radius**2
```

**Failing code (cycle 2)**
```python
def square_area(side_length):
    if side_length < 0:
        return None
    return side_length ** 2
```

**Test outcome**
```
BASE: input=[-1]
expected=None  (stopped here: crash/timeout)
PLUS: input=[-0.5]
expected=None  (stopped here: crash/timeout)
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
write a python function to check if a given string contains the letter 'a' followed by exactly three 'b's using a regular expression.
assert not text_match_three("ac")
"""
```

**Last passing code (cycle 1)**
```python
import re

def text_match_three(text):
    return bool(re.search(r'ab{3}', text))
```

**Failing code (cycle 2)**
```python
import re

def text_match_three(text):
    return bool(re.search(r'ab{3}(?!b)', text))
```

**Test outcome**
```
BASE: input=['abbbba']
expected=True
```
