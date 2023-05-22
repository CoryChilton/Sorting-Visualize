from collections import Counter, deque
import heapq

# def gen():
#     for i in range(5):
#         yield i

# x = gen()
# for _ in range(5):
#     print(next(x))
        
def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2

        left = arr[:mid]
        right = arr[mid:]

        mergeSort(left)
        mergeSort(right)

        l = r = i = 0

        while l < len(left) and r < len(right):
            if (left[l] <= right[r] and ascending) or (left[l] >= right[r] and not ascending):
                arr[i] = left[l]
                l += 1
                # draw_list(draw_info, {l: draw_info.GREEN, r: draw_info.RED}, True)
                # yield True
            else:
                arr[i] = right[r]
                r += 1
            i += 1

        while l < len(left):
            arr[i] = left[l]
            l += 1
            i += 1

        while r < len(right):
            arr[i] = right[r]
            r += 1
            i += 1


def mergeSortIter(lst):
    
    width = 1
    n = len(lst)
    while (width < n):
        l = 0
        while l < n:
            r = min(l + (width * 2 - 1), n - 1)
            m = min(l + width - 1, n - 1)

            #merging
            n1 = m - l + 1
            n2 = r - m
            L = [0] * n1
            R = [0] * n2
            for i in range(0, n1):
                L[i] = lst[l + i]
            for i in range(0, n2):
                R[i] = lst[m + i + 1]
        
            i, j, k = 0, 0, l
            while i < n1 and j < n2:
                if L[i] <= R[j]:
                    lst[k] = L[i]
                    i += 1
                else:
                    lst[k] = R[j]
                    j += 1
                k += 1
        
            while i < n1:
                lst[k] = L[i]
                i += 1
                k += 1
        
            while j < n2:
                lst[k] = R[j]
                j += 1
                k += 1
            #end merging

            l += width * 2
        width *= 2



lst = [9,8,7,6,5,4,3,2,1,0]
mergeSortIter(lst)

print(lst)