import streamlit as st
import numpy as np
from solver import QuadraticSolver
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class EquationHistory(Base):
    __tablename__ = 'equation_history'
    id = Column(Integer, primary_key=True)
    a = Column(Float)
    b = Column(Float)
    c = Column(Float)
    discriminant = Column(Float)
    solution_text = Column(String)
    root1 = Column(Float)
    root2 = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


engine = create_engine('sqlite:///equation_history.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def format_term(coef, var='', power=''):
    if coef == 0:
        return ''
    if coef == 1 and var:  # Для случаев x и x²
        return f'+{var}{power}'
    if coef == -1 and var:  # Для случаев -x и -x²
        return f'-{var}{power}'

    # Округляем до 2 знаков и убираем лишние нули после запятой
    coef_str = f"{coef:.2f}".rstrip('0').rstrip('.')
    if coef > 0:
        return f'+{coef_str}{var}{power}'
    return f'{coef_str}{var}{power}'

def format_equation(a, b, c):
    terms = []
    # Добавляем ax²
    if a != 0:
        terms.append(format_term(a, 'x', '²').lstrip('+'))  # Убираем + в начале
    # Добавляем bx
    if b != 0:
        terms.append(format_term(b, 'x'))
    # Добавляем c
    if c != 0:
        terms.append(format_term(c))

    if not terms:
        return '0 = 0'

    return ' '.join(terms) + ' = 0'

def plot_quadratic(a, b, c):
    x = np.linspace(-10, 10, 200)
    y = a * x**2 + b * x + c

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax.grid(True, alpha=0.3)
    ax.set_title('График квадратичной функции')
    return fig

def save_solution(a, b, c, solver, roots):
    session = Session()

    history_entry = EquationHistory(
        a=a,
        b=b,
        c=c,
        discriminant=solver.get_discriminant(),
        solution_text=str(roots) if isinstance(roots, str) else f"x₁={roots[0]:.2f}, x₂={roots[1]:.2f}" if len(roots) > 1 else f"x={roots[0]:.2f}",
        root1=None if isinstance(roots, str) else roots[0],
        root2=None if isinstance(roots, str) or len(roots) == 1 else roots[1]
    )

    session.add(history_entry)
    session.commit()
    session.close()

def display_history():
    session = Session()
    history = session.query(EquationHistory).order_by(EquationHistory.created_at.desc()).limit(5).all()

    if history:
        st.markdown("### Последние решения:")
        for entry in history:
            equation = format_equation(entry.a, entry.b, entry.c)
            st.markdown(f"""
            **Уравнение:** {equation}
            - Дискриминант: {entry.discriminant:.2f}
            - Решение: {entry.solution_text}
            - Время: {entry.created_at.strftime('%H:%M:%S')}
            ---
            """)

    session.close()

def main():
    st.set_page_config(page_title="Решение квадратных уравнений", layout="wide")

    # Load custom CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("Решение квадратных уравнений")
    st.markdown("### ax² + bx + c = 0")

    col1, col2, col3 = st.columns(3)

    with col1:
        a = st.number_input("Коэффициент a", value=1.0, step=0.1)
    with col2:
        b = st.number_input("Коэффициент b", value=0.0, step=0.1)
    with col3:
        c = st.number_input("Коэффициент c", value=0.0, step=0.1)

    if st.button("Решить уравнение"):
        solver = QuadraticSolver(a, b, c)

        st.markdown("### Решение:")
        st.write(f"Уравнение: {format_equation(a, b, c)}")

        if solver.is_valid():
            st.write(f"Дискриминант: {solver.get_discriminant():.2f}")

            roots = solver.solve()
            if isinstance(roots, str):
                st.warning(roots)
            else:
                if len(roots) == 1:
                    st.success(f"x = {roots[0]:.2f}")
                else:
                    st.success(f"x₁ = {roots[0]:.2f}")
                    st.success(f"x₂ = {roots[1]:.2f}")

            # Save solution to database
            save_solution(a, b, c, solver, roots)

            # Plot the quadratic function
            fig = plot_quadratic(a, b, c)
            st.pyplot(fig)
        else:
            st.error("Коэффициент 'a' не может быть равен 0 для квадратного уравнения")

    # Display solution history
    display_history()

if __name__ == "__main__":
    main()