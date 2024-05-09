class Node():
    def __init__(self, name: str, expression: str, connected_to = None):
        self.name = name
        self.expression = expression
        self.connected_nodes = []
        
        if(connected_to):
            self.connect_to(connected_to)

    def connect_to(self, node):
        if(node not in self.connected_nodes):
            self.connected_nodes.append(node)
        if(self not in node.connected_nodes):
            node.connect_to(self)

    def get_expression(self):
        return self.expression

    def get_name(self):
        return self.name

    def get_connected_node(self):
        return self.connected_to
