import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from CoreCode import *


class Main(QWidget):
    def __init__(self):
        super().__init__()

        city = QLabel("城市")
        WeatherStatus = QLabel("天气状况")

        self.CityNmaeInput = QLineEdit()
        self.CityNmaeInput.returnPressed.connect(self.query)

        self.WeatherStatusOutput = QLineEdit()
        self.WeatherStatusOutput.setReadOnly(True)

        QueryBotton = QPushButton("查询")
        QueryBotton.clicked.connect(self.query)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(city, 1, 1)
        grid.addWidget(self.CityNmaeInput, 1, 2)

        grid.addWidget(WeatherStatus, 2, 1)
        grid.addWidget(self.WeatherStatusOutput, 2, 2)

        grid.addWidget(QueryBotton, 3, 1, 1, 2)

        self.setLayout(grid)

        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle("qWeather")
        self.setWindowIcon(QIcon("icon.png"))
        self.show()

    def query(self):
        CityName = self.CityNmaeInput.text()
        translator = CityCodeTranslator()

        try:
            CityCode = translator.GetCityCode(CityName)
        except:
            MessageBox = QMessageBox()
            MessageBox.setIcon(QMessageBox.Warning)
            MessageBox.setText("数据库中没有查找到您居住的城市")
            MessageBox.setWindowTitle("Warning")
            MessageBox.exec_()
        else:
            WeatherStatus = GetWeatherStatus(CityCode["中心城区"])
            self.WeatherStatusOutput.setText(WeatherStatus)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
