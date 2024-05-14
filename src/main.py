import re
from node import Node, ExpressionTypes
import tkinter as tk
from tkinter import scrolledtext, messagebox
import plot
from interpreter import Interpreter

def analisar_sql(query):
    elementos = {
        "Tables": [],
        "Joins": [],
        "Conditions": {},
        "Projections": {},
        "Intermediary-Projections": {}
    }

    proj_regex = re.compile(r'SELECT\s+(.*?)\s+FROM', re.IGNORECASE)
    match_proj = proj_regex.search(query)
    if match_proj:
        projections = match_proj.group(1).split(',')
        for proj in projections:
            proj = proj.strip()
            table_column = re.match(r'(\w+)\.(\w+)', proj)
            if table_column:
                table, column = table_column.groups()
                if table not in elementos['Projections']:
                    elementos['Projections'][table] = []
                elementos['Projections'][table].append(column)

    tables = []
    table_regex = re.compile(r'FROM\s+(\w+)', re.IGNORECASE)
    join_regex = re.compile(r'JOIN\s+(\w+)', re.IGNORECASE)
    match_table = table_regex.search(query)
    if match_table:
        main_table = match_table.group(1)
        if main_table not in tables:
            tables.append(main_table)
    join_matches = join_regex.findall(query)
    for join_table in join_matches:
        if join_table not in tables:
            tables.append(join_table)

    elementos['Tables'] = tables
    for table in tables:
        elementos['Conditions'][table] = []
        elementos['Intermediary-Projections'][table] = set()

    join_detail_regex = re.compile(r'JOIN\s+(\w+)\s+ON\s+(.*?)\s+(?=JOIN|WHERE|$)', re.IGNORECASE | re.DOTALL)
    for join_match in join_detail_regex.finditer(query):
        join_table = join_match.group(1)
        join_condition = join_match.group(2).strip()
        join_from = re.search(r'(\w+)\.', join_condition).group(1)
        elementos['Joins'].append({"tables": [join_from, join_table], "on": join_condition})
        on_parts = re.findall(r'(\w+)\.(\w+)', join_condition)
        for part in on_parts:
            table, column = part
            elementos['Intermediary-Projections'][table].add(column)

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
                    elementos['Intermediary-Projections'][table].add(column)

    for table in elementos['Intermediary-Projections']:
        elementos['Intermediary-Projections'][table] = list(elementos['Intermediary-Projections'][table])

    return elementos

def define_graph_flow(dicts):
    print("DICTS:")
    for k,v in dicts.items():
        print(k, v)
    print()
    print()

    table_nodes = {}
    temp_flow = []
    step = 1
    tables_flow = {}
    graph_flow = []
    join_nodes = []

    for t in dicts['Tables']:
        table_nodes[t] = [t]

        for t_n, c in dicts['Conditions'].items():
            if(t == t_n):
                table_nodes[t].append(f"σ {c}")
        for t_n, i_p in dicts['Intermediary-Projections'].items():
            if(t == t_n):
                table_nodes[t].append(f"π {i_p}")

    for k, v in table_nodes.items():
        tables_flow[k] = []
        for i in v:
            node = Node(f'passo {step}', i)
            if(node.expression[0] == 'σ'):
                node.expression_type = ExpressionTypes.SELECT
            elif(node.expression[0] == 'π'):
                node.expression_type = ExpressionTypes.PROJECAO
            step += 1
            if(len(temp_flow) > 0):
                node.connect_to(temp_flow[-1])
            tables_flow[k].append(node)
            temp_flow.append(node)
            graph_flow.append(node)
        temp_flow = []

    for join in dicts['Joins']:
        tables = join['tables']
        expr = join['on']
        node = Node(f'passo {step}', expression=f"⨝ {expr}", expression_type=ExpressionTypes.JUNCAO)
        step += 1
        join_tables = []
        for t_in_node in table_nodes.keys():
            if(t_in_node in tables):
                join_tables.append(t_in_node)
        for joined_t in join_tables:
            tables_flow[joined_t][-1].connect_to(node)
            node.expression_type = ExpressionTypes.JUNCAO
        join_nodes.append(node)
        graph_flow.append(node)

    for k in range(1, len(join_nodes)):
        join_nodes[k].connect_to(join_nodes[k-1])

    expression = "π "
    for _i in range(len(dicts['Projections'])):
        tables = list(dicts['Projections'].keys())
        for _j in range(len(dicts['Projections'][tables[_i]])):
            values = dicts['Projections'][tables[_i]]
            expression += f"{values[_j]}, "
    expression = expression[:-2]
    node = Node(f'passo {step}', expression, graph_flow[-1])
    graph_flow.append(node)

    return graph_flow, join_nodes, table_nodes

def define_steps(graph_flow, join_nodes):
    steps = []
    join_index = 0
    for node in graph_flow:
        if(node.expression_type == ExpressionTypes.PROJECAO and join_index < len(join_nodes)):
            steps.append(node)
            steps.append(join_nodes[join_index])
            join_index += 1
            continue
        if(node.expression_type != ExpressionTypes.JUNCAO):
            steps.append(node)
    for i in range(len(steps)):
        node = steps[i]
        node.name = f'passo {(i+1)}'
    return steps

def visualize_graph(graph):
    graph_str = ""
    for node in graph:
        connections = ', '.join([n.name for n in node.connected_nodes])
        graph_str += f"{node.name}: {node.expression} -> [{connections}]\n"
    return graph_str

def process_sql_query():
    sql_query = txt_input.get("1.0", tk.END).strip()

    if sql_query:
        interpreter = Interpreter(sql_query)
        is_sql_valid = interpreter.validade_syntax()
        algebra = interpreter.sql_to_algebra(sql_query)
        print("SQL valido: ", is_sql_valid)
        print("SQL as Algebra", algebra)

        result = analisar_sql(sql_query)
        graph, joins, ts = define_graph_flow(result)
        steps = define_steps(graph, joins)

        G = plot.create_graph_from_nodes(steps)  # Substitua 'nodes' pela sua lista de objetos Node
        plot.draw_graph(G)

        graph_text_area.delete('1.0', tk.END)
        graph_text_area.insert('1.0', visualize_graph(graph))
    else:
        messagebox.showinfo("Information", "Please enter a SQL query before processing.")

root = tk.Tk()
root.geometry("600x600")
root.title("SQL Query Processor")
txt_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=50)
txt_input.pack(pady=10)
graph_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=50)
graph_text_area.pack(pady=10)
process_button = tk.Button(root, text="Process SQL Query", command=process_sql_query)
process_button.pack(pady=20)
root.mainloop()


