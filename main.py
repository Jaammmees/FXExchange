import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import mplfinance as mpf

import api_client  # Your custom module for data fetching

class ForexApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.instrument = "AUD_USD"
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Forex Data Live Plot')
        self.setGeometry(100, 100, 800, 600)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        layout = QVBoxLayout(centralWidget)

        layout.setContentsMargins(50, 50, 50, 50)  
        layout.setSpacing(0)


        # Placeholder for the matplotlib canvas
        self.canvas = None

        # Timer to update plot
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start(100)  # Update interval in milliseconds

        self.updatePlot()  # Initial plot update

    def updatePlot(self):
        # Fetch updated data
        df = api_client.fetch_fx_data(self.instrument)
        
        # Clear the figure for a fresh plot
        if self.canvas is not None:
            fig = self.canvas.figure
            # If canvas exists, remove it from the layout and delete it to prevent memory leak
            plt.close(fig)
            self.canvas.setParent(None)
            self.canvas.deleteLater()

        # Create a new figure for each update
        fig, axes = mpf.plot(df, type='candle', style='yahoo', volume=True, figsize=(10, 6), returnfig=True)
        fig.subplots_adjust(left=0.05, right=0.95)
        self.canvas = FigureCanvas(fig)
        self.centralWidget().layout().addWidget(self.canvas)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ForexApp()
    ex.show()
    sys.exit(app.exec_())
