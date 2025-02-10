from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from reportlab.lib.units import inch
from reportlab.graphics.charts.piecharts import Pie



def reporte_credito(self):
    