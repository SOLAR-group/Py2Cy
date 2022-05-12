def fib(n):
    cdef  a
    cdef  b
    cdef  i
    a = 0
    b = 1
    for i in range(n):
        a, b = b, a + b
    return a