"""
AST for the SensorThings API.

Author: Filippo Finke
"""

class PrettyPrinter(object):
    def __str__(self):
        lines = []
        for key, val in vars(self).items():
            if val is None:
                continue

            if isinstance(val, list):
                lines += ['\n  {}:'.format(key)]
                for item in val:
                    lines += ['   {}'.format(line) for line in str(item).split('\n')]
            else:
                lines += '{}: {}'.format(key, val).split('\n')            
        return '\n'.join(lines)

class Node(PrettyPrinter):
    pass

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

class SelectNode(Node):
    def __init__(self, identifiers):
        self.identifiers = identifiers


class FilterNode(Node):
    def __init__(self, filter):
        self.filter = filter


class ExpandNodeIdentifier(Node):
    def __init__(self, identifier, subquery=None):
        self.identifier = identifier
        self.subquery = subquery


class ExpandNode(Node):
    def __init__(self, identifiers):
        self.identifiers = identifiers

class OrderByNodeIdentifier(Node):
    def __init__(self, identifier, order):
        self.identifier = identifier
        self.order = order

class OrderByNode(Node):
    def __init__(self, identifiers):
        self.identifiers = identifiers

class SkipNode(Node):
    def __init__(self, count):
        self.count = count

class TopNode(Node):
    def __init__(self, count):
        self.count = count

class CountNode(Node):
    def __init__(self, value):
        self.value = value

class QueryNode(Node):
    def __init__(self, select=None, filter=None, expand=None, orderby=None, skip=None, top=None, count=None, is_subquery=False):
        self.select = select
        self.filter = filter
        self.expand = expand
        self.orderby = orderby
        self.skip = skip
        self.top = top
        self.count = count
        self.is_subquery = is_subquery