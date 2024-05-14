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

    # Captura todas as tabelas mencionadas
    tables = set()
    table_regex = re.compile(r'FROM\s+(\w+)', re.IGNORECASE)
    join_regex = re.compile(r'JOIN\s+(\w+)', re.IGNORECASE)

    # Captura a tabela principal
    match_table = table_regex.search(query)
    if match_table:
        main_table = match_table.group(1)
        tables.add(main_table)

    # Captura todas as tabelas de junção
    join_matches = join_regex.findall(query)
    tables.update(join_matches)

    elementos['Tables'] = list(tables)
    for table in tables:
        elementos['Conditions'][table] = []
        elementos['Intermediate-Projections'][table] = set()

    # Regex para extrair detalhes de cada JOIN (JOIN, ON)
    join_detail_regex = re.compile(r'JOIN\s+(\w+)\s+ON\s+(.*?)\s+(?=JOIN|WHERE|$)', re.IGNORECASE | re.DOTALL)
    for join_match in join_detail_regex.finditer(query):
        join_table = join_match.group(1)
        join_condition = join_match.group(2).strip()
        # Identifica a tabela de onde a junção parte
        join_from = re.search(r'(\w+)\.', join_condition).group(1)
        elementos['Joins'].append({"tables": [join_from, join_table], "on": join_condition})
        # Adiciona projeções intermediárias baseadas nos joins
        on_parts = re.findall(r'(\w+)\.(\w+)', join_condition)
        for part in on_parts:
            table, column = part
            elementos['Intermediate-Projections'][table].add(column)

    # Regex para extrair as condições (após WHERE até o fim da query)
    cond_regex = re.compile(r'WHERE\s+(.*)', re.IGNORECASE)
    match_cond = cond_regex.search(query)
    if match_cond:
        general_conditions = match_cond.group(1).split(' AND ')
        for condition in general_conditions:
            condition = condition.strip(';')
            parts = re.findall(r'(\w+)\.(\w+)', condition)
            for table, column in parts:
                if table in tables:
                    elementos['Conditions'][table].append(condition)
                    elementos['Intermediate-Projections'][table].add(column)

    # Convertendo sets para listas
    for table in elementos['Intermediate-Projections']:
        elementos['Intermediate-Projections'][table] = list(elementos['Intermediate-Projections'][table])

    return elementos


# Exemplo de uso
sql_query3 = """
Select Cliente.nome, pedido.idPedido, pedido.DataPedido, Status.descricao, pedido.ValorTotalPedido
FROM Cliente JOIN pedido on Cliente.idcliente = pedido.Cliente_idCliente
JOIN Status on Status.idstatus = pedido.status_idstatus
where Status.descricao = 'Aberto' AND Cliente.TipoCliente_idTipoCliente = 1 AND pedido.ValorTotalPedido = 0;
"""
result = analisar_sql(sql_query3)


for k, v in result.items():
    print(k, v)
