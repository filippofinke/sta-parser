"""
Visitor for the SensorThings API.

Author: Filippo Finke
"""
import sta_parser.ast as ast


class Visitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        # get all the fields of the node
        for field_name, field_value in vars(node).items():
            # if the field is a list of nodes
            if isinstance(field_value, list):
                # visit all the nodes in the list
                for item in field_value:
                    if isinstance(item, ast.Node):
                        self.visit(item)
            # if the field is a node
            elif isinstance(field_value, ast.Node):
                # visit the node
                self.visit(field_value)