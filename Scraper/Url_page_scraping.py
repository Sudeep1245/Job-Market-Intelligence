import pandas as pd
import numpy as np
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc



options = uc.ChromeOptions()

options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-notifications")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-component-update")
# options.add_argument(f'--proxy-server={proxy}')
options.add_argument("--disable-domain-reliability")
options.add_argument("--log-level=3")  # Suppresses most warnings 
# options.add_argument(f'user-agent={user_agent}')


# Initialize the driver once
driver = uc.Chrome(options=options,headless=False)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = { runtime: {} };
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
    """
})



wait = WebDriverWait(driver=driver,timeout=1)


complete_data = []



df = pd.read_csv('../data/whole_unique_url.csv')
total=1
count = 0
for row in df.itertuples(index=True, name='Row'):
    print(total)
    if total==10:
        pd.DataFrame(complete_data).to_csv(f'../data/scraped_output_{total}.csv', index=False)
        break

    salary= row.Salary
    link = row.Detail_link
    try:
        driver.get(link)

        try:
            read_more = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.styles_read-more-link__dD_5h')))
            read_more.click()
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        try:
            Company = driver.find_element(By.XPATH,'//*[@id="job_header"]/div[1]/div[1]/div/a').text
        except Exception as e:
            Company = np.nan

        try:
            Experiance = driver.find_element(By.CLASS_NAME,'styles_jhc__exp__k_giM').text
        except Exception as e:
            Experiance = np.nan


        try:
            City = driver.find_element(By.CLASS_NAME,'styles_jhc__location__W_pVs').text
        except Exception as e:
            City = np.nan


        try:
            Salary_Scrape = driver.find_element(By.CLASS_NAME,'styles_jhc__salary__jdfEC').text
            if Salary_Scrape == 'Not Disclosed':
                Salary_Scrape=salary
        except Exception as e:
            Salary_Scrape = np.nan


        try:
            Job_detail = []
            Job_data  = driver.find_elements(By.CLASS_NAME,'styles_details__Y424J')
            for row in Job_data:
                Job_detail.append(row.text)
        except Exception as e:
            Job_detail = np.nan

        try:
            Skill_list = []
            skill = driver.find_elements(By.CSS_SELECTOR, ".styles_chip__7YCfG.styles_clickable__dUW8S")
            for row in skill:
                try:
                    span = row.find_element(By.TAG_NAME, "span")
                    Skill_list.append(span.text)
                except Exception as e:
                    print(f"Could not extract span from link: {e}")
        except Exception as e:
            Skill_list = np.nan

        extracted_data_dict = {
            'company':Company,
            'experiance':Experiance,
            'city':City,
            'salary':Salary_Scrape,
            'job_detail':Job_detail,
            'required_skill':Skill_list
        }

        complete_data.append(extracted_data_dict)



        
    except Exception as e:
        count += 1
        print(e)

    total += 1

print('total_loop_count:',total)
print('error_row:',count)
print('total_correct_row_count',total-count)

def safe_del(self):
    try:
        if self.service.process:
            self.quit()
    except Exception:
        pass

uc.Chrome.__del__ = safe_del
driver.quit()
del driver  # Prevent __del__ from being called again

