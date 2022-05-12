def fib(short n):
    cdef long b
    cdef long a
    cdef long i
    a = 0
    b = 1
    for i in range(n):
        a, b = b, a + b
    return a