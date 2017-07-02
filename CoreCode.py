class CityCodeTranslator:
    def __init__(self):
        CityCodeData = open("CityCode.data", "r").readlines()

        self.CityCode = {}
        for CurrentLine in CityCodeData:
            CurrentLineWords = CurrentLine.split()

            province = CurrentLineWords[3]
            city = CurrentLineWords[2]
            region = CurrentLineWords[1]
            code = int(CurrentLineWords[0])
            if region == city:
                region = "中心城区"

            if (province in self.CityCode) == False:
                self.CityCode[province] = {}
            assert (province in self.CityCode)
            if (city in self.CityCode[province]) == False:
                self.CityCode[province][city] = {}
            self.CityCode[province][city][region] = code

    def GetCityCode(self, name):
        for province in self.CityCode:
            for city in self.CityCode[province]:
                if name == city:
                    return self.CityCode[province][city]
        raise Exception("找不到您居住的城市")


def URLRequest(url):
    import urllib.request

    content = urllib.request.urlopen(url).read()
    return content.decode("utf-8")


def GetWeatherStatus(code):
    import json

    WeatherStatus = json.loads(URLRequest("http://www.weather.com.cn/data/cityinfo/%d.html" % code))
    WeatherStatus = WeatherStatus["weatherinfo"]
    return "%s\n%s ~ %s\n" % (WeatherStatus["weather"], WeatherStatus["temp1"], WeatherStatus["temp2"])


def GetLocationFromIPAddress():
    content = URLRequest("http://txt.go.sohu.com/ip/soip")
    import re
    ip = re.findall(r"\d+.\d+.\d+.\d+", content)
    return ip[0]


def RaiseWarnings(info):
    from PyQt5.QtWidgets import QMessageBox
    MessageBox = QMessageBox()
    MessageBox.setIcon(QMessageBox.Warning)
    MessageBox.setText(info)
    MessageBox.setWindowTitle("Warning")
    MessageBox.exec_()
