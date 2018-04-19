#import pandas as pd

from selenium import webdriver

from selenium.webdriver.common.keys import Keys




chromedriver = 'C:\\chromedriver.exe'

browser = webdriver.Chrome(chromedriver)

browser.get("http://gproc.procalidad.gob.pe/")


element1 = browser.find_element_by_name("username")

element2 = browser.find_element_by_name("password")


element1.send_keys("evaluador")

element2.send_keys("gproc2015evaluador")


browser.find_element_by_xpath("//button[@type='submit']").click()


browser.get("http://gproc.procalidad.gob.pe/expresionInteresOld/?acev_id=711")


#url = 'http://gproc.procalidad.gob.pe/expresionInteresOld/?acev_id=711'


#for i, df in enumerate(pd.read_html(url)):

#df.to_csv('myfile_%s.csv' % i)

# html = browser.get("http://gproc.procalidad.gob.pe/expresionInteresOld/?acev_id=711").content

# df_list = pd.read_html(html)
# df = df_list[-1]
# print(df)

#df.to_csv('my data.csv')
