class CityCodeTranslator:
    def __init__(self):
        CityCodeJson = open("CityCode.json", "r").read()

        import json
        self.CityCode = json.loads(CityCodeJson)

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
