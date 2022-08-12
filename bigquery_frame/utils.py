import re
from typing import TYPE_CHECKING, Iterable, List, Union

if TYPE_CHECKING:
    from bigquery_frame.column import Column, StringOrColumn


def strip_margin(text):
    s = re.sub(r"\n[ \t]*\|", "\n", text)
    if s.startswith("\n"):
        return s[1:]
    else:
        return s


def indent(str, nb) -> str:
    return " " * nb + str.replace("\n", "\n" + " " * nb)


def quote(str) -> str:
    """Add quotes around a column or table names to prevent collision with SQL keywords.
    This method is idempotent: it does not add new quotes to an already quoted string.
    If the column name is a reference to a nested column (i.e. if it contains dots), each part is quoted separately.

    Examples:

    >>> quote("table")
    '`table`'
    >>> quote("`table`")
    '`table`'
    >>> quote("column.name")
    '`column`.`name`'
    >>> quote("*")
    '*'

    """
    return ".".join(["`" + s + "`" if s != "*" else "*" for s in str.replace("`", "").split(".")])


def str_to_col(args: Union[Iterable["StringOrColumn"], "StringOrColumn"]) -> Union[List["Column"], "Column"]:
    """Converts string or Column arguments to Column types

    Examples:

    >>> str_to_col("id")
    Column('`id`')
    >>> str_to_col(["c1", "c2"])
    [Column('`c1`'), Column('`c2`')]
    >>> from bigquery_frame import functions as f
    >>> str_to_col(f.expr("COUNT(1)"))
    Column('COUNT(1)')
    >>> str_to_col("*")
    Column('*')

    """
    from bigquery_frame import functions as f

    if isinstance(args, str):
        return f.col(args)
    elif isinstance(args, list):
        return [str_to_col(arg) for arg in args]
    else:
        return args
