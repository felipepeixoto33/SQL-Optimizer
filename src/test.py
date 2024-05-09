import re
from node import Node

def analisar_sql(query):
    # Dicionários para armazenar as partes da consulta
    elementos = {
        "Tables": [],
        "Joins": [],
        "Conditions": {},
        "Projections": {},
        "Intermediary-Projections": {}
    }

    # Regex para extrair as projeções (após SELECT e antes do FROM)
    proj_regex = re.compile(r'SELECT\s+(.*?)\s+FROM', re.IGNORECASE)
    match_proj = proj_regex.search(query)
    if match_proj:
        # Extrai projeções e as associa a tabelas específicas
        projections = match_proj.group(1).split(',')
        for proj in projections:
            proj = proj.strip()
            table_column = re.match(r'(\w+)\.(\w+)', proj)
            if table_column:
                table, column = table_column.groups()
                if table not in elementos['Projections']:
                    elementos['Projections'][table] = []
                elementos['Projections'][table].append(column)

    # Regex para extrair os nomes das tabelas principais e de junção
    table_regex = re.compile(r'FROM\s+(\w+)', re.IGNORECASE)
    join_regex = re.compile(r'JOIN\s+(\w+)', re.IGNORECASE)
    
    # Captura a tabela principal
    match_table = table_regex.search(query)
    main_table = ''
    if match_table:
        main_table = match_table.group(1)
        elementos['Tables'].append(main_table)
        elementos['Conditions'][main_table] = []
        elementos['Intermediary-Projections'][main_table] = set()
        if main_table not in elementos['Projections']:
            elementos['Projections'][main_table] = []

    # Regex para extrair as informações de JOIN (JOIN, ON)
    join_detail_regex = re.compile(r'JOIN\s+(\w+)\s+ON\s+(.*?)\s+(WHERE|JOIN|$)', re.IGNORECASE)
    for join_match in join_detail_regex.finditer(query):
        join_table = join_match.group(1)
        join_condition = join_match.group(2).strip()
        elementos['Tables'].append(join_table)
        if join_table not in elementos['Conditions']:
            elementos['Conditions'][join_table] = []
        elementos['Joins'].append({"tables": [main_table, join_table], "on": join_condition})
        # Adiciona projeções intermediárias baseadas nos joins
        on_parts = re.findall(r'(\w+)\.(\w+)', join_condition)
        for part in on_parts:
            table, column = part
            if table not in elementos['Intermediary-Projections']:
                elementos['Intermediary-Projections'][table] = set()
            elementos['Intermediary-Projections'][table].add(column)

    # Regex para extrair as condições (após WHERE até o fim da query)
    cond_regex = re.compile(r'WHERE\s+(.*)', re.IGNORECASE)
    match_cond = cond_regex.search(query)
    if match_cond:
        general_conditions = match_cond.group(1).split(' AND ')
        for condition in general_conditions:
            condition = condition.strip(';')
            parts = re.findall(r'(\w+)\.(\w+)', condition)
            if parts:
                for table, column in parts:
                    if table in elementos['Tables']:
                        elementos['Conditions'][table].append(condition)
                        elementos['Intermediary-Projections'][table].add(column)

    # Convertendo sets para listas
    for table in elementos['Intermediary-Projections']:
        elementos['Intermediary-Projections'][table] = list(elementos['Intermediary-Projections'][table])

    for k, v in elementos.items():
        print(k, v)

    print()
    for table in elementos['Projections']:
        for e in elementos['Projections'][table]:
            table_int_projs = elementos['Intermediary-Projections'][table]
            if(e not in table_int_projs):
                table_int_projs.append(e)
                

    return elementos

def define_graph_flow(dicts):
    table_nodes = {}
    temp_flow = []
    step = 1
    tables_flow = {}
    graph_flow = []

    for t in dicts['Tables']:
        table_nodes[t] = [t]

        for t_n, c in dicts['Conditions'].items():
            if(t == t_n):
                table_nodes[t].append(f"σ {c}")
                # print(t_n, c)
        for t_n, i_p in dicts['Intermediary-Projections'].items():
            if(t == t_n):
                table_nodes[t].append(f"π {i_p}")
                # print(t_n, c)

    for k, v in table_nodes.items():
        tables_flow[k] = []
        for i in v:
            node = Node(f'passo {step}', i)
            step += 1
            
            if(len(temp_flow) > 0):
                node.connect_to(temp_flow[-1])
            
            tables_flow[k].append(node)
            temp_flow.append(node)
            graph_flow.append(node)
        temp_flow = []

    for join in dicts['Joins']:
        tables = join['tables']
        expr = join['on']

        node = Node(f'passo {step}', expression=expr)
        step += 1
        
        join_tables = []

        for t_in_node in table_nodes.keys():
            if(t_in_node in tables):
                join_tables.append(t_in_node)
        
        for joined_t in join_tables:
            tables_flow[joined_t][-1].connect_to(node)

        graph_flow.append(node)

        print()

    expression = "π "
    for _i in range(len(dicts['Projections'])):
        tables = list(dicts['Projections'].keys())
        for _j in range(len(dicts['Projections'][tables[_i]])):
            values = dicts['Projections'][tables[_i]]
            expression += f"{values[_j]}, "

    expression = expression[0:len(expression)-2]

    node = Node(f'passo {step}', expression, graph_flow[-1])
    graph_flow.append(node)

    for node in graph_flow:
        print(node.get_name(), node.get_expression(), list([n.get_name()] for n in node.connected_nodes))


# Exemplo de uso
sql_query = "SELECT name, age FROM users JOIN roles ON users.role_id = roles.id WHERE age > 25 AND name = 'John';"
sql_query2 = """
SELECT Cliente.nome, pedido.idPedido, pedido.DataPedido, pedido.ValorTotalPedido
FROM Cliente JOIN pedido ON Cliente.idcliente = pedido.Cliente_idCliente
WHERE Cliente.TipoCliente_idTipoCliente = 1 AND pedido.ValorTotalPedido = 0;
"""
sql_query3 = """
Select Cliente.nome, pedido.idPedido, pedido.DataPedido, Status.descricao, pedido.ValorTotalPedido
FROM Cliente JOIN pedido on Cliente.idcliente = pedido.Cliente_idCliente
JOIN Status on Status.idstatus = Pedido.status_idstatus
where Status.descricao = 'Aberto' AND Cliente.TipoCliente_idTipoCliente = 1 AND pedido.ValorTotalPedido = 0;
"""

"""
{
        'Tables': ['users', 'roles'], 
        'Joins': [{'tables': ['users', 'roles'], 'on': 'users.role_id = roles.id'}], 
        'Conditions': {'users': ['age > 25', "name = 'John';"], 'roles': []}, 
        'Projections': ['name', 'age'], 
        'Intermediary-Projections': {'users': ['age', 'role_id', 'name'], 'roles': ['id']}
}
"""


result = analisar_sql(sql_query3)


print()

graph = define_graph_flow(result)
