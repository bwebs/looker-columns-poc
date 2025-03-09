from typing import List

from sqlglot import exp, lineage


class FQCN:
    def __init__(self, *, table: str, column: str):
        self.table = table
        self.column = column

    def __str__(self):
        return f"{self.column}"


def walk_for_columns(sql: str, target_field: str) -> List[FQCN]:
    lng = lineage.lineage(column=target_field, sql=sql)
    ends: List[FQCN] = []
    for node in lng.walk():
        if isinstance(node.expression, exp.Table):
            ends.append(
                FQCN(
                    table=node.expression.this,
                    column=node.name,
                )
            )
    return ends
