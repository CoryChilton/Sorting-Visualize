def partition(arr, l, r):
    i = ( l - 1 )
    x = arr[r]
  
    for j in range(l, r):
        if   arr[j] <= x:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
  
    arr[i + 1], arr[r] = arr[r], arr[i + 1]
    return (i + 1)

def quickSortIterative(arr):
  
    # Create an auxiliary stack
    size = len(arr)
    stack = [0] * (size)
  
    # initialize top of stack
    top = -1
  
    # push initial values of l and r to stack
    top = top + 1
    stack[top] = 0
    top = top + 1
    stack[top] = len(arr) - 1
  
    # Keep popping from stack while is not empty
    while top >= 0:
  
        # Pop r and l
        r = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1
  
        # Set pivot element at its correct position in
        # sorted array
        p = partition( arr, l, r)
  
        # If there are elements on left side of pivot,
        # then push left side to stack
        if p-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1
  
        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < r:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = r
  
# Driver code to test above
arr = [4, 3, 5, 2, 1, 3, 2, 3]
n = len(arr)
quickSortIterative(arr)
print(arr)