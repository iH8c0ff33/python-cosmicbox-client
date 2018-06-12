import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from cosmicbox import UpdateThread 

class CosmicBox(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.top = QLabel("0", self)
        self.bottom = QLabel("0", self)
        self.ext = QLabel("0", self)
        self.coinc = QLabel("0", self)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        hbox1.addWidget(self.top)
        hbox1.addWidget(self.bottom)

        hbox2.addWidget(self.ext)
        hbox2.addWidget(self.coinc)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("CosmicBox")
        self.show()
    
    def update(self, values):
        self.top.setText(repr(values["top"]))
        self.bottom.setText(repr(values["bottom"]))
        self.ext.setText(repr(values["ext"]))
        self.coinc.setText(repr(values["coinc"]))
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CosmicBox()

    t = UpdateThread()
    t.update.connect(w.update)
    t.start()

    sys.exit(app.exec_())
