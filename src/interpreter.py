import re
from enum import Enum

class Interpreter:
    def __init__(self, sql) -> None:
        self.sql = sql
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
    
    def validade_syntax(self):
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
        components['SELECT'] = safe_search(r'SELECT\s+([\w\s\*,]+)\s+', self.raw_sql)
        if not components['SELECT']:
            return False, "Error parsing SELECT"

        # Extrair FROM
        components['FROM'] = safe_search(r'FROM\s+([\w\s]+?)(?:\s+WHERE|\s+JOIN|;|$)', self.raw_sql)
        if not components['FROM']:
            return False, "Error parsing FROM"

        # Extrair WHERE, se existir
        components['WHERE'] = safe_search(r'WHERE\s+(.*?)(?:\s+JOIN|;|$)', self.raw_sql)

        # Extrair JOINs
        joins = re.finditer(r'JOIN\s+([\w\s]+)\s+ON\s+([\w\s\.\=\>\<\!\(\)]+)', self.raw_sql, re.IGNORECASE)
        for join in joins:
            components['JOIN'].append((join.group(1).strip(), join.group(2).strip()))

        # Retorna true e os componentes se tudo estiver correto
        return True, components


    def validate_expression(self):
        return self.check_parenthesis() and self.validade_syntax()
    
    def sql_to_string(self):
        str = ""
        for line in self.sql:
            str += line
        return str

    def sql_to_algebra(self, sql_query):
        # Extração dos componentes principais da consulta SQL
        select_match = re.search(r'SELECT\s+([\w\s\*,]+)\s+FROM', sql_query, re.IGNORECASE)
        from_match = re.search(r'FROM\s+(\w+)', sql_query, re.IGNORECASE)
        where_match = re.search(r'WHERE\s+([^;]+)', sql_query, re.IGNORECASE)
        join_match = re.search(r'JOIN\s+(\w+)\s+ON\s+([\w\.]+)\s*=\s*([\w\.]+)', sql_query, re.IGNORECASE)

        # Montagem da álgebra relacional
        if select_match and from_match:
            projection_fields = select_match.group(1).replace(' ', '')
            from_table = from_match.group(1)
            relational_algebra = f'π_{projection_fields} ('

            if where_match:
                conditions = where_match.group(1)
                relational_algebra += f'σ_{conditions} ('

            if join_match:
                join_table = join_match.group(1)
                join_condition = f"{join_match.group(2)} = {join_match.group(3)}"
                relational_algebra += f'{from_table} ⨝_{join_condition} {join_table}'
            else:
                relational_algebra += from_table

            relational_algebra += ')'
            if where_match:
                relational_algebra += ')'

            return relational_algebra

        return "Query structure not recognized"

    def optimize_algebra(self, sql_as_algebra):
        pass
