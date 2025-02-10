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
        return round(self.b**2 - 4*self.a*self.c, 8)

    def get_solution_steps(self):
        """
        Возвращает список шагов решения уравнения с подробными объяснениями
        """
        steps = []

        # Шаг 1: Определение типа уравнения
        steps.append("1️⃣ Определяем тип уравнения:")
        if not self.is_valid():
            steps.append("   a = 0, это не квадратное уравнение")
            return steps

        steps.append(f"   {self.get_equation_str()} - это квадратное уравнение")

        # Шаг 2: Вычисление дискриминанта
        steps.append("\n2️⃣ Вычисляем дискриминант по формуле D = b² - 4ac:")
        steps.append(f"   D = ({self.b})² - 4·({self.a})·({self.c})")
        steps.append(f"   D = {self.b**2} - {4*self.a*self.c}")
        discriminant = self.get_discriminant()
        steps.append(f"   D = {discriminant}")

        # Шаг 3: Анализ дискриминанта
        steps.append("\n3️⃣ Анализируем дискриминант:")
        if discriminant > 0:
            steps.append("   D > 0, уравнение имеет два различных действительных корня")

            # Шаг 4: Вычисление корней
            steps.append("\n4️⃣ Вычисляем корни по формуле x = (-b ± √D) / (2a):")

            x1 = (-self.b + np.sqrt(discriminant)) / (2*self.a)
            x2 = (-self.b - np.sqrt(discriminant)) / (2*self.a)

            steps.append(f"   x₁ = (-({self.b}) + √{discriminant}) / (2·({self.a}))")
            steps.append(f"   x₁ = ({-self.b} + {np.sqrt(discriminant):.4f}) / {2*self.a}")
            steps.append(f"   x₁ = {x1:.4f}")

            steps.append(f"\n   x₂ = (-({self.b}) - √{discriminant}) / (2·({self.a}))")
            steps.append(f"   x₂ = ({-self.b} - {np.sqrt(discriminant):.4f}) / {2*self.a}")
            steps.append(f"   x₂ = {x2:.4f}")

        elif discriminant == 0:
            steps.append("   D = 0, уравнение имеет один действительный корень (кратный)")

            # Шаг 4: Вычисление корня
            steps.append("\n4️⃣ Вычисляем корень по формуле x = -b / (2a):")
            x = -self.b / (2*self.a)
            steps.append(f"   x = -({self.b}) / (2·({self.a}))")
            steps.append(f"   x = {-self.b} / {2*self.a}")
            steps.append(f"   x = {x:.4f}")

        else:
            steps.append("   D < 0, уравнение не имеет действительных корней")

        return steps

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