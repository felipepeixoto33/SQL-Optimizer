import re

class Interpreter:
    def __init__(self, sql) -> None:
        self.sql = sql
        self.common_operators = ['CREATE', 'IF', 'INT', 'NOT', 'NULL']
        self.tables = {}
        self.separate_sql_by_terms
        # Colocar todos os operadores do SQL nesse array acima.

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
        for line in self.sql:
            terms = self.separate_line_by_terms(line)
            print(terms)

    def attribute_parameters(self):
        pass
    
    def validate_expression(self):
        return self.check_parenthesis()
    
    def create_table(self, table_sql):
        pass