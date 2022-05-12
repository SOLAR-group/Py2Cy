import itertools
from operator import truediv
import subprocess
import time
import timeit
from unittest.mock import patch
from Cython.Compiler.TreeFragment import *
from Cython.Compiler.Visitor import *
from Cython.Compiler.Main import *
from Cython.CodeWriter import *
from Cython.Compiler.AnalysedTreeTransforms import *
from Cython.Compiler.ParseTreeTransforms import *
from Cython.Compiler.Symtab import *
from algorithm.algorithm import Algorithm
import utilities.cython_tree as cy
from edit import TypeInsertion
from patch import Patch
from examples import fib


class ExhaustiveSearch(Algorithm):
    def __init__(self, program):
        self.program = program

    def run(self):
        run_start = time.time()
        normal = NormalizeTree(None)
        types = ['short', 'long']
        ast = cy.file_to_ast(self.program.file_path)
        normal.visit(ast)
        modifications = len(self.program.modification_points)
        points = [x for x in range(modifications)]

        patches = []

        combinations = [p for p in itertools.product(
            types, repeat=modifications)]

        for c in combinations:
            zipped = zip(c, points)
            patches.append(list(zipped))
        best_patch = Patch(self.program)

        print(patches)

        start = timeit.default_timer()
        expected = fib.fib(75)
        end = timeit.default_timer()
        fastest = end-start
        fast_index = 0
        print(fastest)

        file = 'output/temp.pyx'
        result_list = {"success": 0, "compilation_fail": 0,
                       "bug_found": 0, "wrong_value": 0}

        for i in range(len(patches)):
            print(i)
            new_patch = best_patch.clone()
            for edit in patches[i]:
                new_patch.add(TypeInsertion.create(
                    self.program, edit[1], edit[0]))
            result = self.program.evaluate_patch(new_patch)
            print(result)

            result_list[result["status"]] += 1

            if result["status"] == "success":
                value = float(result["value"])
                if value < fastest:
                    fastest = value
                    fast_index = i
                    best_patch = new_patch

        print(fast_index)
        print(fastest)
        print(result_list)
        self.program.write_result(best_patch)

        run_end = time.time()
        print(run_end-run_start)

        return
