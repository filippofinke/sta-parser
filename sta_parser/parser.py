"""
Parser for the SensorThings API query language.

Author: Filippo Finke
"""

from sta_parser.lexer import Lexer
import sta_parser.ast as ast

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None

    def match(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.next_token()
        else:
            raise Exception(f"Expected '{token_type}', but found '{self.current_token.type}' ('{self.current_token.value}')")

    def check_token(self, token_type):
        return self.current_token and self.current_token.type == token_type

    def parse_identifier_list(self):
        identifiers = []
        identifiers.append(ast.IdentifierNode(self.current_token.value))
        self.match('IDENTIFIER')
        while self.current_token.type == 'VALUE_SEPARATOR':
            self.match('VALUE_SEPARATOR')
            identifiers.append(ast.IdentifierNode(self.current_token.value))
            self.match('IDENTIFIER')
        return identifiers

    def parse_filter(self):
        self.match('FILTER')
        filter = ""
        
        while not self.check_token('OPTIONS_SEPARATOR') and not self.check_token('RIGHT_PAREN') and self.current_token != None:
            filter += self.current_token.value
            self.next_token()

        return ast.FilterNode(filter)

    def parse_expand(self):
        self.match('EXPAND')

        identifiers = []
        while self.current_token.type != 'OPTIONS_SEPARATOR':
            identifier = ast.ExpandNodeIdentifier(self.current_token.value)
            self.match('IDENTIFIER')

            # Check if there is a subquery
            if self.check_token('LEFT_PAREN'):
                identifier.subquery = self.parse_subquery()
            
            identifiers.append(identifier)

            # Check if there is another option
            if self.check_token('VALUE_SEPARATOR'):
                self.match('VALUE_SEPARATOR')
            else:
                break

        return ast.ExpandNode(identifiers)
    
    def parse_select(self):
        self.match('SELECT')
        identifiers = self.parse_identifier_list()
        return ast.SelectNode(identifiers)

    def parse_orderby(self):
        self.match('ORDERBY')
        # match identifiers separated by commas and check if there is a space and order
        identifiers = []
        while True:
            identifier = self.current_token.value
            self.match('IDENTIFIER')
            order = 'asc'
            if self.check_token('WHITESPACE'):
                self.match('WHITESPACE')
                order = self.current_token.value
                self.match('ORDER')

            identifiers.append(ast.OrderByNodeIdentifier(identifier, order))

            if not self.check_token('VALUE_SEPARATOR'):
                break

            self.match('VALUE_SEPARATOR')

        return ast.OrderByNode(identifiers)

    def parse_skip(self):
        self.match('SKIP')
        count = int(self.current_token.value)
        self.match('INTEGER')
        return ast.SkipNode(count)

    def parse_top(self):
        self.match('TOP')
        if self.check_token("INTEGER"):
            count = int(self.current_token.value)
            self.match('INTEGER')
            return ast.TopNode(count)
        else:
            raise Exception(f"Expected integer, but found '{self.current_token.type}' ('{self.current_token.value}')")

    def parse_count(self):
        self.match('COUNT')
        value = self.current_token.value.lower() == 'true'
        self.match('BOOL')
        return ast.CountNode(value)
    
    def parse_subquery(self):
        self.match('LEFT_PAREN')
        select = None
        filter = None
        expand = None
        orderby = None
        skip = None
        top = None
        count = None

        # continue parsing until we reach the end of the query
        while True:
            if self.current_token.type == 'SELECT':
                select = self.parse_select()
            elif self.current_token.type == 'FILTER':
                filter = self.parse_filter()
            elif self.current_token.type == 'EXPAND':
                expand = self.parse_expand()
            elif self.current_token.type == 'ORDERBY':
                orderby = self.parse_orderby()
            elif self.current_token.type == 'SKIP':
                skip = self.parse_skip()
            elif self.current_token.type == 'TOP':
                top = self.parse_top()
            elif self.current_token.type == 'COUNT':
                count = self.parse_count()
            else:
                raise Exception(f"Unexpected token: {self.current_token.type}")
            
            # check for other options
            if self.check_token('SUBQUERY_SEPARATOR'):
                self.match('SUBQUERY_SEPARATOR')
            else:
                break
        
        self.match('RIGHT_PAREN')

        return ast.QueryNode(select, filter, expand, orderby, skip, top, count, True)

    def parse_query(self):
        select = None
        filter = None
        expand = None
        orderby = None
        skip = None
        top = None
        count = None

        # continue parsing until we reach the end of the query
        while self.current_token != None:
            if self.current_token.type == 'SELECT':
                select = self.parse_select()
            elif self.current_token.type == 'FILTER':
                filter = self.parse_filter()
            elif self.current_token.type == 'EXPAND':
                expand = self.parse_expand()
            elif self.current_token.type == 'ORDERBY':
                orderby = self.parse_orderby()
            elif self.current_token.type == 'SKIP':
                skip = self.parse_skip()
            elif self.current_token.type == 'TOP':
                top = self.parse_top()
            elif self.current_token.type == 'COUNT':
                count = self.parse_count()
            else:
                raise Exception(f"Unexpected token: {self.current_token.type}")
            
            if self.current_token != None:
                self.match('OPTIONS_SEPARATOR')

        return ast.QueryNode(select, filter, expand, orderby, skip, top, count)

    def parse(self):
        return self.parse_query()

# Example usage
if __name__ == '__main__':
    text = '''$select=id,name,description,properties&$top=1000&$filter=properties/type eq 'station'&$expand=Locations,Datastreams($select=id,name,unitOfMeasurement;$expand=ObservedProperty($select=name),Observations($select=result,phenomenonTime;$orderby=phenomenonTime desc;$top=1))'''
    lexer = Lexer(text)
    tokens = lexer.tokens

    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
