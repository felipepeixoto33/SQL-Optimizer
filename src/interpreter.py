import re

class Interpreter:
    def __init__(self, sql) -> None:
        self.sql = sql
        self.common_operators = ['CREATE', 'IF', 'INT', 'NOT', 'NULL']
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
        tables = {}
        for line in self.sql:
            terms = self.separate_line_by_terms(line)
            print(terms)

    def attribute_parameters(self):
        pass
    
    def validate_expression(self):
        return self.check_parenthesis()
        