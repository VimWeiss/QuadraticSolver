import streamlit as st
import numpy as np
from solver import QuadraticSolver
import matplotlib.pyplot as plt

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
        st.write(f"Уравнение: {solver.get_equation_str()}")
        
        if solver.is_valid():
            st.write(f"Дискриминант: {solver.get_discriminant():.4f}")
            
            roots = solver.solve()
            if isinstance(roots, str):
                st.warning(roots)
            else:
                if len(roots) == 1:
                    st.success(f"x = {roots[0]:.4f}")
                else:
                    st.success(f"x₁ = {roots[0]:.4f}")
                    st.success(f"x₂ = {roots[1]:.4f}")
            
            # Plot the quadratic function
            fig = plot_quadratic(a, b, c)
            st.pyplot(fig)
        else:
            st.error("Коэффициент 'a' не может быть равен 0 для квадратного уравнения")

if __name__ == "__main__":
    main()
