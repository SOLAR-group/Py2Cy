def fib(int n):
    cdef float a = 0
    cdef double b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a