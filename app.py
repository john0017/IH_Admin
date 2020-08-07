from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import json

app = Flask(__name__)
Bootstrap(app)

search_key = "ALPHA"   #should be dynamic when deployed
options = Options()
options.headless = True
browser = webdriver.Chrome("/Review_web/chromedriver", options=options)

missing_values = {}
mapped = {}
# check_list = []

def ad_id_map():
    for num in range(len(browser.find_elements_by_xpath('//*[@id="tableViewProperties"]/tbody/tr'))):
        address = browser.find_element_by_xpath('//*[@id="tableViewProperties"]/tbody/tr['+ str(num+1) + ']/td[1]').text
        uid = browser.find_element_by_xpath('//*[@id="tableViewProperties"]/tbody/tr['+ str(num+1) + ']').get_attribute("id")
        a_href = browser.find_element_by_xpath('/html/body/form/div[3]/main/div[2]/div[2]/div[4]/div/div[1]/div/table/tbody/tr['+ str(num+1) + ']/td[1]/a').get_attribute("href")
        href_id = a_href.split("&")[-2].split("=")[-1]
        mapped.update({address: (uid, href_id)})
    return mapped

def main_review():
    with open("id_map.json") as f:
        dict_ = json.load(f)
    for a, i in mapped.items():
        browser.get("https://portfolio.irishhomes.ie/Portal/ManageProperty.aspx?actionType=GET-PROPERTY-DETAILS&propertyCode=" + str(i[1]) + "&propertyId=" + str(i[0]))
        time.sleep(5)
        adres = browser.find_element_by_id("txtPropertyFullAddress").get_attribute("value").lower()
        if len(adres) ==0:
            print("Address not found")
        else:
            missing_values.update({adres: []})
        #     print(browser.find_element_by_id("txtPropertyFullAddress").get_attribute("value").lower())
            for master_key in dict_:
                for key, value in dict_[master_key].items():
                    try:
                        val = browser.find_element_by_id(value).get_attribute("value").lower()
                        if val == "0" or val == "not-set" or val == "not-selected" or val == " " or val == "nan" or val == "" or val == "none" or val == "none-selected" or val == "not-selected" or val == "€ 0":
                            missing_values[adres].append(key)
                            # check_list.append(key)
                    except NoSuchElementException as e:
                        print("error found")
                        print(master_key, " ", key, " ", value)

    # for a, i in mapped.items():
    #     browser.get("https://portfolio.irishhomes.ie/Portal/ManageProperty.aspx?actionType=GET-PROPERTY-DETAILS&propertyCode=" + str(i[1]) + "&propertyId=" + str(i[0]))
    #     time.sleep(5)   # every address takes 15min to load
    #     # print(browser.find_element_by_id("txtPropertyFullAddress").get_attribute("value").lower())
    #     for master_key in dict_:
    #         for key, value in dict_[master_key].items():
    #             try:
    #                 val = browser.find_element_by_id(value).get_attribute("value").lower()
    #                 if val == "0" or val == "not-set" or val == "not-selected" or val == " " or val == "nan" or val == "" or val == "none" or val == "none-selected" or val == "not-selected" or val == "€ 0":
    #                     check_list.append(key)
    #             except NoSuchElementException as e:
    #                 print("error found")
    #                 print(master_key, " ", key, " ", value)

@app.route('/review', methods=['GET', 'POST'])
def home():
    url = "https://portfolio.irishhomes.ie/Portal/ViewProperties.aspx"
    browser.get(url)
    # login
    browser.find_element_by_id('ContentPlaceHolder1_LoginUser_UserName').send_keys('jithin.john@irishhomes.ie')
    browser.find_element_by_id('ContentPlaceHolder1_LoginUser_Password').send_keys('irishhomes2020')
    browser.find_element_by_id('ContentPlaceHolder1_LoginUser_LoginButton').click()
    time.sleep(1)
    print("stage1")
    browser.get("https://portfolio.irishhomes.ie/Portal/ViewProperties.aspx")
    time.sleep(1)
    print("stage2")
    browser.find_element_by_id('btnMasterSearchButton').click()
    browser.find_element_by_id('page-header-search-input').send_keys(search_key)
    time.sleep(1)
    print("stage3")
    ad_id_map()
    print("stage4")
    main_review()
    print("stage5")
    browser.quit()
    return render_template('home.html', missing_values=missing_values)

if __name__== '__main__':
    app.run(debug='True')