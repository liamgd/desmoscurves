import dataclasses

import pyperclip


@dataclasses.dataclass
class Formula:
    formula: str

    def save(self) -> None:
        pyperclip.copy(self.formula)
        print()
        print(self.formula)
