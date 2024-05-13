from interpreter import Interpreter
import re

def read_file(file_path: str):
    with open(file_path, 'r') as f:
        return f.readlines() if f != None else None


def parse_relational_algebra(expression):
    # Dicionários para armazenar os componentes
    tables = set()
    joins = []
    conditions = {}
    projections = []

    # Expressões regulares para identificar componentes
    join_pattern = re.compile(r"(.+?) ⨝_(.+?) (.+?)\s*(\(.+?\))?")
    condition_pattern = re.compile(r"σ_(.+?)\s*\((.+?)\)")
    projection_pattern = re.compile(r"π_(.+?)\s*\((.+?)\)")

    # Encontrar projeções
    for match in re.finditer(projection_pattern, expression):
        fields, from_expr = match.groups()
        projections.append((fields.split(','), from_expr))
        # Analisar a expressão 'from' para mais tabelas
        from_tables = re.findall(r'\b\w+\b', from_expr)
        tables.update(from_tables)

    # Encontrar limitações
    for match in re.finditer(condition_pattern, expression):
        cond, from_expr = match.groups()
        from_tables = re.findall(r'\b\w+\b', from_expr)
        for table in from_tables:
            if table not in conditions:
                conditions[table] = []
            conditions[table].append(cond)
        tables.update(from_tables)

    # Encontrar junções
    for match in re.finditer(join_pattern, expression):
        left_table, condition, right_table, _ = match.groups()
        joins.append((left_table, condition, right_table))
        tables.update([left_table, right_table])

    # Remover as tabelas dos campos de projeção e condições para limpeza
    return {
        "tables": list(tables),
        "joins": joins,
        "conditions": conditions,
        "projections": projections
    }

# Carrega um arquivo SQL e cria uma instância do Interpreter
file = read_file('../data/declaration.sql')
interpreter = Interpreter(file)

# Gera a álgebra relacional a partir da consulta SQL
sql_query = """
SELECT name, age FROM users
JOIN roles ON users.role_id = roles.id
WHERE age > 25 AND name = 'John';
"""


algebra = interpreter.sql_to_algebra(sql_query)
print("Algebra Relacional Original:", algebra)

print()
algebra = "π_name,age(σ_age > 25 AND name = 'John'(users ⨝_users.role_id = roles.id roles))"
print("Alg2", algebra)
print()

dict = parse_relational_algebra(algebra)

for d in dict:
    print(d, dict[d])

"π_Nome,Age((π_Nome, Age, Role-ID(σ_age > 25, Nome='John'(users)))⨝_users.role_id = roles.id (π_ID(roles)))"
# print("Alg2", f"{algebra_users.role-id} = {roles.id(Pi_id(roles)))}")

# Outras operações conforme necessário
