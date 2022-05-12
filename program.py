
import random
import subprocess
import timeit
from Cython.Compiler.TreeFragment import *
from Cython.Compiler.Visitor import *
from Cython.Compiler.Main import *
from Cython.Compiler.Pipeline import *
from Cython.CodeWriter import *
from Cython.Compiler.AnalysedTreeTransforms import *
from Cython.Compiler.ParseTreeTransforms import *
from Cython.Compiler.Symtab import *
from black import out
import utilities.cython_tree as cy
from utilities.cython_visitor import MyVisitor, NodeVisitor
import time
import importlib


class Program:
    file_path = ""

    def __init__(self, file_path, test_path):
        self.file_path = file_path
        self.test_path = test_path
        self.contents = cy.file_to_ast(self.file_path)
        self.modification_points = cy.get_modification_points(self.contents)

    def get_modified_contents(self, patch):
        modification_points = copy.deepcopy(self.modification_points)
        new_contents = copy.deepcopy(self.contents)
        edits = patch.edit_list
        for edit in edits:
            edit.apply(new_contents, modification_points)
        return new_contents

    def apply(self, patch):
        """
        This method applies the patch to the target program.
        It does not directly modify the source code of the original program,
        but modifies the copied program within the temporary directory.
        """
        new_contents = self.get_modified_contents(patch)
        self.write_to_tmp_dir(new_contents)
        return new_contents

    def evaluate_patch(self, patch):
        result_type = ["compilation_fail",
                       "bug_found", "wrong_value"]
        result = {"status": None, "value": None}
        # apply & run
        self.apply(patch)
        output = self.exec_cmd().strip()
        print(output)

        if output in result_type:
            result["status"] = output
            return result

        result["status"] = "success"
        result["value"] = output

        return result

    def load_contents(self):
        self.contents = {}
        self.modification_points = dict()
        for file_name in self.target_files:
            self.contents[file_name] = cy.get_contents(file_name)
            self.modification_points[file_name] = cy.get_modification_points(
                self.contents[file_name])

    def exec_cmd(self):
        process = subprocess.Popen(['python', self.test_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        return stdout

    def dump(self, content, name):
        writer = CodeWriter()
        writer.visit(content[name])
        source = "\n".join(writer.result.lines)
        return source

    def random_target(self):
        """
        :param str target_file: The modification point is chosen within target_file
        :return: The **index** of modification point
        :rtype: int
        """
        candidates = self.modification_points
        return random.randrange(len(candidates))

    def write_to_tmp_dir(cls, contents):
        with open("output/temp.pyx", 'w') as tmp_file:
            tmp_file.write(cy.ast_to_source(contents))

    def write_result(self, patch):
        contents = self.get_modified_contents(patch)
        with open("output/result.pyx", 'w') as result_file:
            result_file.write(cy.ast_to_source(contents))
