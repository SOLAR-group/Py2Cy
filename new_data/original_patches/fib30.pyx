def fib(char n):
    cdef long a = 0
    cdef double b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a