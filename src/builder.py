import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
from interpreter import Interpreter

class Builder():
    def __init__(self, sql):
        self.sql = sql
        self.expressions = ["Select", "From", "Where", "Join", "On"]
    
    def show_sql_as_graph(self):
        fig = go.Figure()
    
    def get_num_vertices(self):
        vertices = 0
        sql_terms = Interpreter.separate_sql_by_terms()
        for t in sql_terms:
            if t in self.expressions:
                vertices += 1
        return vertices