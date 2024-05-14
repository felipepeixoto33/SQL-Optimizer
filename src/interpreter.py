import re
from enum import Enum

class Interpreter:
    def __init__(self, sql) -> None:
        self.sql = sql.splitlines(True)
        self.raw_sql = self.sql_to_string()
        self.common_operators = ['CREATE', 'IF', 'INT', 'NOT', 'NULL', 'EXISTS']
        # Colocar todos os operadores do SQL nesse array acima.
        self.tables = {}
        self.sql_by_expressions = self.separate_sql_by_expressions()

    def separate_sql_by_terms(self):
        terms = []
        for line in self.sql:
            line_terms = re.split(r'(\(|\)|\s|\n)', line)
            line_terms = [t for t in line_terms if t != '' and t != '\n' and t != ' ']
            terms.append(line_terms)
        return terms
    
    def separate_line_by_terms(self, line):
        line_terms = re.split(r'(\(|\)|\s|\n)', line)
        line_terms = [t for t in line_terms if t != '' and t != '\n' and t != ' ']
        return line_terms
    
    def separate_sql_by_expressions(self):
        count = 0
        began = False
        expressions = []
        expression = ''

        for line in self.sql:
            for letter in line:
                expression += letter
                if(letter == '('):
                    count += 1
                    began = True
                elif(letter == ')'):
                    count -= 1
                elif(letter == ';'):
                    expressions.append(expression)
                    began = False
                    expression = ''
                if(count == 0 and began):
                    expressions.append(expression)
                    began = False
                    expression = ''
        
        return expressions

    
    def filter_useful_terms(self, sql_by_terms):
        useful_terms = filter(lambda x: x[0] != '--', sql_by_terms)
        return useful_terms
    
    def remove_terms_of_line(self, sql_to_filter):
        filtered_sql = list(filter(lambda x: x not in self.common_operators and x.upper() != x, self.separate_line_by_terms(sql_to_filter)))
        return filtered_sql

    def check_parenthesis(self):
        count = 0
        for line in self.sql:
            for letter in line:
                if(letter == '('):
                    count += 1
                elif(letter == ')'):
                    count -= 1
                if(count < 0):
                    return False
        return count == 0
    
    def attribute_tables(self):
        for exp in self.sql_by_expressions:
            if("CREATE" not in exp):
                continue

            lines = exp.split("\n")
            table_title = self.remove_terms_of_line(lines[0])
            if(len(table_title) > 0):
                table_title = table_title[0]

            self.create_table(table_title)
            for line in lines[1:]:
                var_name = self.remove_terms_of_line(line)
                if(len(var_name) == 0):
                    print('ERROR')
                var_name = var_name[0]
                self.create_table_parameter(table_title, var_name)

    def create_table(self, table_title):
        # print("TABLE_TITLE:", table_title)
        self.tables[table_title] = {}
        # print(self.tables)
    
    def create_table_parameter(self, table_title, var_name):
        self.tables[table_title][var_name] = None
        # print(self.tables[table_title]) 

    def attribute_parameters(self):
        pass


    def validate_expression(self):
        return self.check_parenthesis()
    
    def sql_to_string(self):
        str = ""
        for line in self.sql:
            str += line
        return str

    def sql_to_algebra(self, sql):
        # Remover quebras de linha e espaços extras
        sql = ' '.join(sql.split())
        
        # Encontrar a cláusula SELECT
        select_clause = re.search(r"SELECT\s+(.*?)\s+FROM", sql, re.IGNORECASE)
        projections = select_clause.group(1) if select_clause else ""
        
        # Encontrar as tabelas e junções
        from_clause = re.search(r"FROM\s+(.*?)(?:WHERE|;|$)", sql, re.IGNORECASE)
        tables = from_clause.group(1) if from_clause else ""
        
        # Converter JOINs
        join_conditions = re.findall(r"JOIN\s+(\w+)\s+ON\s+(\w+\.\w+\s*=\s*\w+\.\w+)", sql, re.IGNORECASE)
        for table, condition in join_conditions:
            tables = f"({tables} ⨝_{condition} {table})"
        
        # Encontrar a cláusula WHERE
        where_clause = re.search(r"WHERE\s+(.*?);", sql, re.IGNORECASE)
        selection = where_clause.group(1) if where_clause else ""
        
        # Montar a expressão de álgebra relacional
        relational_algebra = f"π_{projections} (σ_{selection} ({tables}))"
        
        return relational_algebra

    def check_sql_syntax(self, sql):
        # Verificar a cláusula SELECT
        select_pattern = r"SELECT\s+[\w\.,\s]+\s+FROM\s+[\w\s]+"
        if not re.search(select_pattern, sql, re.IGNORECASE):
            return "Erro de sintaxe na cláusula SELECT ou FROM."

        # Verificar a cláusula JOIN com ON
        join_pattern = r"JOIN\s+\w+\s+ON\s+[\w\.]+\s*=\s*[\w\.]+"
        joins = re.findall(join_pattern, sql, re.IGNORECASE)
        if "JOIN" in sql.upper() and not joins:
            return "Erro de sintaxe na(s) cláusula(s) JOIN/ON."

        # Verificar a cláusula WHERE
        where_pattern = r"WHERE\s+[\w\.\s'=\d]+(?:\s+AND\s+[\w\.\s'=\d]+)*;"
        if "WHERE" in sql.upper() and not re.search(where_pattern, sql, re.IGNORECASE):
            return "Erro de sintaxe na cláusula WHERE."

        # Verificações adicionais podem ser incluídas aqui, como subconsultas, grupos, etc.

        return "Sintaxe SQL parece correta."
