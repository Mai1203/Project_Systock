import sys
import plotly.graph_objects as go
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QTimer
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráficos Dinámicos con Plotly y PyQt6")
        self.setGeometry(100, 100, 800, 600)
        
        # Configuración del layout y el widget principal
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Vista del navegador WebEngine para mostrar el gráfico
        self.view = QWebEngineView()
        self.layout.addWidget(self.view)

        # Crear la figura de Plotly
        self.fig = go.Figure()

        # Productos para simular
        self.productos = ["Producto A", "Producto B", "Producto C", "Producto D"]
        self.datos = {producto: [random.randint(20, 100)] for producto in self.productos}

        # Colores de las líneas
        colores = ["#FF5733", "#33FF57", "#3357FF", "#F1C40F"]

        # Añadir las trazas a la figura
        for producto, color in zip(self.productos, colores):
            self.fig.add_trace(go.Scatter(
                x=[0], y=self.datos[producto], mode="lines+markers", name=producto,
                line=dict(color=color, width=2),
                marker=dict(size=8)
            ))

        # Configurar el QTimer para actualizar el gráfico
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)  # Llamar a update_graph cada vez que suene el timer
        self.timer.start(1000)  # Actualizar cada 1000 ms (1 segundo)

    def update_graph(self):
        """Actualiza el gráfico dinámicamente."""
        for i, producto in enumerate(self.productos):
            # Simula nuevos datos
            nuevos_datos = self.datos[producto][-1] + random.randint(-5, 10)
            self.datos[producto].append(max(nuevos_datos, 0))  # Evitar valores negativos

            # Actualizar la traza correspondiente
            self.fig.data[i].x = list(range(len(self.datos[producto])))
            self.fig.data[i].y = self.datos[producto]

        # Renderizar la figura en HTML
        html = self.fig.to_html(full_html=False)

        # Asegurarse de que el gráfico se cargue correctamente
        self.view.setHtml(html)

        # Forzar el redibujado para asegurarse de que el contenido se actualiza
        self.view.reload()

# Crear la aplicación y la ventana principal
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
