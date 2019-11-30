def to_int(value: str) -> int:
    return ord(value.upper()) - ord("A") + 1


def to_char(value: int) -> str:
    return chr(ord("A") - 1 + value)
