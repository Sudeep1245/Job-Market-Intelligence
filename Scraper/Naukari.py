from Baisc_sacrping_func import ScrapingClass
import time


#main homepage url 
main_homepage_url = "https://www.naukri.com/"

# main page form xpaths
xpath_for_search_bar = "//input[@placeholder='Enter skills / designations / companies']"
xpath_of_submit_button = "//div[@class='qsbSubmit']"



naukari = ScrapingClass(main_homepage_url)

naukari.accessing_url()
naukari.homepage_input_data('Data Science',xpath_input_box=xpath_for_search_bar,xpath_search_button=xpath_of_submit_button)



# apply filter code
naukari.dropdown_filter(dropdown_xpath='//*[@id="filter-freshness"]/i',value_xapth='''//*[@id="search-result-container"]/div[1]/div[1]/div/div/div[2]/div[14]/div[2]/div/div/ul/li[3]''')
filter_page_url = naukari.page_url()
print(filter_page_url)

salary_filter_dict =  {
    '0_to_3L' :"//label[@for='chk-0-3 Lakhs-ctcFilter-']//i[@class='ni-icon-unchecked']",
    '3L_to_6L' :"//label[@for='chk-3-6 Lakhs-ctcFilter-']//i[@class='ni-icon-unchecked']",
    '6L_to_10L' :"//label[@for='chk-6-10 Lakhs-ctcFilter-']//i[@class='ni-icon-unchecked']",
    '10L_to_15L' :"//label[@for='chk-10-15 Lakhs-ctcFilter-']//i[@class='ni-icon-unchecked']",
    '15L_to_25L' :"//label[@for='chk-15-25 Lakhs-ctcFilter-expanded']//i[@class='ni-icon-unchecked']",
    '25L_to_50L' :"//label[@for='chk-25-50 Lakhs-ctcFilter-expanded']//i[@class='ni-icon-unchecked']",
    '50L_to_75L' :"//label[@for='chk-50-75 Lakhs-ctcFilter-expanded']//i[@class='ni-icon-unchecked']",
    '75L_to_100L' :"//label[@for='chk-75-100 Lakhs-ctcFilter-expanded']//i[@class='ni-icon-unchecked']",
    '1Cr_to_5Cr' :"//label[@for='chk-1-5 Cr-ctcFilter-expanded']//i[@class='ni-icon-unchecked']",    
}

view_more_submit = "//div[contains(@class,'styles_filter-apply-btn__MDAUd')]"

viewmore_xpath = "//a[@id='ctcFilter']//span[contains(text(),'View More')]"
count=0
for salary_range,xpath in salary_filter_dict.items():
    naukari.single_checkbox_filter(xpath,view_more_xpath=viewmore_xpath,submit_xpath=view_more_submit)
    naukari.page_traversing_and_scraping(nextpage_button_xpath="//span[normalize-space()='Next']",data_class_name='srp-jobtuple-wrapper',salary_range=salary_range)
    time.sleep(5)
    naukari.reopen_page(filter_page_url)
    time.sleep(5)
naukari.extracted_data_output(data_name='Data_science_url')
print(len(naukari.data))