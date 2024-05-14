import re
import networkx as nx
import matplotlib.pyplot as plt


def parse_sql(query):
    # Dicionário para armazenar as partes do SQL
    components = {
        'SELECT': None,
        'FROM': None,
        'JOIN': [],
        'WHERE': None
    }

    # Função auxiliar para extrair com segurança usando regex
    def safe_search(pattern, text):
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return False

    # Extrair SELECT
    components['SELECT'] = safe_search(r'SELECT\s+([\w\s\*,]+)\s+', query)
    if not components['SELECT']:
        return False, "Error parsing SELECT"

    # Extrair FROM
    components['FROM'] = safe_search(r'FROM\s+([\w\s]+?)(?:\s+WHERE|\s+JOIN|;|$)', query)
    if not components['FROM']:
        return False, "Error parsing FROM"

    # Extrair WHERE, se existir
    components['WHERE'] = safe_search(r'WHERE\s+(.*?)(?:\s+JOIN|;|$)', query)

    # Extrair JOINs
    joins = re.finditer(r'JOIN\s+([\w\s]+)\s+ON\s+([\w\s\.\=\>\<\!\(\)]+)', query, re.IGNORECASE)
    for join in joins:
        components['JOIN'].append((join.group(1).strip(), join.group(2).strip()))

    # Retorna true e os componentes se tudo estiver correto
    return True, components


def build_graph(components):
    G = nx.DiGraph()

    # Nó da tabela FROM
    from_table = components['FROM'].strip()
    G.add_node(from_table, type='table')

    # Nós e arestas para JOIN
    for join_table, condition in components['JOIN']:
        G.add_node(join_table.strip(), type='table')
        G.add_edge(from_table, join_table, label=condition)

    # Nó WHERE, se existir
    if components['WHERE']:
        G.add_node('WHERE', type='operator', condition=components['WHERE'])
        G.add_edge(from_table, 'WHERE')
        from_table = 'WHERE'  # O próximo nó se conectará ao WHERE se ele existir

    # Nós para SELECT
    select_fields = components['SELECT'].split(',')
    for field in select_fields:
        G.add_node(field.strip(), type='field')
        G.add_edge(from_table, field.strip())

    return G


def plot_graph(G):
    pos = nx.spring_layout(G)
    labels = {node: node for node in G.nodes()}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()


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
