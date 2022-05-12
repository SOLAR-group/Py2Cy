def fib(double n):
    cdef short a = 0
    cdef int b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a