from interpreter import Interpreter
from builder import Builder


def read_file(file_path: str):
    with open(file_path, 'r') as f:
        return f.readlines() if f != None else None

file = read_file('../data/declaration.sql')
interpreter = Interpreter(file)
builder = Builder(interpreter.sql)

# sql_by_terms = interpreter.separate_sql_by_terms()

# for term in sql_by_terms:
#     print(term)

# valid_par = interpreter.check_parenthesis()
# tables = interpreter.attribute_tables()

sql_by_expressions = interpreter.separate_sql_by_expressions()
interpreter.attribute_tables()

validation = interpreter.validade_syntax()
print(validation)
vertices = builder.get_num_vertices()
print(vertices)

# for exp in sql_by_expressions:
#     print(exp)
#     print("=-=-=-=-=-=-=-=-=-")
#     print("=-=-=-=-=-=-=-=-=-")
#     print("=-=-=-=-=-=-=-=-=-")
