import re

def analisar_sql(query):
    # Dicionários para armazenar as partes da consulta
    elementos = {
        "Tables": [],
        "Joins": [],
        "Conditions": {},
        "Projections": {},
        "Intermediate-Projections": {}
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
        elementos['Intermediate-Projections'][main_table] = set()
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
            if table not in elementos['Intermediate-Projections']:
                elementos['Intermediate-Projections'][table] = set()
            elementos['Intermediate-Projections'][table].add(column)

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
                        elementos['Intermediate-Projections'][table].add(column)

    # Convertendo sets para listas
    for table in elementos['Intermediate-Projections']:
        elementos['Intermediate-Projections'][table] = list(elementos['Intermediate-Projections'][table])

    for table in elementos['Projections']:
        for e in elementos['Projections'][table]:
            table_int_projs = elementos['Intermediate-Projections'][table]
            if(e not in table_int_projs):
                table_int_projs.append(e)
                

    return elementos

# Exemplo de uso
sql_query2 = """
Select Cliente.nome, pedido.idPedido, pedido.DataPedido, pedido.ValorTotalPedido
from Cliente Join pedido on Cliente.idcliente = pedido.Cliente_idCliente
where Cliente.TipoCliente_idTipoCliente = 1 and pedido.ValorTotalPedido = 0;
"""
result = analisar_sql(sql_query2)

for k,v in result.items():
    print(k, v)