# Py2Cy
Py2Cy is a Genetic Improvement tool that automatically converts Python to Cython code to speed up execution speed.

# Prerequisites 

* Python 3.5+
* Cython

# Usage
Paramaters:
* Target python file path
* Mode (exhaustive, random, walk)
* Iterations
* Epoch
* Test cases file path


Example
```
python improve_cython.py --project_path examples/fib.py --mode local --iter 20 --test test_fib.py
```

When the run is finished, the optimal patch will be found in output/result.pyx

# Files
improve_cython.py: Used to set parameters and run a search on a python file \
program.py: Represents a single Cython file \
cython_tree.py: Utility methods for the Cython AST, including the conversion code \
cython_visitor.py: Contains several implementations of visitor classes to get/edit nodes in a Cython AST \
patch.py:  Represents a single patch \
edit.py: code to insert a type to a node 
