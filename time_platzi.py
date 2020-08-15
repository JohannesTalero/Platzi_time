import pandas as pd
import numpy as np
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains



path='H:/2020-02/Platzi/Meta/'
user_w=pd.read_csv(path+'user_and_password.txt',sep=';')['user'][0]
password_w=pd.read_csv(path+'user_and_password.txt',sep=';')['password'][0]
pg_web_platzi='https://platzi.com'

goals_platzi_time=pd.read_csv(path+'Data_platzi_goals.csv')
del goals_platzi_time['Unnamed: 0']

#Driver initilizer
options=webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver= webdriver.Chrome(executable_path=r'H:/2020-02/How to find a new home with Scraping and game theory/chromedriver.exe',options=options)

#----------------- Open session ----------------------
url=pg_web_platzi+'/login/'
driver.get(url)
user=driver.find_element_by_xpath('//input[@name="email"]')
user.send_keys(user_w)

passw=driver.find_element_by_xpath('//input[@name="password"]')
passw.send_keys(password_w)

button_send=driver.find_element_by_xpath('//button[@class="btn-Green btn--md"]')
ActionChains(driver).click(button_send).perform()
#----------------------------------------------------

                                         


                                                           