import sys
import math
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QPushButton, QLineEdit, QStackedLayout, QTextEdit
)
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mathgical")
        self.setGeometry(100, 100, 400, 600)

        self.dark_mode = False
        self.memory = 0

        self.create_ui()

    def create_ui(self):
        self.main_layout = QVBoxLayout()

        # Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(60)
        self.display.setStyleSheet("font-size: 22px; padding: 10px;")
        self.display.returnPressed.connect(self.calculate)

        self.main_layout.addWidget(self.display)

        # Top buttons
        top_layout = QGridLayout()

        self.mode_btn = QPushButton("Scientific")
        self.mode_btn.clicked.connect(self.toggle_mode)

        self.theme_btn = QPushButton("🌙 Dark")
        self.theme_btn.clicked.connect(self.toggle_theme)

        self.clear_history_btn = QPushButton("Clear History")
        self.clear_history_btn.clicked.connect(self.clear_history)

        top_layout.addWidget(self.mode_btn, 0, 0)
        top_layout.addWidget(self.theme_btn, 0, 1)
        top_layout.addWidget(self.clear_history_btn, 0, 2)

        self.main_layout.addLayout(top_layout)

        # Memory buttons
        memory_layout = QGridLayout()
        mem_buttons = ['MC', 'MR', 'M+', 'M-']

        for i, text in enumerate(mem_buttons):
            btn = QPushButton(text)
            btn.setFixedSize(75, 50)
            btn.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; border-radius: 8px;")
            btn.clicked.connect(self.handle_memory)
            memory_layout.addWidget(btn, 0, i)

        self.main_layout.addLayout(memory_layout)

        # History
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setFixedHeight(120)
        self.history.setStyleSheet("font-size: 14px;")
        self.main_layout.addWidget(self.history)

        # Stack layout
        self.stack = QStackedLayout()

        # -------- NORMAL PANEL --------
        normal_widget = QWidget()
        normal_grid = QGridLayout()

        normal_buttons = [
            ('7',0,0),('8',0,1),('9',0,2),('/',0,3),
            ('4',1,0),('5',1,1),('6',1,2),('*',1,3),
            ('1',2,0),('2',2,1),('3',2,2),('-',2,3),
            ('0',3,0),('.',3,1),('=',3,2),('+',3,3),
            ('C',4,0)
        ]

        for text, r, c in normal_buttons:
            btn = QPushButton(text)
            btn.setFixedSize(75, 75)

            if text == "=":
                btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; border-radius: 10px;")
            elif text == "C":
                btn.setStyleSheet("background-color: #f44336; color: white; font-size: 16px; border-radius: 10px;")
            elif text in "+-*/":
                btn.setStyleSheet("background-color: #ff9800; color: white; font-size: 16px; border-radius: 10px;")
            else:
                btn.setStyleSheet("font-size: 16px; border-radius: 10px;")

            btn.clicked.connect(self.on_click)
            normal_grid.addWidget(btn, r, c)

        normal_widget.setLayout(normal_grid)

        # -------- SCIENTIFIC PANEL --------
        sci_widget = QWidget()
        sci_grid = QGridLayout()

        sci_buttons = [
            ('sin',0,0), ('cos',0,1), ('tan',0,2), ('√',0,3),
            ('log',1,0), ('π',1,1), ('e',1,2), ('^',1,3),
            ('x²',2,0), ('x³',2,1), ('Back',3,0)
        ]

        for text, r, c in sci_buttons:
            btn = QPushButton(text)
            btn.setFixedSize(75, 75)

            if text == "Back":
                btn.setStyleSheet("background-color: #607d8b; color: white; font-size: 16px; border-radius: 10px;")
                btn.clicked.connect(self.toggle_mode)
            else:
                btn.setStyleSheet("background-color: #9c27b0; color: white; font-size: 16px; border-radius: 10px;")
                btn.clicked.connect(self.on_scientific_click)

            sci_grid.addWidget(btn, r, c)

        sci_widget.setLayout(sci_grid)

        self.stack.addWidget(normal_widget)
        self.stack.addWidget(sci_widget)

        self.main_layout.addLayout(self.stack)
        self.setLayout(self.main_layout)

    def toggle_mode(self):
        if self.stack.currentIndex() == 0:
            self.stack.setCurrentIndex(1)
            self.mode_btn.setText("Basic")
        else:
            self.stack.setCurrentIndex(0)
            self.mode_btn.setText("Scientific")

    def toggle_theme(self):
        if not self.dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: white; }
                QLineEdit, QTextEdit { background-color: #3c3c3c; color: white; }
                QPushButton { background-color: #444; color: white; border-radius: 8px; }
                QPushButton:hover { background-color: #555; }
            """)
            self.theme_btn.setText("☀ Light")
        else:
            self.setStyleSheet("")
            self.theme_btn.setText("🌙 Dark")

        self.dark_mode = not self.dark_mode

    def handle_memory(self):
        action = self.sender().text()

        try:
            value = float(self.display.text())
        except:
            value = 0

        if action == "MC":
            self.memory = 0
        elif action == "MR":
            self.display.setText(str(self.memory))
        elif action == "M+":
            self.memory += value
        elif action == "M-":
            self.memory -= value

    def clear_history(self):
        self.history.clear()

    def on_click(self):
        text = self.sender().text()

        if text == "=":
            self.calculate()
        elif text == "C":
            self.display.clear()
        else:
            self.display.setText(self.display.text() + text)

    def on_scientific_click(self):
        text = self.sender().text()

        mapping = {
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "log": "log(",
            "√": "sqrt(",
            "π": "pi",
            "e": "e",
            "x²": "**2",
            "x³": "**3",
            "^": "^"
        }

        self.display.setText(self.display.text() + mapping.get(text, ""))

    def calculate(self):
        try:
            expression = self.display.text()

            # 🔧 Fix leading zeros
            expression = re.sub(r'\b0+(\d+)', r'\1', expression)

            expression = expression.replace("^", "**")
            expression = expression.replace("π", "pi")

            allowed = {
                "sin": lambda x: math.sin(math.radians(x)),
                "cos": lambda x: math.cos(math.radians(x)),
                "tan": lambda x: math.tan(math.radians(x)),
                "log": math.log10,
                "sqrt": math.sqrt,
                "pi": math.pi,
                "e": math.e
            }

            result = eval(expression, {"__builtins__": None}, allowed)
            result = round(result, 3)

            self.history.append(f"{expression} = {result}")
            self.display.setText(str(result))

        except:
            self.display.setText("Error")

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.calculate()
        elif event.key() == Qt.Key_Backspace:
            self.display.backspace()
        elif event.key() == Qt.Key_Delete:
            self.display.clear()
        else:
            text = event.text()
            if text in "0123456789.+-*/()":
                self.display.setText(self.display.text() + text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())