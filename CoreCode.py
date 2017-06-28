class CityCodeTranslator:
    def __init__(self):
        # import city code from flies
        CityCodeData = open("CityCode.data", "r").readlines()

        # transform data from string(CityCodeData) to dictionary(CityCode)
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

def GetWeatherStatus(code):
    import urllib.request
    url = "http://www.weather.com.cn/data/cityinfo/%d.html" % code

    json_content = urllib.request.urlopen(url).read()

    import json
    final_result = json.loads(json_content)
    final_result = final_result["weatherinfo"]
    return "%s\n%s ~ %s\n" % (final_result["weather"], final_result["temp1"], final_result["temp2"])
