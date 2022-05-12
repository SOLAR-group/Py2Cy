from ast import Expr
from turtle import position
from typing import Tuple
from Cython.Compiler.Nodes import *
from Cython.Compiler.ModuleNode import *
from Cython.Compiler.ExprNodes import *
from Cython.Compiler.AnalysedTreeTransforms import *
from Cython.Compiler.ParseTreeTransforms import *
from edit_types import *
from Cython.CodeWriter import *
from Cython.Compiler.TreeFragment import *
from Cython.Compiler.Pipeline import *
from Cython.Compiler.Visitor import *


class MyVisitor(EnvTransform):
    target_pos = None
    c_type = None

    def __call__(self, root):
        self.env_stack = []
        self.enter_scope(root, root.scope)
        return super(EnvTransform, self).__call__(root)

    def visit_ModuleNode(self, node):
        self.visitchildren(node)
        return node

    def visit_DefNode(self, node):
        # Insert C type declaration for functions
        if node.pos == self.target_pos:
            position = node.pos
            test_type = get_type(position, self.edit_type)
            base = get_name_declarator(position, node.name, None)
            declarator = get_func_declarator(position, base, node.args)

            new_node = CFuncDefNode(position, visibility='private', base_type=test_type,
                                    declarator=declarator, body=node.body, modifiers=[], api=False, overridable=False)
            return new_node

        self.visitchildren(node)
        return node

    def visit_SingleAssignmentNode(self, node):
        # Insert C type declaration for expressions
        if node.pos == self.target_pos:
            if isinstance(node.lhs, ExprNodes.NameNode):
                position = node.pos
                type_node = get_type(position, self.edit_type)
                base = get_name_declarator(position, node.lhs.name, node.rhs)
                new_node = CVarDefNode(
                    position, visibility='private', base_type=type_node, declarators=[base])
                new_node.child
                self.visitchildren(node)
                return new_node
        self.visitchildren(node)
        return node

    def visit_ExprStatNode(self, node):
        # Insert C type declaration for unassigned variable
        if node.pos == self.target_pos:
            position = node.pos
            type_node = get_type(position, self.edit_type)
            base = get_name_declarator(position, node.expr.name, None)
            new_node = CVarDefNode(
                position, visibility='private', base_type=type_node, declarators=[base])

            self.visitchildren(node)
            return new_node
        return node

    def visit_CArgDeclNode(self, node):
        # Insert C type declarations for function arguments
        if node.pos == self.target_pos:
            position = node.pos
            type_node = get_type(position, self.edit_type)
            node.base_type = type_node
            self.visitchildren(node)
        return node


class NodeVisitor(CythonTransform):
    positions = []

    # Add positions of lines that require types: Tuple (Description, line, col)

    def __call__(self, root):
        self.env_stack = []
        self.enter_scope(root, root.scope)
        return super(EnvTransform, self).__call__(root)

    def visit_CSimpleBaseTypeNode(self, node):
        self.positions.append(node.pos)
        self.visitchildren(node)
        return node


class TypeInsertionVisitor(CythonTransform):

    target_pos = None
    c_type = None

    def visit_CSimpleBaseTypeNode(self, node):
        if node.pos == self.target_pos:
            node.name = self.c_type

        return node


class DeclarationVisitor(EnvTransform):
    declarations = []

    def __call__(self, root):
        self.env_stack = []
        self.enter_scope(root, root.scope)
        return super(EnvTransform, self).__call__(root)

    def visit_ModuleNode(self, node):
        stat_node = getattr(node, 'body')
        visitor = VariableVisitor(None)
        for stat in stat_node.stats:
            if not isinstance(stat, DefNode):
                visitor.visit(stat)
        variables = list(visitor.names)
        # Reset
        VariableVisitor.names = set()
        for v in variables:
            untyped = CSimpleBaseTypeNode(node.pos, name=None, module_path=[
            ], is_basic_c_type=True, signed=1, longness=0, is_self_arg=False)
            name = CNameDeclaratorNode(node.pos, name=v, cname=v, default=None)
            new_declaration = CVarDefNode(
                node.pos, visibility='private', base_type=untyped, declarators=[name])
            getattr(node, 'body').stats.insert(0, new_declaration)

        self.visitchildren(node)
        return node

    def visit_DefNode(self, node):
        stat_node = getattr(node, 'body')
        visitor = VariableVisitor(None)
        for stat in stat_node.stats:
            if not isinstance(stat, DefNode):
                visitor.visit(stat)

        variables = list(visitor.names)
        # Reset
        VariableVisitor.names = set()

        for v in variables:
            untyped = CSimpleBaseTypeNode(node.pos, name=None, module_path=[
            ], is_basic_c_type=True, signed=1, longness=0, is_self_arg=False)
            name = CNameDeclaratorNode(node.pos, name=v, cname=v, default=None)
            new_declaration = CVarDefNode(
                node.pos, visibility='private', base_type=untyped, declarators=[name])
            getattr(node, 'body').stats.insert(0, new_declaration)
        self.visitchildren(node)
        return node


class VariableVisitor(EnvTransform):
    names = set()

    def __call__(self, root):
        self.env_stack = []
        self.enter_scope(root, root.scope)
        return super(EnvTransform, self).__call__(root)

    def visit_SingleAssignmentNode(self, node):
        if isinstance(node.lhs, NameNode):
            self.names.add(node.lhs.name)
        elif isinstance(node.lhs, TupleNode):
            for item in node.lhs.args:
                self.names.add(item.name)
        return node

    def visit_ForInStatNode(self, node):
        self.names.add(node.target.name)
        return node


class WriterVisitor(CodeWriter):

    def visit_CVarDefNode(self, node):
        self.startline(u"cdef ")
        self.visit(node.base_type)
        if node.base_type != None:
            self.put(u" ")
        self.comma_separated_list(node.declarators, output_rhs=False)
        self.endline()

    def visit_CSimpleBaseTypeNode(self, node):
        # See Parsing.p_sign_and_longness
        if node.is_basic_c_type:
            self.put(("unsigned ", "", "signed ")[node.signed])
            if node.longness < 0:
                self.put("short " * -node.longness)
            elif node.longness > 0:
                self.put("long " * node.longness)
        if node.name is not None:
            self.put(node.name)
