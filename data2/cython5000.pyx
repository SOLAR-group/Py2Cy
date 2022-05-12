def f(double x):
    return x ** 2 - x
def integrate_f(int a, int b, N):
    cdef i
    cdef dx
    cdef s
    s = 0
    dx = b / N - a / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx