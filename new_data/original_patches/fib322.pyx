def fib(float n):
    cdef char a = 0
    cdef int b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a