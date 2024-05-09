class Node():
    def __init__(self, name: str, expression: str, connected_to = None):
        self.name = name
        self.expression = expression
<<<<<<< HEAD
        self.connected_nodes = [connected_to] if connected_to else []

    def connect_to(self, node):
        if(node not in self.connected_nodes):
            self.connected_nodes.append(node)
        if(self not in node.connected_nodes):
            node.connect_to(self)
=======
        self.connected_to = connected_to

    def connect_to(self, node):
        self.connected_to = node
>>>>>>> bc937eae1bf4d6800896165023b3a106fad35f1e

    def get_expression(self):
        return self.expression

    def get_name(self):
        return self.name

    def get_connected_node(self):
        return self.connected_to
