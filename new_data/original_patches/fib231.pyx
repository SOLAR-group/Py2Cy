def fib(long n):
    cdef long long a = 0
    cdef long double b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a