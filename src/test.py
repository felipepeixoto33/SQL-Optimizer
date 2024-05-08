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

    graph_flow = {}

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
        print(f"#{k}:")
        for i in v:
            print(i)
        print()

    for join in dicts['Joins']:
        tables = join['tables']
        expr = join['on']
        
        join_tables = []

        for t_in_node in table_nodes.keys():
            if(t_in_node in tables):
                join_tables.append(t_in_node)
        
        

graph = define_graph_flow(result)
