import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from CoreCode import *


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.InitWidget()
        self.InitGUI()

    def InitWidget(self):
        self.city = QLabel("城市")
        self.WeatherStatus = QLabel("天气状况")
        self.region = QLabel("城区")

        self.CityNmaeInput = QLineEdit()
        self.CityNmaeInput.returnPressed.connect(self.query)
        self.WeatherStatusOutput = QLineEdit()
        self.WeatherStatusOutput.setReadOnly(True)

        self.CurrentCity = CityCodeTranslator()
        self.RegionSelection = QComboBox()
        self.RegionSelection.activated.connect(self.ChooseRegion)

        self.QueryBotton = QPushButton("查询")
        self.QueryBotton.clicked.connect(self.query)
        self.IPBotton = QPushButton("通过IP地址获取地理位置")
        self.IPBotton.clicked.connect(self.IPQuery)

    def InitGUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.city, 1, 1)
        grid.addWidget(self.CityNmaeInput, 1, 2)

        grid.addWidget(self.region, 2, 1)
        grid.addWidget(self.RegionSelection, 2, 2)

        grid.addWidget(self.WeatherStatus, 3, 1)
        grid.addWidget(self.WeatherStatusOutput, 3, 2)

        grid.addWidget(self.QueryBotton, 4, 1)
        grid.addWidget(self.IPBotton, 4, 2)

        self.setLayout(grid)

        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle("qWeather")
        self.setWindowIcon(QIcon("icon.png"))
        self.show()

    def ChooseRegion(self):
        self.WeatherStatusOutput.setText("")

        CurrentRegion = self.RegionSelection.currentText()
        CurrentRegionCode = self.CurrentCity[CurrentRegion]

        try:
            WeatherStatus = GetWeatherStatus(CurrentRegionCode)
        except:
            RaiseWarnings("网络异常")
            return

        self.WeatherStatusOutput.setText(WeatherStatus)

    def query(self):
        self.WeatherStatusOutput.setText("")
        self.RegionSelection.clear()

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

        for region in CityCode:
            self.RegionSelection.addItem(region)
        self.CurrentCity = CityCode

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
