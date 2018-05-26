import urllib2
import json
from pprint import pprint
from time import sleep
from multiprocessing import Process, Lock

url = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"

response = urllib2.urlopen(url)
data = json.load(response)

gameOrDlcCount = 0

def check(l, appId):

    global gameOrDlcCount

    appId = str(appId)
    l.acquire()
    detailLink = "https://store.steampowered.com/api/appdetails?key=7E776FB895E02F9B5DDF3451F3FD68E3&appids=" + str(
        appId)
    try:
        response = urllib2.urlopen(detailLink)
        appData = json.load(response)
        if "data" in appData[appId]:
            app = appData[appId]["data"]
            appType = app["type"]
            if appType == "game" or appType == "dlc":
                print str(appId) + ": " + app["name"]
                gameOrDlcCount += 1
    except urllib2.HTTPError, e:
        print "link: " + detailLink
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for index, value in enumerate(data["applist"]["apps"]):
        appId = value["appid"]
        Process(target=check, args=(lock, appId)).start()

# errorCount = 0
#
# def get(startIndex=0):
#
#     global gameOrDlcCount
#     global errorCount
#
#     for index, value in enumerate(data["applist"]["apps"], start=startIndex):
#         detailLink = "https://store.steampowered.com/api/appdetails?key=7E776FB895E02F9B5DDF3451F3FD68E3&appids=" + str(
#             value["appid"])
#         try:
#             response = urllib2.urlopen(detailLink)
#             appData = json.load(response)
#             appId = str(value["appid"])
#             if "data" in appData[appId]:
#                 app = appData[appId]["data"]
#                 appType = app["type"]
#                 if appType == "game" or appType == "dlc":
#                     print str(index) + ": " + app["name"]
#                     gameOrDlcCount += 1
#                     errorCount = 0
#         except urllib2.HTTPError, e:
#             print "Error Code: " + str(e.code)
#             sleepTime = 10
#             if errorCount > 0:
#                 sleepTime = 10 * errorCount
#             errorCount += 1
#             print "Limit extended, sleeping " + str(sleepTime) + " secs.."
#             sleep(sleepTime)
#             print "Continues.."
#             get(index)
#
# get(0)

print "Complete..."
print "Total Apps: " + str(len(data["applist"]["apps"]))
print "Game or DLC count: " + str(gameOrDlcCount)