import re
import networkx as nx
import plotly.graph_objects as go


def parse_sql(query):
    components = {
        'SELECT': None,
        'FROM': None,
        'JOIN': [],
        'WHERE': None
    }

    def safe_search(pattern, text):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return False

    components['SELECT'] = safe_search(r'SELECT\s+([\w\s\*,]+)\s+', query)
    if not components['SELECT']:
        return False, "Error parsing SELECT"

    components['FROM'] = safe_search(r'FROM\s+([\w\s]+?)(?:\s+WHERE|\s+JOIN|;|$)', query)
    if not components['FROM']:
        return False, "Error parsing FROM"

    components['WHERE'] = safe_search(r'WHERE\s+(.*?)(?:\s+JOIN|;|$)', query)

    joins = re.finditer(r'JOIN\s+([\w\s]+)\s+ON\s+([\w\s\.\=\>\<\!\(\)]+)', query, re.IGNORECASE)
    for join in joins:
        components['JOIN'].append((join.group(1).strip(), join.group(2).strip()))

    return True, components


def build_graph(components):
    G = nx.DiGraph()

    from_table = components['FROM'].strip()
    G.add_node(from_table, type='table')

    for join_table, condition in components['JOIN']:
        G.add_node(join_table.strip(), type='table')
        G.add_edge(from_table, join_table, label=condition)

    if components['WHERE']:
        G.add_node('WHERE', type='operator', condition=components['WHERE'])
        G.add_edge(from_table, 'WHERE')
        from_table = 'WHERE'

    select_fields = components['SELECT'].split(',')
    for field in select_fields:
        G.add_node(field.strip(), type='field')
        G.add_edge(from_table, field.strip())

    return G


def plot_graph(G):
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='blue',
            size=10,
            line_width=2),
        text=text,
        textposition="top center")

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()


# Exemplo de uso
sql_query = """
SELECT name, age FROM users
JOIN roles ON users.role_id = roles.id
WHERE age > 25 AND (name = 'John' OR name = 'Jane');
"""

result, parsed_sql_or_error = parse_sql(sql_query)
if result:
    print("Parsing successful:", parsed_sql_or_error)
    G = build_graph(parsed_sql_or_error)
    plot_graph(G)
else:
    print("Parsing failed:", parsed_sql_or_error)
