import argparse
import datetime
import csv
import urllib.request
import re


def myCounts(myList):
    row_count = 0.0
    image_count = 0.0
    firefox_count = 0
    chrome_count = 0
    msie_count = 0
    safari_count = 0
    for row in myList:
        row_count += 1
        image_search = re.search('.*(\.jpg|\.gif|\.png)',row[0])
        if image_search is not None:
            image_count += 1
        if re.search('MSIE',row[2]):
            msie_count += 1
        elif re.search('Firefox',row[2]):
            firefox_count += 1
        elif re.search('Chrome', row[2]):
            chrome_count += 1
        elif re.search('Safari', row[2]):
            safari_count += 1
    image_percentage = (image_count / row_count) * 100
    browser_dict = {"MSIE":msie_count,"FireFox":firefox_count,"Chrome":chrome_count,"Safari":safari_count}
    print("Image requests account for", str(image_percentage) + chr(37), "of all requests")
    print("Browser Counts for reference:", browser_dict)
    print("The most popular browser is " + max(browser_dict,key=browser_dict.get))


def ExtraCredit(ECList):
    HourDict = dict()
    for row in ECList:
        d = datetime.datetime.strptime(row[1],"%Y-%m-%d %H:%M:%S")
        if d.hour not in HourDict:
            HourDict[d.hour] = 1
        else:
            HourDict[d.hour] += 1
    for myHour in HourDict:
        print("Hour " + str(myHour) + " has " + str(HourDict[myHour]) + " hits")


def downloadData(myURL):
    response = urllib.request.urlopen(myURL)
    lines = [l.decode('utf-8') for l in response.readlines()]
    myCSVlist = csv.reader(lines)
    myCounts(myCSVlist)
    response = urllib.request.urlopen(myURL)
    lines = [l.decode('utf-8') for l in response.readlines()]
    myCSVlist = csv.reader(lines)
    ExtraCredit(myCSVlist)
    

def main(url):
    print(f"Running main with URL = {url}...")
    downloadData(url)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)