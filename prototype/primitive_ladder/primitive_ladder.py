"""Малий зонд для дослідження примітива на різних ширинах."""

from dataclasses import dataclass

SUPPORTED_WIDTHS = (8, 16, 32, 64)


@dataclass(frozen=True)
class Primitive:
    name: str
    width: int
    value: int

    def __post_init__(self) -> None:
        if self.width not in SUPPORTED_WIDTHS:
            raise ValueError(f"непідтримувана ширина: {self.width}")
        if not 0 <= self.value < (1 << self.width):
            raise ValueError(f"значення не поміщається у {self.width} бітів")

    def lift(self, width: int) -> "Primitive":
        """Перенести числовий носій у більшу ширину без зміни значення."""
        if width < self.width:
            raise ValueError("підняття вимагає не меншої ширини")
        return Primitive(self.name, width, self.value)

    def bits(self) -> str:
        return f"{self.value:0{self.width}b}"


def compose(left: Primitive, right: Primitive, width: int) -> Primitive:
    """Пробно скласти два поля; це пакування, а не семантичне правило."""
    required = left.width + right.width
    if width < required:
        raise ValueError(f"потрібно щонайменше {required} бітів")
    value = (left.value << right.width) | right.value
    return Primitive(f"({left.name},{right.name})", width, value)


def demo() -> None:
    atom = Primitive("атом", 8, 0x12)
    neighbour = Primitive("сусід", 8, 0x34)
    pair = compose(atom, neighbour, 16)
    print(f"{atom.name}:   {atom.width}-bit 0x{atom.value:02x} {atom.bits()}")
    print(f"{neighbour.name}: {neighbour.width}-bit 0x{neighbour.value:02x} {neighbour.bits()}")
    print(f"складання: {pair.width}-bit 0x{pair.value:04x} {pair.bits()}")
    print(f"підняття:  {atom.lift(16).width}-bit 0x{atom.lift(16).value:04x}")


if __name__ == "__main__":
    demo()
