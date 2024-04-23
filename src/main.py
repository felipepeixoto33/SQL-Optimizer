from interpreter import Interpreter


def read_file(file_path: str):
    with open(file_path, 'r') as f:
        return f.readlines() if f != None else None

file = read_file('../data/example.sql')
interpreter = Interpreter(file)
# sql_by_terms = interpreter.separate_sql_by_terms()

# for term in sql_by_terms:
#     print(term)

# valid_par = interpreter.check_parenthesis()
# tables = interpreter.attribute_tables()

sql_by_expressions = interpreter.separate_sql_by_expressions()
# for exp in sql_by_expressions:
#     print(exp)
#     print("=-=-=-=-=-=-=-=-=-")
#     print("=-=-=-=-=-=-=-=-=-")
#     print("=-=-=-=-=-=-=-=-=-")
