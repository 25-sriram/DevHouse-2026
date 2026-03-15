import ast
import logging
import json

logger = logging.getLogger(__name__)

class ASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.structure = {
            "classes": [],
            "functions": [],
            "imports": [],
            "calls": []
        }

    def visit_ClassDef(self, node):
        self.structure["classes"].append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.structure["functions"].append(node.name)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.structure["imports"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        for alias in node.names:
            self.structure["imports"].append(f"{module}.{alias.name}")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Handle simple calls like func()
        if isinstance(node.func, ast.Name):
            self.structure["calls"].append(node.func.id)
        # Handle attribute calls like obj.method()
        elif isinstance(node.func, ast.Attribute):
            self.structure["calls"].append(node.func.attr)
        self.generic_visit(node)

class ASTParser:
    @staticmethod
    def parse_file(file_path):
        """Parses a Python file and returns its code structure."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            
            tree = ast.parse(source)
            visitor = ASTVisitor()
            visitor.visit(tree)
            return visitor.structure
        except Exception as e:
            logger.error(f"Failed to parse AST for {file_path}: {e}")
            return None
