import random
from Cython.Compiler.AnalysedTreeTransforms import *
from Cython.Compiler.ParseTreeTransforms import *
from utilities.cython_visitor import MyVisitor, NodeVisitor, TypeInsertionVisitor, WriterVisitor
from Cython.Compiler.TreeFragment import *
from Cython.CodeWriter import *
from Cython.Compiler.Visitor import *

"""
Contains the methods to transform the source code to
and from the Cython AST and also get the modification points
"""


def get_modification_points(root):

    modification_points = list()
    visitor = NodeVisitor(None)
    visitor.visit(root)
    modification_points = visitor.positions
    return modification_points


def file_to_ast(file_path):
    with open(file_path, "r") as f:
        source = f.read()
    return parse_from_strings("fib", source)


def print_tree(root):
    PrintTree()(root)
    return


def ast_to_source(root):
    writer = WriterVisitor()
    writer.visit(root)
    source = "\n".join(writer.result.lines)
    return source


def insert_type(target, new_contents, modification_points, c_type):
    position = modification_points[target]
    visitor = TypeInsertionVisitor(None)
    visitor.target_pos = position
    visitor.c_type = c_type

    # PrintTree()(new_contents)

    normal = NormalizeTree(None)
    normal.visit(new_contents)
    visitor.visit(new_contents)

    return True
