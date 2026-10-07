from dataclasses import dataclass
from typing import Optional, List, Tuple

@dataclass
class CreateTableCommand:
    table_name: str
    columns: List[Tuple[str,bool]]

@dataclass
class InsertCommand:
    table_name: str
    values: List[str]

@dataclass
class SelectCommand:
    table_name_1: str
    join_table: Optional[str] = None
    t1_column: Optional[str] = None
    t2_column: Optional[str] = None
    where_col1: Optional[str] = None
    where_operand2: Optional[str] = None  
    is_operand2_literal: bool = False     