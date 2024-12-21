"""
Given an array of integers and a target value, determine the number of pairs of array elements that have a difference equal to the target value.

Example
k = 1
arr = [1,2,3,4]

There are three values that differ by k = 1: 2-1=1, 3-2=1, and 4-3=1. Return 3.

Function Description

Complete the pairs function below.

pairs has the following parameter(s):

int k: an integer, the target difference
int arr[n]: an array of integers
Returns

int: the number of pairs that satisfy the criterion
Input Format

The first line contains two space-separated integers n and k, the size of arr and the target value.
The second line contains n space-separated integers of the array arr.

Constraints
2 <= n <= 10^5
0 < k < 10^9
0 < arr[i] < 2^31 - 1
each integer arr[i] will be unique

Sample Input

STDIN       Function
-----       --------
5 2         arr[] size n = 5, k =2
1 5 3 4 2   arr = [1, 5, 3, 4, 2]
Sample Output

3
Explanation

There are 3 pairs of integers in the set with a difference of 2: [5,3], [4,2] and [3,1]. .
"""

#
# Complete the 'pairs' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY arr
#

def pairs(k, arr):
    # Write your code here
    setarr = set(arr)
    pairs = 0

    for itm in setarr:
        if itm + k in setarr:
            pairs += 1

    return pairs

if __name__ == '__main__':

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    k = int(first_multiple_input[1])

    arr = list(map(int, input().rstrip().split()))

    print(pairs(k, arr))
