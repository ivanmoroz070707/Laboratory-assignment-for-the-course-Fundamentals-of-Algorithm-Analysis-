import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    STRING = auto()
    SYMBOL = auto()
    OPERATOR = auto()

@dataclass
class Token:
    type: TokenType
    value: str

KEYWORDS = {
    "CREATE", "INSERT", "INTO", "SELECT", "FROM",
    "LEFT_JOIN", "ON", "WHERE", "INDEXED"
}

def tokenize(text: str) -> List[Token]:
    token_specification = [
        ('STRING',     r'"[^"]*"'),                     
        ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]*'),       
        ('OPERATOR',   r'<=|>=|=|<|>'),                 
        ('SYMBOL',     r'[(),;]'),                      
        ('SKIP',       r'\s+'),                         
        ('MISMATCH',   r'.'),                           
    ]
    
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    tokens = []

    for mo in re.finditer(tok_regex, text):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'SKIP':
            continue
        elif kind == 'STRING':
            tokens.append(Token(TokenType.STRING, value[1:-1]))
        elif kind == 'IDENTIFIER':
            upper_val = value.upper()
            if upper_val in KEYWORDS:
                tokens.append(Token(TokenType.KEYWORD, upper_val))
            else:
                tokens.append(Token(TokenType.IDENTIFIER, value))
        elif kind == 'OPERATOR':
            tokens.append(Token(TokenType.OPERATOR, value))
        elif kind == 'SYMBOL':
            tokens.append(Token(TokenType.SYMBOL, value))
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Неприпустимий символ в запиті: '{value}'")

    return tokens