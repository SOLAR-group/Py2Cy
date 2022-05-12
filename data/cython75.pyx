def fib(short n):
    cdef short i
    cdef long b
    cdef long a
    a = 0
    b = 1
    for i in range(n):
        a, b = b, a + b
    return a