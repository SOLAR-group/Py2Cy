def fib(char n):
    cdef short a = 0
    cdef short b = 1
    for i in range(n):
        (a, b) = (b, a + b)
    return a