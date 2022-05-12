def fib(long long n):
    cdef int a = 0
    cdef double b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a