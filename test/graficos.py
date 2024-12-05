import plotly.graph_objects as go
import random
import time
from itertools import cycle

# Configuración inicial
productos = ["Producto A", "Producto B", "Producto C", "Producto D"]
colores = cycle(["#FF5733", "#33FF57", "#3357FF", "#F1C40F"])  # Ciclo de colores
datos = {producto: [random.randint(20, 100)] for producto in productos}  # Datos iniciales

# Crear la figura inicial
fig = go.Figure()

# Añadir trazas para cada producto
for producto, color in zip(productos, colores):
    fig.add_trace(go.Scatter(
        x=[0], y=datos[producto], mode="lines+markers", name=producto,
        line=dict(color=color, width=2),
        marker=dict(size=8)
    ))

# Configuración del diseño
fig.update_layout(
    title="Gráfico Dinámico de Productos",
    xaxis_title="Tiempo (segundos)",
    yaxis_title="Unidades Vendidas",
    template="plotly_dark",
    showlegend=True
)

# Función para simular datos en tiempo real
def actualizar_datos(fig, max_iteraciones=20, intervalo=1):
    for t in range(1, max_iteraciones + 1):
        for i, producto in enumerate(productos):
            # Añadir nuevos datos aleatorios
            nuevos_datos = datos[producto][-1] + random.randint(-5, 10)
            datos[producto].append(max(nuevos_datos, 0))  # Asegurarse de que no haya valores negativos

            # Actualizar la traza del producto
            fig.data[i].x = list(range(len(datos[producto])))
            fig.data[i].y = datos[producto]

        # Renderizar el gráfico actualizado
        fig.show(renderer="browser")  # Abre el navegador para visualizarlo
        time.sleep(intervalo)  # Espera antes de la siguiente actualización

# Llamar a la función para actualizar datos
actualizar_datos(fig)
