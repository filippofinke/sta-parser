from sta_parser.lexer import Lexer
from sta_parser.visitor import Visitor
from sta_parser.parser import Parser
from sta_parser import ast

class NodeVisitor(Visitor):
    def visit_IdentifierNode(self, node: ast.IdentifierNode):
        return node.name

    def visit_SelectNode(self, node: ast.SelectNode):
        identifiers = ','.join([self.visit(identifier) for identifier in node.identifiers])
        return f'$select={identifiers}'

    def visit_FilterNode(self, node: ast.FilterNode):
        return f'$filter={node.filter}'

    def visit_ExpandNodeIdentifier(self, node: ast.ExpandNodeIdentifier):
        identifier = node.identifier
        if node.subquery:
            subquery = self.visit(node.subquery)
            return f'{identifier}({subquery})'
        else:
            return identifier

    def visit_ExpandNode(self, node: ast.ExpandNode):
        identifiers = ','.join([self.visit(identifier) for identifier in node.identifiers])
        return f'$expand={identifiers}'

    def visit_OrderByNodeIdentifier(self, node: ast.OrderByNodeIdentifier):
        return f'{node.identifier} {node.order}'

    def visit_OrderByNode(self, node: ast.OrderByNode):
        identifiers = ','.join([self.visit(identifier) for identifier in node.identifiers])
        return f'$orderby={identifiers}'

    def visit_SkipNode(self, node: ast.SkipNode):
        return f'$skip={node.count}'

    def visit_TopNode(self, node: ast.TopNode):
        return f'$top={node.count}'

    def visit_CountNode(self, node: ast.CountNode):
        return f'$count={node.value}'

    def visit_QueryNode(self, node: ast.QueryNode):
        query_parts = []
        if node.select:
            query_parts.append(self.visit(node.select))
        if node.filter:
            query_parts.append(self.visit(node.filter))
        if node.expand:
            query_parts.append(self.visit(node.expand))
        if node.orderby:
            query_parts.append(self.visit(node.orderby))
        if node.skip:
            query_parts.append(self.visit(node.skip))
        if node.top:
            query_parts.append(self.visit(node.top))
        if node.count:
            query_parts.append(self.visit(node.count))
            
        if node.is_subquery:
            return ';'.join(query_parts)
        return '&'.join(query_parts)

if __name__ == '__main__':
    text = '''$select=id,name,description,properties&$top=1000&$filter=properties/type eq 'station'&$expand=Locations,Datastreams($select=id,name,unitOfMeasurement;$expand=ObservedProperty($select=name),Observations($select=result,phenomenonTime;$orderby=phenomenonTime desc;$top=1))'''
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    visitor = NodeVisitor()
    result = visitor.visit(ast)    
    print(result)