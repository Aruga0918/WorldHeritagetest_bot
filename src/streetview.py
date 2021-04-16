from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
def tree(heritage):
    browser = webdriver.chrome(options=options)
    url = "https://www.google.co.jp/maps/preview"
    browser.get(url)
    searchbox = browser.find_element_by_id("searchboxinput")
    searchbox.send_keys(heritage)
    searchbtn = browser.find_element_by_id("searchbox-searchbutton")
    searchbtn.click()
    viewbtn = browser.find_element_by_xpath('//button[@aria-label="ストリートビューと 360° ビュー"]')
    viewbtn.click()
    cur_url = browser.current_url
    return cur_url

if __name__=="__main__":
    print(tree("サグラダファミリア"))