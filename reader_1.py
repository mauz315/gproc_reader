# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from tinydb import TinyDB, Query
import xlsxwriter

chromedriver = 'C:\\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)
browser.get("http://gproc.procalidad.gob.pe/")

username = browser.find_element_by_name("username")
password = browser.find_element_by_name("password")

username.send_keys("evaluador")
password.send_keys("gproc2015evaluador")

browser.find_element_by_xpath("//button[@type='submit']").click()

url = "http://gproc.procalidad.gob.pe/expresionInteresOld/?acev_id=711"
total_added = 0
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def make_soup(url):
    browser.get(url)
    html = browser.page_source
    return BeautifulSoup(html)

def main(url):
    global total_added
    db = TinyDB("db.json")

    while url:
        print ("Web Page: ", url)
        soup = soup_process(url, db)
        nextlink = soup.find("link", rel="next")

        url = False
        if (nextlink):
            url = nextlink['href']

    print ("Added ",total_added)

    make_excel(db)

def soup_process(url, db):
    global total_added

    soup = make_soup(url)
    results = soup.find_all("li", class_="result-row")

    for result in results:
        try:
            rec = {
                'pid': result['data-pid'],
                'date': result.p.time['datetime'],
                'cost': clean_money(result.a.span.string.strip()),
                'webpage': result.a['href'],
                'pic': clean_pic(result.a['data-ids']),
                'descr': result.p.a.string.strip(),
                'createdt': datetime.datetime.now().isoformat()
            }

            Result = Query()
            s1 = db.search(Result.pid == rec["pid"])

            if not s1:
                total_added += 1
                print ("Adding ... ", total_added)
                db.insert(rec)

        except (AttributeError, KeyError) as ex:
            pass

    return soup

def clean_money(amt):
    return int(amt.replace("$",""))

def clean_pic(ids):
    idlist = ids.split(",")
    first = idlist[0]
    code = first.replace("1:","")
    return "https://images.craigslist.org/%s_300x300.jpg" % code

def make_excel(db):
    Headlines = ["Pid", "Date", "Cost", "Webpage", "Pic", "Desc", "Created Date"]
    row = 0

    workbook = xlsxwriter.Workbook('motorcycle.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.set_column(0,0, 15) # pid
    worksheet.set_column(1,1, 20) # date
    worksheet.set_column(2,2, 7)  # cost
    worksheet.set_column(3,3, 10)  # webpage
    worksheet.set_column(4,4, 7)  # picture
    worksheet.set_column(5,5, 60)  # Description
    worksheet.set_column(6,6, 30)  # created date

    for col, title in enumerate(Headlines):
        worksheet.write(row, col, title)

    for item in db.all():
        row += 1
        worksheet.write(row, 0, item['pid'] )
        worksheet.write(row, 1, item['date'] )
        worksheet.write(row, 2, item['cost'] )
        worksheet.write_url(row, 3, item['webpage'], string='Web Page')
        worksheet.write_url(row, 4, item['pic'], string="Picture" )
        worksheet.write(row, 5, item['descr'] )
        worksheet.write(row, 6, item['createdt'] )

    workbook.close()

main(url)