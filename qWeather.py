import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from CoreCode import *


class ClickSelection(QGridLayout):
    def __init__(self, MaxColumn, boss):
        super().__init__()
        self.MaxColumn = MaxColumn
        self.boss = boss

    def clear(self):
        while self.count():
            self.takeAt(0).widget().setParent(None)

    def ProxyResponse(self, province, city, item):
        def response():
            if province is None:
                self.set(item)
            elif city is None:
                self.boss.CityNmaeInput.setText(item)
                self.boss.query()
                self.set()

        return response

    def set(self, province=None, city=None):
        self.clear()

        CurrentLevel = CityCodeTranslator().CityCode
        if province is not None:
            CurrentLevel = CurrentLevel[province]
        if city is not None:
            CurrentLevel = CurrentLevel[city]

        CurrentRow = 1
        CurrentColumn = 1
        for item in CurrentLevel:
            Currentbutton = QPushButton(item)
            Currentbutton.clicked.connect(self.ProxyResponse(province, city, item))
            self.addWidget(Currentbutton, CurrentRow, CurrentColumn)

            CurrentColumn += 1
            if CurrentColumn > self.MaxColumn:
                CurrentRow += 1
                CurrentColumn = 1
        if province is not None:
            Currentbutton = QPushButton("返回省级菜单")
            Currentbutton.clicked.connect(lambda: self.set())
            self.addWidget(Currentbutton, CurrentRow, CurrentColumn)


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.EnterInit()
        self.ClickInit()

        MainGrid = QGridLayout()
        MainGrid.setSpacing(10)

        MainGrid.addLayout(self.ClickGrid, 1, 1)
        MainGrid.addLayout(self.EnterGrid, 2, 1)

        self.setLayout(MainGrid)

        self.setWindowTitle("qWeather")
        self.setWindowIcon(QIcon("icon.png"))

        self.show()

    def ClickInit(self):
        self.ClickGrid = ClickSelection(5, self)
        self.ClickGrid.set()

    def EnterInit(self):
        # init widget
        CityLabel = QLabel("城市")
        WeatherStatusLabel = QLabel("天气状况")
        RegionLabel = QLabel("城区")

        self.CityNmaeInput = QLineEdit()
        self.CityNmaeInput.returnPressed.connect(self.query)
        self.WeatherStatusOutput = QLineEdit()
        self.WeatherStatusOutput.setReadOnly(True)

        self.CurrentCity = CityCodeTranslator()
        self.RegionSelection = QComboBox()
        self.RegionSelection.activated.connect(self.ChooseRegion)

        Querybutton = QPushButton("查询")
        Querybutton.clicked.connect(self.query)
        IPbutton = QPushButton("通过IP地址获取地理位置")
        IPbutton.clicked.connect(self.IPQuery)

        # init GUI
        self.EnterGrid = QGridLayout()
        self.EnterGrid.setSpacing(10)

        self.EnterGrid.addWidget(CityLabel, 1, 1)
        self.EnterGrid.addWidget(self.CityNmaeInput, 1, 2)

        self.EnterGrid.addWidget(RegionLabel, 2, 1)
        self.EnterGrid.addWidget(self.RegionSelection, 2, 2)

        self.EnterGrid.addWidget(WeatherStatusLabel, 3, 1)
        self.EnterGrid.addWidget(self.WeatherStatusOutput, 3, 2)

        self.EnterGrid.addWidget(Querybutton, 4, 1)
        self.EnterGrid.addWidget(IPbutton, 4, 2)

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
    MainProg = Main()
    sys.exit(app.exec_())
