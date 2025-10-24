import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd




options = Options()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-notifications')
options.add_argument('--disable-background-networking')
options.add_argument('--disable-component-update')
options.add_argument('--disable-domain-reliability')
options.add_argument("--log-level=3")  # Suppresses most warnings 



class ScrapingClass:

    # creating a Driver with basic code
    def __init__(self,url,wait_time=3):
        self.driver = webdriver.Chrome(options=options)
        self.url = url
        self.wait = WebDriverWait(self.driver,wait_time)
        self.data = []

    def accessing_url(self):
        self.driver.get(self.url)
        self.driver.maximize_window()

    def page_url(self):
        return self.driver.current_url
    
    def reopen_page(self,url=None):
        self.driver.get(url)

    def wait_until_page_get_load(self,wait):
        current_page_title = self.driver.title
        try:
            time.sleep(2)
            wait.until(
                lambda d : d.execute_script('return document.readyState')=='complete'
            )
        except:
            print(f'The webpage "{current_page_title}" did not get fully load.')

    def homepage_input_data(self,job_field,xpath_input_box,xpath_search_button,time_sleep=3):
        search_box = self.driver.find_element(by=By.XPATH,value=xpath_input_box)
        for letter in job_field:
            search_box.send_keys(letter)
            time.sleep(0.2)
        submit =  self.driver.find_element(by=By.XPATH,value=xpath_search_button)
        submit.click()
        time.sleep(time_sleep)

    def is_element_visible(self,element):
        return self.driver.execute_script("""
            const el = arguments[0];
            const style = window.getComputedStyle(el);
            return (
            style.display !== 'none' &&
            style.visibility !== 'hidden' &&
            el.offsetParent !== null);""", element)
    
    def dropdown_filter(self,dropdown_xpath,value_xapth,time_sleep=2):
        dropdown = self.driver.find_element(By.XPATH,value=dropdown_xpath) # This line is for finding the drop down feature on page
        self.driver.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top - 100);",dropdown)
        if self.is_element_visible(dropdown):
            dropdown.click()
            time.sleep(1)
            value = self.driver.find_element(By.XPATH,value=value_xapth) # This line is for selecting the option from dropdown values
            value.click()
            self.wait_until_page_get_load(self.wait)
            time.sleep(time_sleep)
        else :
            print("Driver is unable to find the dropdown")
            time.sleep(time_sleep)


    def single_checkbox_filter(self,checkBox=None,sleep_time=1,view_more_xpath=None,submit_xpath=None):
        try:
            time.sleep(1)
            try:
                check_option = self.driver.find_element(By.XPATH,checkBox)
                if self.is_element_visible(check_option):
                    check_option.click()
                    time.sleep(sleep_time)
            
            except:
                view_more = self.driver.find_element(By.XPATH,view_more_xpath)
                view_more.click()
                time.sleep(sleep_time)  
                self.wait_until_page_get_load(self.wait)
                check_option = self.driver.find_element(By.XPATH,checkBox)
                check_option.click()
                more_submit = self.driver.find_element(By.XPATH,submit_xpath)
                more_submit.click()
                time.sleep(sleep_time)
            
        except Exception as e:
            print(e)

    def loading_fullpage_till_nextpage_(self,element):
        try:
            self.driver.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top - 100);",element)
            time.sleep(2)
        except:
            print(f'Failed to find the next_page element .')

    def data_scraping(self,data_classname=None,salary_range=None):
        data_bars = self.driver.find_elements(By.CLASS_NAME,data_classname)
        try:
            for bar in data_bars:
                job_title = bar.find_element(By.CLASS_NAME,'title').text
                company = bar.find_element(By.CSS_SELECTOR,'div.row2 > span > a').text
                job_detail_link = bar.find_element(By.CSS_SELECTOR,'div.row1 > h2 > a.title').get_attribute('href') 
                self.data.append({'Company':company,
                                'Job_title':job_title,
                                'Salary':salary_range,
                                'Detail_link':job_detail_link})
        except Exception as e:
            print(e)

    def page_traversing_and_scraping(self, nextpage_button_xpath=None,data_class_name=None,salary_range=None):
        try:
            self.wait_until_page_get_load(self.wait)
            count_page = 0
            while True:
                try:
                    count_page += 1
                    next_page_button = self.driver.find_element(By.XPATH, nextpage_button_xpath)
                    self.loading_fullpage_till_nextpage_(next_page_button)
                    self.data_scraping(data_classname=data_class_name,salary_range=salary_range)
                    next_page_button.click()
                    time.sleep(1)
                    self.wait_until_page_get_load(self.wait)
                except Exception as inner_e:
                    print(f'Traverse through the :"{self.driver.title}" ,Page Number : {count_page}')
                    break

        except Exception as e:
            print(f'We completed traversing to complete page: {e}')

    def extracted_data_output(self,data_name=None):
        df = pd.DataFrame(self.data)
        df.to_csv(f'{data_name}.csv', index=False)


    
