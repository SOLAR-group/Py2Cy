def fib(float n):
    cdef long double a = 0
    cdef float b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a