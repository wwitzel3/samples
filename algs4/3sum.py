"""
Given a list of numbers
Determine if the sum of any 3 exist
"""

a = range(0,10)

def binary_search(a, i, imin, imax):
    if imax < imin:
        return -1
    else:
        imid = imin + ((imax - imin) / 2)
        if a[imid] > i:
            return binary_search(a, i, imin, imid-1)
        elif a[imid] < i:
            return binary_search(a, i, imid+1, imax)
        else:
            return imid;

if __name__ == '__main__':
    for i in a:
        for j in a:
            n = binary_search(a, -(a[i]+a[j]), 0, len(a))
            if n > -1:
                print n
