#import city code from flies
city_code_data = open("city_code.data", "r").readlines()

#transform data from string(city_code_data) to dictionary(city_code)
city_code = {}
for i in range(len(city_code_data)):
    current_line_words = city_code_data[i].split()
    assert(len(current_line_words) == 4)
    if current_line_words[1] == current_line_words[2]:
        city_name = current_line_words[1]
        regions_of_this_city = {"中心城区": int(current_line_words[0])}
        for j in range(i + 1, len(city_code_data)):
            line_words = city_code_data[j].split()
            assert(len(line_words) == 4)
            if (line_words[2] == city_name):
                regions_of_this_city[line_words[1]] = int(line_words[0])
            else:
                break
        city_code[city_name] = regions_of_this_city
    else:
        continue

#define a function to process queries
def output_weather(code_of_the_city):
    assert(type(code_of_the_city) == int)
    url = "http://www.weather.com.cn/data/cityinfo/%d.html" % (code_of_the_city)
    json_content = urllib.request.urlopen(url).read()
    import json
    final_result = json.loads(json_content)
    assert ("weatherinfo" in final_result)
    final_result = final_result["weatherinfo"]
    print("%s\n%s ~ %s\n" % (final_result["weather"], final_result["temp1"], final_result["temp2"]))

#interact with users
import urllib.request
query_city = input("Please enter the name of your city\n")

if ((query_city in city_code) == False):
    print("sorry, but we can't find the city you live\n")
    input("please enter anything to exit")
    exit(0)
output_weather(city_code[query_city]["中心城区"])

if (len(city_code[query_city]) == 1):
    exit(0)
print("weather information shown above is the main region of the city")
print("this city also include following %d region" % (len(city_code[query_city]) - 1))
cnt_regions = 0
index_of_regions = {}
for region in city_code[query_city]:
    if (region == "中心城区"):
        continue
    else:
        cnt_regions = cnt_regions + 1
        index_of_regions[cnt_regions] = city_code[query_city][region]
        print("%d. %s" % (cnt_regions, region))
print("if you want to know the weather of a particular region")
print("please enter the index of the region or you can enter anything else to exit")
try:
    index = int(input())
    if index in index_of_regions:
        output_weather(index_of_regions[index])
        input("please enter anything to exit")
    else:
        exit(0)
except:
    exit(0)