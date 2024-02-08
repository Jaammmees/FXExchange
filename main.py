import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDesktopWidget, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer
from matplotlib.figure import Figure
import mplfinance as mpf

import api_client  # Your custom module for data fetching

class ForexApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.instrument = "AUD_USD"
        self.granularity = "S30"
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Forex Data Live Plot')
        self.setGeometry(0, 0, 1920, 1080)
        self.centerWindow()

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        mainLayout = QHBoxLayout()

        controlLayout = QVBoxLayout()
        orderBookLabel = QLabel("Order Book Data")
        buyButton = QPushButton('Buy')
        sellButton = QPushButton('Sell')
        controlLayout.addWidget(orderBookLabel)
        controlLayout.addWidget(buyButton)
        controlLayout.addWidget(sellButton)

        # Explicitly create a layout for the chart
        self.chartLayout = QVBoxLayout()  
        self.canvas = None  # Placeholder for the matplotlib canvas
        #chart inputs
        inputLayout = QHBoxLayout()
        self.fxPairInput = QLineEdit(self.instrument)
        updateFxPairButton = QPushButton('Update FX')
        updateFxPairButton.clicked.connect(self.updateFxPair)
        inputLayout.addWidget(self.fxPairInput)
        inputLayout.addWidget(updateFxPairButton)

        #different resolution buttons
        resolutions = ["S5", "S30", "M1", "M15", "M30", "H1", "W", "M"]
        for res in resolutions:
            button = QPushButton(res)
            button.clicked.connect(lambda checked, res = res: self.changeResolution(res))
            inputLayout.addWidget(button)
        
        self.chartLayout.addLayout(inputLayout)

        # Add the control layout and the chart layout to the main layout
        mainLayout.addLayout(controlLayout, 1)
        mainLayout.addLayout(self.chartLayout, 3)  # Allocating more space for the chart

        centralWidget.setLayout(mainLayout)

        # Timer to update plot
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start(100)  # Update interval in milliseconds

        self.updatePlot()  # Initial plot update

    def updateFxPair(self):
        newInstrument = self.fxPairInput.text()
        self.instrument = newInstrument
        self.updatePlot()

    def changeResolution(self, resolution):
        self.granularity = resolution

    #centering app screen
    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def updatePlot(self):
        # Fetch updated data
        df = api_client.fetch_fx_data(self.instrument,self.granularity)
        
        # Clear the figure for a fresh plot
        if self.canvas is not None:
            fig = self.canvas.figure
            # If canvas exists, remove it from the layout and delete it to prevent memory leak
            plt.close(fig)
            self.canvas.setParent(None)
            self.canvas.deleteLater()

        # Create a new figure for each update
        fig, axes = mpf.plot(df, 
                             type='candle', 
                             style='yahoo', 
                             volume=True, 
                             figsize=(10, 6), 
                             returnfig=True, 
                             scale_padding={'left': 0.05, 'right': 1.0, 'top': 0.1, 'bottom': 0.7},
                             datetime_format='%I:%M %p',
                             )


        self.canvas = FigureCanvas(fig)
        self.chartLayout.addWidget(self.canvas)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ForexApp()
    ex.show()
    sys.exit(app.exec_())
