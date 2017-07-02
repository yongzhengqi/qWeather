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
        IPBotton = QPushButton("通过IP地址获取地理位置")
        IPBotton.clicked.connect(self.IPQuery)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(city, 1, 1)
        grid.addWidget(self.CityNmaeInput, 1, 2)

        grid.addWidget(WeatherStatus, 2, 1)
        grid.addWidget(self.WeatherStatusOutput, 2, 2)

        grid.addWidget(QueryBotton, 3, 1)
        grid.addWidget(IPBotton, 3, 2)

        self.setLayout(grid)

        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle("qWeather")
        self.setWindowIcon(QIcon("icon.png"))
        self.show()

    def query(self):
        self.WeatherStatusOutput.setText("")
        CityName = self.CityNmaeInput.text()
        translator = CityCodeTranslator()

        try:
            CityCode = translator.GetCityCode(CityName)
        except:
            RaiseWarnings("数据库中没有查找到您居住的城市")
            return

        try:
            WeatherStatus = GetWeatherStatus(CityCode["中心城区"])
        except:
            RaiseWarnings("网络异常")
            return

        self.WeatherStatusOutput.setText(WeatherStatus)

    def IPQuery(self):
        try:
            ip = GetLocationFromIPAddress()
        except:
            RaiseWarnings("获取IP地址失败")
            return

        try:
            import json

            content = json.loads(URLRequest("http://freeapi.ipip.net/%s" % ip))
            self.CityNmaeInput.setText(content[2])
            self.query()
        except:
            RaiseWarnings("查询地理位置失败")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
