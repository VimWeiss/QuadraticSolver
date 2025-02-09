import numpy as np

class QuadraticSolver:
    def __init__(self, a: float, b: float, c: float):
        self.a = float(a)  # Преобразуем в float для безопасности
        self.b = float(b)
        self.c = float(c)

    def is_valid(self) -> bool:
        return self.a != 0

    def get_equation_str(self) -> str:
        terms = []

        if self.a != 0:
            terms.append(f"{self.a if self.a != 1 else ''}x²")

        if self.b != 0:
            sign = "+" if self.b > 0 and terms else ""
            terms.append(f"{sign}{self.b if self.b != 1 else ''}x")

        if self.c != 0 or not terms:
            sign = "+" if self.c > 0 and terms else ""
            terms.append(f"{sign}{self.c}")

        return " ".join(terms) + " = 0"

    def get_discriminant(self) -> float:
        """
        Вычисляет дискриминант квадратного уравнения по формуле D = b² - 4ac
        """
        return round(self.b**2 - 4*self.a*self.c, 8)  # Округляем до 8 знаков для устранения погрешностей вычислений

    def solve(self):
        if not self.is_valid():
            return "Это не квадратное уравнение (a=0)"

        discriminant = self.get_discriminant()

        if discriminant > 0:
            x1 = (-self.b + np.sqrt(discriminant)) / (2*self.a)
            x2 = (-self.b - np.sqrt(discriminant)) / (2*self.a)
            return sorted([x1, x2])
        elif discriminant == 0:
            x = -self.b / (2*self.a)
            return [x]
        else:
            return "Уравнение не имеет действительных корней"