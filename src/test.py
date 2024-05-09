import re
from node import Node

def analisar_sql(query):
    # Dicionários para armazenar as partes da consulta
    elementos = {
        "Tables": [],
        "Joins": [],
        "Conditions": {},
        "Projections": [],
        "Intermediary-Projections": {}
    }

    # Regex para extrair as projeções (após SELECT e antes do FROM)
    proj_regex = re.compile(r'SELECT\s+(.*?)\s+FROM', re.IGNORECASE)
    match_proj = proj_regex.search(query)
    if match_proj:
        elementos['Projections'] = [proj.strip() for proj in match_proj.group(1).split(',')]

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
            parts = re.findall(r'(\w+)\.(\w+)', condition)
            if parts:
                for table, column in parts:
                    elementos['Conditions'][table].append(condition.strip())
                    elementos['Intermediary-Projections'][table].add(column)
            else:
                # Se não encontramos tabela explicitamente mencionada, assumimos a principal
                column = re.search(r'(\w+)', condition).group(1)
                elementos['Conditions'][main_table].append(condition.strip())
                elementos['Intermediary-Projections'][main_table].add(column)

    # Convertendo sets para listas
    for table in elementos['Intermediary-Projections']:
        elementos['Intermediary-Projections'][table] = list(elementos['Intermediary-Projections'][table])

    return elementos

# Exemplo de uso
sql_query = "SELECT name, age FROM users JOIN roles ON users.role_id = roles.id WHERE age > 25 AND name = 'John';"
result = analisar_sql(sql_query)
print(result)
print()


"""
{
        'Tables': ['users', 'roles'], 
        'Joins': [{'tables': ['users', 'roles'], 'on': 'users.role_id = roles.id'}], 
        'Conditions': {'users': ['age > 25', "name = 'John';"], 'roles': []}, 
        'Projections': ['name', 'age'], 
        'Intermediary-Projections': {'users': ['age', 'role_id', 'name'], 'roles': ['id']}
}
"""

def define_graph_flow(dicts):
    table_nodes = {}
    temp_flow = []
<<<<<<< HEAD
    step = 1
    tables_flow = {}
=======
>>>>>>> bc937eae1bf4d6800896165023b3a106fad35f1e
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
<<<<<<< HEAD
        tables_flow[k] = []
        for i in v:
            node = Node(f'passo {step}', i)
            step += 1
=======
        for i in v:
            node = Node('passo', i)
>>>>>>> bc937eae1bf4d6800896165023b3a106fad35f1e
            
            if(len(temp_flow) > 0):
                node.connect_to(temp_flow[-1])
            
<<<<<<< HEAD
            tables_flow[k].append(node)
=======
>>>>>>> bc937eae1bf4d6800896165023b3a106fad35f1e
            temp_flow.append(node)
            graph_flow.append(node)
        temp_flow = []

    for join in dicts['Joins']:
        tables = join['tables']
        expr = join['on']
<<<<<<< HEAD

        node = Node(f'passo {step}', expression=expr)
        step += 1
=======
>>>>>>> bc937eae1bf4d6800896165023b3a106fad35f1e
        
        join_tables = []

        for t_in_node in table_nodes.keys():
            if(t_in_node in tables):
                join_tables.append(t_in_node)
        
<<<<<<< HEAD
        for joined_t in join_tables:
            tables_flow[joined_t][-1].connect_to(node)

        graph_flow.append(node)

        print()
        expression = "π_"
        for _i in range(len(dicts['Projections'])):
            if(_i == len(dicts['Projections'])-1):
                expression += f"{dicts['Projections'][_i]}"
                break

            expression += f"{dicts['Projections'][_i]}, "

        expression += f"({dicts['Tables'][0]})"

        node = Node(f'passo {step}', expression, graph_flow[-1])
        graph_flow.append(node)

        for node in graph_flow:
            print(node.get_name(), node.get_expression(), list([n.get_name()] for n in node.connected_nodes))

            
=======
        for node in graph_flow:
            print(node.get_name(), node.get_expression(), node.connected_to)

>>>>>>> bc937eae1bf4d6800896165023b3a106fad35f1e
graph = define_graph_flow(result)
