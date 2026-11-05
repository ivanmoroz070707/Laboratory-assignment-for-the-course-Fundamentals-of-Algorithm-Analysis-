from typing import Dict, List, Any
from ast_nodes import CreateTableCommand, InsertCommand, SelectCommand

class Table:
    def __init__(self, name:str, columns:List[str]):
        self.name = name
        self.columns = columns
        self.rows = []
    def insert(self, value:List[str]):
        if len(value) != len(self.columns):
            raise ValueError(
                f"Кількість значень ({len(value)}) не відповідає кількості стовпців ({len(self.columns)}) у таблиці '{self.name}'"
            )
        self.rows.append(value)
class Database:
    def __init__(self):
        self.tables ={}
    def command_act(self, command):
        if isinstance(command, CreateTableCommand):
            return self.command_create(command)
        elif isinstance(command, InsertCommand):
            return self.command_insert(command)
        elif isinstance(command, SelectCommand):
            return self.command_select(command)
        else:
            raise ValueError("Невідома команда")
    def command_create(self, cmd: CreateTableCommand):
        if cmd.table_name in self.tables:
            raise ValueError(f"Таблиця '{cmd.table_name}' вже існує.")
        cols_names = [colums[0] for colums in cmd.columns]
        self.tables[cmd.table_name] = Table(cmd.table_name, cols_names)
        return f"Table {cmd.table_name} create."
    def command_insert(self, cmd: InsertCommand):
        if cmd.table_name not in self.tables:
            raise ValueError(f"Таблиці '{cmd.table_name}' не існує.")
        table =  self.tables[cmd.table_name]
        table.insert(cmd.values)
        return f"1 row has been inserted into {cmd.table_name}."
    def command_select(self, cmd: SelectCommand):
        if cmd.table_name_1 not in self.tables:
            raise ValueError(f"Таблиці '{cmd.table_name_1}' не існує.")
        tab1 = self.tables[cmd.table_name_1]

        result_columns = list(tab1.columns)
        result_rows = list(tab1.rows)
        
        if cmd.join_table:
            tab2 = self.tables[cmd.join_table]
            if cmd.t1_column not in tab1.columns:
                raise ValueError(f"Стовпець '{cmd.t1_column}' відсутній у таблиці '{tab1.name}'")
            if cmd.t2_column not in tab2.columns:
                raise ValueError(f"Стовпець '{cmd.t2_column}' відсутній у таблиці '{tab2.name}'")
            tab1_index = tab1.columns.index(cmd.t1_column) 
            tab2_index = tab2.columns.index(cmd.t2_column)

            result_columns = tab1.columns + tab2.columns
            joined_rows = []
            for row_tab1 in tab1.rows:
                found_match = False
                for row_tab2 in tab2.rows:
                     if row_tab1[tab1_index] == row_tab2[tab2_index]:
                         joined_rows.append(row_tab1+row_tab2) 
                         found_match = True
                if not found_match:
                    empty_tab2 = [""]*len(tab2.columns)
                    joined_rows.append(row_tab1+empty_tab2) 
            result_rows = joined_rows
        if cmd.where_col1:
            columns1_index = result_columns.index(cmd.where_col1)
            filtered = []

            for row in result_rows:
                value_1 = row[columns1_index]

                if cmd.is_operand2_literal:
                    value_2 = cmd.where_operand2
                else:
                    columns2_index = result_columns.index(cmd.where_operand2)
                    value_2 = row[columns2_index]

                if value_1< value_2:
                    filtered.append(row)
            result_rows = filtered
        return self.format_table(result_columns, result_rows)

    def format_table(self, cols: List[str], rows: List[List[str]]) -> str:
        
        if not cols:
            return ""
        
        widths = [len(c) for c in cols]
        for r in rows:
            for i in range(len(r)):
                widths[i] = max(widths[i], len(str(r[i])))                
        
        sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"        
        header = "|" + "|".join(f" {cols[i].center(widths[i])} " for i in range(len(cols))) + "|"
        
        lines = [sep, header, sep]
        for r in rows:
            line = "|" + "|".join(f" {str(r[i]).center(widths[i])} " for i in range(len(r))) + "|"
            lines.append(line)
        lines.append(sep)
        
        return "\n".join(lines)



