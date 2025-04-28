""""Dit programma berekent de hoeveelheid inkt die nodig is voor een x aantal druks.
De gebruiker voert drie velden in en zie onmiddellijk het resultaat. Dit programma is
geschreven in PySide6. Gemaakt door <Erwin de Geus> op 27-04-2025"""
__VERSION__ = "1.0"

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import (
                           QIntValidator,
                           QFont,
                           QPalette,
                           QColor)

from PySide6.QtWidgets import (
                             QApplication,
                             QWidget,
                             QLabel,
                             QLineEdit,
                             QVBoxLayout,
                             QComboBox,
                             QMainWindow)

font = QFont()
font.setPointSize(12)

LabelStyle = """
    QLabel {
        color: #3c0c9f;
        font-weight: regular;
        font-family: Arial;
        font-size: 14px;
        padding: 5px;
    }
"""
InputStyle = """
    QLineEdit:focus {
        border: 2px solid #efb9ad;
        background-color: #f0f0f0;
    }
"""
palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor("#7af9ef"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('inkt calculator')
        self.setMinimumSize(250, 300)
        self.setMaximumSize(500, 600)

        # Maak een centraal widget en layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # papier oplage invoerveld
        self.label1 = QLabel("Voer de oplage in:")
        self.label1.setFont(font)
        self.label1.setStyleSheet(LabelStyle)
        self.number1 = QLineEdit()
        self.number1.setFixedWidth(300)
        self.number1.setFixedHeight(30)
        self.number1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.number1.setPlaceholderText("Voer oplage in")
        self.number1.returnPressed.connect(lambda: self.number2.setFocus())
        self.number1.setValidator(QIntValidator(1, 1000000))
        self.number1.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.number1.setStyleSheet(InputStyle)
        self.number1.textChanged.connect(self.bereken)

        # dekking percentage invoerveld
        self.label2 = QLabel("Voer dekking percentage in:")
        self.label2.setFont(font)
        self.label2.setStyleSheet(LabelStyle)
        self.number2 = QLineEdit()
        self.number2.setFixedWidth(300)
        self.number2.setFixedHeight(30)
        self.number2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.number2.setPlaceholderText("Dekking percentage van 1 t/m 100")
        self.number2.returnPressed.connect(lambda: self.papierformaat.setFocus())
        self.number2.setValidator(QIntValidator(1, 100))
        self.number2.setStyleSheet(InputStyle)
        self.number2.textChanged.connect(self.bereken)

        # Papierformaat ComboBox
        self.label3 = QLabel("Selecteer papierformaat:")
        self.label3.setFont(font)
        self.label3.setStyleSheet(LabelStyle)
        self.papierformaat = QComboBox()
        self.papierformaat.setFixedWidth(300)
        self.papierformaat.setFixedHeight(30)
        self.papierformaat.addItems(["A3", "A4"])
        self.papierformaat.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.papierformaat.setStyleSheet(InputStyle)
        self.papierformaat.currentTextChanged.connect(self.bereken)

        # Resultaat label
        self.resultaat_label = QLabel("U moet ")
        self.resultaat_label.setFont(font)
        self.resultaat_label.setStyleSheet(LabelStyle)

        # Resultaat label droging
        self.resultaat_label_droging = QLabel("2% droging: ")
        self.resultaat_label_droging.setFont(font)
        self.resultaat_label_droging.setStyleSheet(LabelStyle)

        # Voeg widgets toe aan de layout
        layout.addWidget(self.label1)
        layout.addWidget(self.number1)
        layout.addWidget(self.label2)
        layout.addWidget(self.number2)
        layout.addWidget(self.label3)
        layout.addWidget(self.papierformaat)
        layout.addWidget(self.resultaat_label)
        layout.addWidget(self.resultaat_label_droging)

    # bereken het resultaat van de invoer
    def bereken(self):
        try:
            # Eerst controleren of de velden niet leeg zijn
            if not self.number1.text() or not self.number2.text():
                self.resultaat_label.setText("Vul alle velden correct in")
                self.resultaat_label_droging.setText("2% droging: ")
                return
            #begrenzing van de oplage
            oplage = int(self.number1.text())
            if oplage < 1 or oplage > 1000000:
                self.resultaat_label.setText("Oplage moet tussen 0 en 1.000.001 vel zijn")
                self.resultaat_label_droging.setText("2% droging: ")
                return
            #begrenzing van de dekking
            dekking = int(self.number2.text())
            if dekking < 1 or dekking > 100:
                self.resultaat_label.setText("Dekking moet tussen 0 en 101 zijn")
                self.resultaat_label_droging.setText("2% droging: ")
                return

            oplage = int(self.number1.text())
            dekking = int(self.number2.text())

            # Kies de juiste inkt constante
            inkt_constante: float = 0.3 if oplage > 5000 else 0.4

            # Bepaal papierformaat waarde
            papierformaat_waarde: int = 100 if self.papierformaat.currentText() == "A3" else 200

            # Bereken resultaat
            resultaat: float = ((inkt_constante * dekking) * oplage) / papierformaat_waarde
            resultaat_droging: float = ((inkt_constante * dekking) * oplage) / 5000

            # Update resultaat label
            self.resultaat_label.setText(f"U moet {resultaat:.2f} gram mengen.")
            self.resultaat_label_droging.setText(f"2% droging: {resultaat_droging:.2f} gram.")
        except ValueError:
            self.resultaat_label.setText("Vul alle velden correct in")
            self.resultaat_label_droging.setText("2% droging: ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

