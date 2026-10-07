from typing import List, Optional
from lexer import Token, TokenType
from ast_nodes import CreateTableCommand, InsertCommand, SelectCommand

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Optional[Token]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type: Optional[TokenType] = None, expected_value: Optional[str] = None) -> Token:
        token = self.peek()
        if not token:
            raise SyntaxError("Несподіваний кінець команди")
        
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Очікується тип {expected_type}, отриманно {token.type} ('{token.value}')")
        if expected_value and token.value.upper() != expected_value.upper():
            raise SyntaxError(f"Очікувалось '{expected_value}', отриманно '{token.value}'")

        self.pos += 1
        return token

    def parse(self):
        token = self.peek()
        if not token or token.type != TokenType.KEYWORD:
            raise SyntaxError("Запит повиннен починатися з ключового слова (CREATE, INSERT, SELECT)")

        keyword = token.value
        if keyword == "CREATE":
            return self._parse_create()
        elif keyword == "INSERT":
            return self._parse_insert()
        elif keyword == "SELECT":
            return self._parse_select()
        else:
            raise SyntaxError(f"Невідома команда '{keyword}'")

    def _parse_create(self) -> CreateTableCommand:
        self.consume(TokenType.KEYWORD, "CREATE")
        table_name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.SYMBOL, "(")

        columns = []
        while True:
            col_name = self.consume(TokenType.IDENTIFIER).value
            is_indexed = False
            
            if self.peek() and self.peek().value == "INDEXED":
                self.consume(TokenType.KEYWORD, "INDEXED")
                is_indexed = True

            columns.append((col_name, is_indexed))

            if self.peek() and self.peek().value == ",":
                self.consume(TokenType.SYMBOL, ",")
            else:
                break

        self.consume(TokenType.SYMBOL, ")")
        return CreateTableCommand(table_name, columns)

    def _parse_insert(self) -> InsertCommand:
        self.consume(TokenType.KEYWORD, "INSERT")
        if self.peek() and self.peek().value == "INTO":
            self.consume(TokenType.KEYWORD, "INTO")

        table_name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.SYMBOL, "(")

        values = []
        while True:
            val = self.consume(TokenType.STRING).value
            values.append(val)

            if self.peek() and self.peek().value == ",":
                self.consume(TokenType.SYMBOL, ",")
            else:
                break

        self.consume(TokenType.SYMBOL, ")")
        return InsertCommand(table_name, values)

    def _parse_select(self) -> SelectCommand:
        self.consume(TokenType.KEYWORD, "SELECT")
        self.consume(TokenType.KEYWORD, "FROM")
        t1_name = self.consume(TokenType.IDENTIFIER).value

        join_table = t1_col = t2_col = None
        where_col1 = where_op2 = None
        is_literal = False

        if self.peek() and self.peek().value == "LEFT_JOIN":
            self.consume(TokenType.KEYWORD, "LEFT_JOIN")
            join_table = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.KEYWORD, "ON")
            t1_col = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.OPERATOR, "=")
            t2_col = self.consume(TokenType.IDENTIFIER).value

        if self.peek() and self.peek().value == "WHERE":
            self.consume(TokenType.KEYWORD, "WHERE")
            where_col1 = self.consume(TokenType.IDENTIFIER).value
            
            op = self.consume(TokenType.OPERATOR).value
            if op != "<":
                raise SyntaxError(f"В Варіанті №5 в WHERE підтримується тільки оператор'<', отриманно '{op}'")

            next_tok = self.peek()
            if next_tok and next_tok.type == TokenType.STRING:
                where_op2 = self.consume(TokenType.STRING).value
                is_literal = True
            elif next_tok and next_tok.type == TokenType.IDENTIFIER:
                where_op2 = self.consume(TokenType.IDENTIFIER).value
                is_literal = False
            else:
                raise SyntaxError("Після '<' очікується рядок в лапках або ім'я колонки")

        return SelectCommand(
            table_name_1=t1_name,
            join_table=join_table,
            t1_column=t1_col,
            t2_column=t2_col,
            where_col1=where_col1,
            where_operand2=where_op2,
            is_operand2_literal=is_literal
        )