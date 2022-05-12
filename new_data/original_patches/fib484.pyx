def fib(long double n):
    cdef long long a = 0
    cdef long long b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a