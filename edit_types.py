from Cython.Compiler.Nodes import *
from Cython.Compiler.ModuleNode import *
from Cython.Compiler.AnalysedTreeTransforms import *
from Cython.Compiler.ParseTreeTransforms import *
import random


def get_type(pos, edit_type):
    return CSimpleBaseTypeNode(pos, name=edit_type, module_path=[
    ], is_basic_c_type=True, signed=1, longness=0, is_self_arg=False)


def get_name_declarator(pos, node_name, value):
    return CNameDeclaratorNode(pos, name=node_name, cname=node_name, default=value)


def get_func_declarator(pos, base, arguments):
    return CFuncDeclaratorNode(pos, base=base, args=arguments, has_varargs=False, exception_value=None, exception_check=0, nogil=True, with_gil=False)
