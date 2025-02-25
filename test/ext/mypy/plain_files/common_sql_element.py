"""tests for #8847

we want to assert that SQLColumnExpression can be used to represent
all SQL expressions generically, across Core and ORM, without using
unions.

"""


from __future__ import annotations

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import SQLColumnExpression
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "a"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]


user_table = Table(
    "user_table", MetaData(), Column("id", Integer), Column("email", String)
)


def receives_str_col_expr(expr: SQLColumnExpression[str]) -> None:
    pass


def receives_bool_col_expr(expr: SQLColumnExpression[bool]) -> None:
    pass


def orm_expr(email: str) -> SQLColumnExpression[bool]:
    return User.email == email


def core_expr(email: str) -> SQLColumnExpression[bool]:
    email_col: Column[str] = user_table.c.email
    return email_col == email


e1 = orm_expr("hi")

# EXPECTED_TYPE: SQLColumnExpression[bool]
reveal_type(e1)

stmt = select(e1)

# EXPECTED_TYPE: Select[Tuple[bool]]
reveal_type(stmt)

stmt = stmt.where(e1)


e2 = core_expr("hi")

# EXPECTED_TYPE: SQLColumnExpression[bool]
reveal_type(e2)

stmt = select(e2)

# EXPECTED_TYPE: Select[Tuple[bool]]
reveal_type(stmt)

stmt = stmt.where(e2)


receives_str_col_expr(User.email)
receives_str_col_expr(User.email + "some expr")
receives_str_col_expr(User.email.label("x"))
receives_str_col_expr(User.email.label("x"))

receives_bool_col_expr(e1)
receives_bool_col_expr(e1.label("x"))
receives_bool_col_expr(User.email == "x")

receives_bool_col_expr(e2)
receives_bool_col_expr(e2.label("x"))
receives_bool_col_expr(user_table.c.email == "x")
