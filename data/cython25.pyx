def fib(short n):
    cdef short i
    cdef int b
    cdef int a
    a = 0
    b = 1
    for i in range(n):
        a, b = b, a + b
    return a