import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://www.dmart.in/")
driver.maximize_window()
search_box = driver.find_element(By.ID, "pincodeInput")
search_text = '500081'   #Can be changed accordingly
search_box.send_keys(search_text)

wait = WebDriverWait(driver, 10)
dropdown_locator = (By.XPATH, "/html/body/div[2]/div[3]/div/div[2]/div/div/div[2]/div/ul/li/button")
dropdown_options = wait.until(EC.visibility_of_all_elements_located(dropdown_locator))

if dropdown_options:
    dropdown_options[0].click()

driver.implicitly_wait(10)

select_shopping_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[2]/div/div/div[3]/div/div[2]/div[2]/button")
select_shopping_button.click()
time.sleep(15)

wait = WebDriverWait(driver, 10)
all_categories_locator = (By.CLASS_NAME, "categories-header_listStaticItemLink__ePZaj")
all_categories = wait.until(EC.element_to_be_clickable(all_categories_locator))
time.sleep(15)

all_categories.click()
time.sleep(15)

category = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/header/div/div[3]/div[1]/div[2]/div/div[3]/a[1]')
category.click()
time.sleep(15)

sub_category = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div[1]/nav/div[3]')
time.sleep(15)
sub_category.click()
time.sleep(15)

category_elements = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/main/div/div/div[1]/nav/div[2]/p')
total_categories = category_elements.text.split(' ')
len_total_categories = total_categories[1].replace('(', '').replace(')', '')
time.sleep(5)
element_items = driver.find_elements(by=By.XPATH,value='//*[@class="MuiList-root navigation-list_listNested__V8mkH mui-style-1uzmcsd"]/div')
element_items_names=driver.find_elements(by=By.XPATH,value='//*[@class="MuiList-root navigation-list_listNested__V8mkH mui-style-1uzmcsd"]/*/p')
time.sleep(5)
lister = []
ele_names=[]
for z in range(len(element_items_names)):
    element_items_names = driver.find_elements(by=By.XPATH,value='//*[@class="MuiList-root navigation-list_listNested__V8mkH mui-style-1uzmcsd"]/*/p')
    ele_names.append(element_items_names[z].text)
for i in range(len(element_items)):
    element_items = driver.find_elements(by=By.XPATH,value='//*[@class="MuiList-root navigation-list_listNested__V8mkH mui-style-1uzmcsd"]/div')
    element_items[i].click()
    time.sleep(10)
    cat_list_el = driver.find_elements(by=By.XPATH, value='//*[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 mui-style-tuxzvu"]/div')
   # print(len(cat_list_el))
    for j in range(len(cat_list_el)):
        cat_list_el = driver.find_elements(by=By.XPATH, value='//*[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 mui-style-tuxzvu"]/div')
        time.sleep(4)
        cat_list_el[j].click()
        time.sleep(10)
        driver.implicitly_wait(20)
        listbox_element = driver.find_element(By.CLASS_NAME, 'variants-component_variants-container__kO1pk')
        listbox_items = listbox_element.find_elements(By.CLASS_NAME, 'variants-component_volume__5KpID')
        time.sleep(1)
        for k in range(len(listbox_items)):
            li = []
            time.sleep(1)
            path = driver.find_elements(By.CLASS_NAME, 'variants-component_volume__5KpID')
            time.sleep(5)
            path[k].click()
            time.sleep(10)
            element = driver.find_elements(by=By.XPATH, value='//*[@id="__next"]/div[@class="layout_container__ojOIi"]/main/div/div/div[@class="common_product-section__r1Moi"]/div[@ class="image-gallery_component_gallery-panel__7hDF1"]/div/div[@class="image-gallery_component_info__e2_Aa"]')
            element_items_names = driver.find_elements(by=By.XPATH,
                                                       value='//*[@class="MuiList-root navigation-list_listNested__V8mkH mui-style-1uzmcsd"]/*/p')
            cat_list_el = driver.find_elements(by=By.XPATH,
                                               value='//*[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 mui-style-tuxzvu"]/div')
            li.append(search_text)
            li.append(total_categories[0])
            li.append(ele_names[i])
            item_name = driver.find_element(By.XPATH, ('//*[@id="__next"]/div[1]/main/div/div/div[2]/div[@class="common_product-info__cMBch"]/h1/span[@class="text-label-component_title__TpDIk"]'))
            li.append(item_name.text)
            variant= driver.find_element(By.XPATH,('//*[@id="__next"]/div[1]/main/div/div/div[2]/div[@class="common_product-info__cMBch"]/h1/span[2]'))
            li.append(variant.text)
            market_prices = driver.find_elements(By.CLASS_NAME, 'price-details-component_value__IIJeF')
            market_price = market_prices[0]
            li.append(market_price.text)
            dmart_price = market_prices[1]
            li.append(dmart_price.text)

            if element:
                li.append('NO')
            else:
                li.append('YES')

            lister.append(li)
            time.sleep(15)
            #print(li)
            time.sleep(5)

        driver.back()
        time.sleep(10)

time.sleep(10)
driver.close()

df=pd.DataFrame(lister,columns=['Pincode','Category','SubCategory','Item','Variant','MRP','Dmart_Price','In-Stock'])
df.to_csv('DMART_Bevarages.csv')

