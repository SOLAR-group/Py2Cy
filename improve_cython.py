import argparse
from copy import deepcopy
from hashlib import new
import itertools
from numbers import Integral
import random
import timeit
from tracemalloc import start
from Cython.Compiler.TreeFragment import *
from Cython.Compiler.Visitor import *
from Cython.Compiler.Main import *
from Cython.CodeWriter import *
from Cython.Compiler.AnalysedTreeTransforms import *
from Cython.Compiler.ParseTreeTransforms import *
from Cython.Compiler.Symtab import *
from algorithm.exhaustive import ExhaustiveSearch
import utilities.cython_tree as cy
from utilities.cython_visitor import MyVisitor, NodeVisitor, DeclarationVisitor, TypeInsertionVisitor, WriterVisitor
from edit import TypeInsertion
from algorithm.local_search import LocalSearch
from program import Program


def preprocess(filename):

    ast = cy.file_to_ast(filename)

    # Add in declarations to variables in each scope
    normal = NormalizeTree(None)
    declaration = DeclarationVisitor(None)
    # Normalize structure of tree and add declarations
    normal.visit(ast)

    declaration.visit(ast)

    # Write to Cython file
    with open("output/test.pyx", 'w') as file:
        file.write(cy.ast_to_source(ast))

    ast = cy.file_to_ast("output/test.pyx")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Py2Cy Python Genetic Improvement')
    parser.add_argument('--project_path', type=str)
    parser.add_argument('--mode', type=str, default='local')
    parser.add_argument('--epoch', type=int, default=30,
                        help='total epoch(default: 30)')
    parser.add_argument('--iter', type=int, default=100,
                        help='total iterations per epoch(default: 100)')
    parser.add_argument('--test', type=str, default=100,
                        help='total iterations per epoch(default: 100)')
    args = parser.parse_args()
    assert args.mode in ['local', 'exhaustive', 'random']

    preprocess(args.project_path)
    program = Program("output/test.pyx", args.test)

    if args.mode == 'local':
        local_search = LocalSearch(program)
        local_search.run()

    elif args.mode == 'exhaustive':
        exhaustive_search = ExhaustiveSearch(program)
        exhaustive_search.run()

    elif args.mode == 'random':
        exhaustive_search = ExhaustiveSearch(program)
        exhaustive_search.run()

    # ast = cy.file_to_ast("./output/temp.pyx")
    # PrintTree()(ast)
    # print(cy.ast_to_source(ast))

    # start_time = timeit.default_timer()
    # print(integrate.integrate_f(0, 2, 50000))
    # end_time = timeit.default_timer()
    # print(end_time-start_time)

    # start_time = timeit.default_timer()
    # print(integral.integrate_f(0, 2, 50000))
    # end_time = timeit.default_timer()
    # print(end_time-start_time)

    # program = Program("output/test.pyx")
    # exhaustive_search = ExhaustiveSearch(program)
    # exhaustive_search.run()
