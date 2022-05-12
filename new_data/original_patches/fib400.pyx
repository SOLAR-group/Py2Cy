def fib(double n):
    cdef int a = 0
    cdef char b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a