def merge(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def mergesort(unsorted):
    if len(unsorted) < 2:
        return unsorted
    middle = len(unsorted) / 2
    left = mergesort(unsorted[:middle])
    right = mergesort(unsorted[middle:])
    return merge(left, right)

if __name__ == '__main__':
    print mergesort([3,4,7,8,5,6,4,2,6,1,2,9,87,])

