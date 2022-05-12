import importlib
import subprocess
import timeit
from examples import integral


def test_integral():
    expected = integral.integrate_f(0, 2, 5000)
    result = ()
    file = 'output/temp.pyx'
    # Compile .pyx program
    process = subprocess.Popen(['Cythonize', '-i', file],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()
    temp = importlib.import_module("output.temp")
    if stderr and process.returncode:
        # compilation_fails += 1
        # print(file + ": Compilation Failed")
        print("compilation_fail")
    else:
        try:
            start = timeit.default_timer()
            output = temp.integrate_f(0, 2, 5000)
            end = timeit.default_timer()
        except Exception as e:
            # print(e)
            # print(file + ": Bug Found")
            print("bug_found")
        else:
            t = end - start
            if output == expected:
                print(float(t))
            else:
                # wrong += 1
                # print(file + ": Wrong Value")
                print("wrong_value")

    return


if __name__ == "__main__":
    test_integral()
