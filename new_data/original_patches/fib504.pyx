def fib(long double n):
    cdef long double a = 0
    cdef char b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a