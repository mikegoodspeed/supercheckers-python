def in_middle(row_id, col_id, *, extended: bool = False) -> bool:
    if extended:
        return (1 < row_id < 6) and (1 <= col_id < 6)
    return (1 < row_id < 6) and (1 < col_id < 6)


def to_int(value: str) -> int:
    return ord(value.upper()) - ord("A") + 1


def to_char(value: int) -> str:
    return chr(ord("A") - 1 + value)
