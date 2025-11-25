from dataclasses import dataclass


@dataclass
class Tratta:
    h1: int
    h2: int
    valore_totale: float
    n_spedizioni: int

    def __eq__(self, other):
        return isinstance(other, Tratta) and self.h1 == other.h1 and self.h2 == other.h2

    def __str__(self):
        return f"Tratta: {self.h1} - {self.h2}"

    def __repr__(self):
        return f"Tratta: {self.h1} - {self.h2}"

    def peso_tratta(self) -> float:
        return self.valore_totale / self.n_spedizioni