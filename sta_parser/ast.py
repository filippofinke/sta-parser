"""
AST for the SensorThings API.

Author: Filippo Finke
"""

class ASTNode:
    pass

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return f"Identifier({self.name})"


class SelectNode(ASTNode):
    def __init__(self, identifiers):
        self.identifiers = identifiers

    def __str__(self) -> str:
        return f"Select({', '.join(str(identifier) for identifier in self.identifiers)})"


class FilterNode(ASTNode):
    def __init__(self, filter):
        self.filter = filter

    def __str__(self) -> str:
        return f"Filter({self.filter})"

class ExpandNodeIdentifier(ASTNode):
    def __init__(self, identifier, subquery=None):
        self.identifier = identifier
        self.subquery = subquery

    def __str__(self) -> str:
        return f"ExpandNodeIdentifier({self.identifier}, {self.subquery})"

class ExpandNode(ASTNode):
    def __init__(self, identifiers):
        self.identifiers = identifiers

    def __str__(self) -> str:
        return f"Expand({', '.join(str(identifier) for identifier in self.identifiers)})"


class OrderByNodeIdentifier(ASTNode):
    def __init__(self, identifier, order):
        self.identifier = identifier
        self.order = order

    def __str__(self) -> str:
        return f"OrderByNodeIdentifier({self.identifier}, {self.order})"


class OrderByNode(ASTNode):
    def __init__(self, identifiers):
        self.identifiers = identifiers

    def __str__(self) -> str:
        return f"OrderBy({', '.join(str(identifier) for identifier in self.identifiers)})"


class SkipNode(ASTNode):
    def __init__(self, count):
        self.count = count

    def __str__(self) -> str:
        return f"Skip({self.count})"


class TopNode(ASTNode):
    def __init__(self, count):
        self.count = count

    def __str__(self) -> str:
        return f"Top({self.count})"


class CountNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"Count({self.value})"


class QueryNode(ASTNode):
    def __init__(self, select=None, filter=None, expand=None, orderby=None, skip=None, top=None, count=None):
        self.select = select
        self.filter = filter
        self.expand = expand
        self.orderby = orderby
        self.skip = skip
        self.top = top
        self.count = count

    def __str__(self) -> str:
        return f"Query({self.select}, {self.filter}, {self.expand}, {self.orderby}, {self.skip}, {self.top}, {self.count})"