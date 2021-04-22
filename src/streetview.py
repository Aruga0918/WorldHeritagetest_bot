from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib3.packages.six import b 
from time import sleep
options = Options()
options.add_argument('--headless')
def tree(heritage):
    browser = webdriver.Chrome('chromedriver.exe',options=options)
    url = "https://www.google.co.jp/maps/preview"
    browser.get(url)
    sleep(1)
    searchbox = browser.find_element_by_id("searchboxinput")
    searchbox.send_keys(heritage)
    searchbtn = browser.find_element_by_id("searchbox-searchbutton")
    sleep(1)
    searchbtn.click()
    sleep(10)
    height = browser.execute_script("return document.body.scrollHeight") // 2
    browser.execute_script("window.scrollTo(0, "+str(height)+");")
    browser.refresh()
    sleep(10)
    viewbtn = browser.find_element_by_xpath("//*[@aria-label='ストリートビューと 360° ビュー']")
    # viewbtn =browser.find_elements_by_css_selector("[aria-label=ストリートビューと 360° ビュー]")
    # viewbtn = browser.find_element_by_class_name('kdFz2y0CdKp__section-carouselphoto-photo-container')
    viewbtn.click()
    sleep(10)
    cur_url = browser.current_url
    return cur_url

if __name__=="__main__":
    print(tree("イエローストーン国立公園"))