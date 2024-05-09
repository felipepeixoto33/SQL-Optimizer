def montar_grafo(dados):
    grafo = {}
    last_node = "root"

    # Projeção final conforme as Projections principais
    proj_final = ", ".join(dados['Projections'])
    last_node = criar_no(grafo, f"π {proj_final}", last_node)

    # Se existem Joins, processar cada um
    if dados['Joins']:
        for join in reversed(dados['Joins']):
            on_clause = join['on']
            join_desc = f"⨝ {on_clause}"
            last_node = criar_no(grafo, join_desc, last_node)
            # Processa cada tabela na join
            for table in join['tables']:
                intermediate_proj = ", ".join(dados['Intermediate-Projections'][table])
                intermediate_node = criar_no(grafo, f"π {intermediate_proj}", last_node)
                if dados['Conditions'][table]:
                    condition = " ^ ".join(dados['Conditions'][table])
                    intermediate_node = criar_no(grafo, f"σ {condition}", intermediate_node)
                grafo[f"Node-{intermediate_node}"].append(table)
    else:
        # Sem joins, processar diretamente as tabelas
        for table in dados['Tables']:
            if dados['Conditions'][table]:
                condition = " ^ ".join(dados['Conditions'][table])
                last_node = criar_no(grafo, f"σ {condition}", last_node)
            intermediate_proj = ", ".join(dados['Intermediate-Projections'][table])
            last_node = criar_no(grafo, f"π {intermediate_proj}", last_node)
            grafo[f"Node-{last_node}"].append(table)

    return grafo

def criar_no(grafo, descricao, proximo_no):
    node_id = len(grafo) + 1
    grafo[f"Node-{node_id}"] = [descricao, proximo_no]
    return node_id

# Exemplo de dados de entrada
dados = {
    'Tables': ['users', 'roles'],
    'Joins': [{'tables': ['users', 'roles'], 'on': 'users.role_id = roles.id'}],
    'Conditions': {'users': ['age > 25', "name = 'John'"], 'roles': []},
    'Projections': ['name', 'age'],
    'Intermediate-Projections': {'users': ['age', 'role_id', 'name'], 'roles': ['id']}
}

# Gerar o grafo
grafo = montar_grafo(dados)
print(grafo)


"""

{
        'Node-1': ['π name, age', 'root'], 
        'Node-2': ['⨝ users.role_id = roles.id', 1], 
        'Node-3': ['π age, role_id, name', 2], 
        'Node-4': ["σ age > 25 ^ name = 'John'", 3, 'users'], 
        'Node-5': ['π id', 2, 'roles']
}


{
    "Node-1":["Users", "Node-2"],
    "Node-2":["σ age > 25 ^ "name = John", "Node-3"]
    "Node-3":["π name, age, role_id", "Node-6"]
    "Node-4":["roles", "Node-5"]
    "Node-5":["π id", "Node-6"]
    "Node-6":["⨝ users.role_id = roles.id", "Node-7"]
    "Node-7":["π name, age", "root"] 
}

"""


