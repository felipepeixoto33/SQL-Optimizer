class Node():
    def __init__(self, name: str, expression: str, connected_to = None):
        self.name = name
        self.expression = expression
        self.connected_to = connected_to

    def connect_to(self, node):
        self.connected_to = node

    def get_expression(self):
        return self.expression

    def get_name(self):
        return self.name

    def get_connected_node(self):
        return self.connected_to
