import re


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


# Exemplo de uso
sql_query = """
SELECT name, age FROM users
JOIN roles ON users.role_id = roles.id
WHERE age > 25 AND (name = 'John' OR name = 'Jane');
"""

result, parsed_sql_or_error = parse_sql(sql_query)
if result:
    print("Parsing successful:", parsed_sql_or_error)
else:
    print("Parsing failed:", parsed_sql_or_error)
