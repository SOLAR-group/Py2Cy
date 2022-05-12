def f(x):
    return x ** 2 - x
def integrate_f(a, b, N):
    cdef  i
    cdef  s
    cdef  dx
    s = 0
    dx = b / N - a / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx