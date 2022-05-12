def fib(double n):
    cdef long a = 0
    cdef long b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a