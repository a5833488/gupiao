import base64

from selenium import webdriver
from anticaptchaofficial.imagecaptcha import *


url = 'https://store.steampowered.com/join/?&snr=1_60_4__62'
if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.get(url)
    # el = driver.find_element_by_css_selector('.postTitle a')

    driver.find_element_by_id("email").send_keys("2251296517@qq.com")
    driver.find_element_by_id("reenter_email").send_keys("2251296517@qq.com")
    driver.find_element_by_id("country").send_keys("BL")
    # driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'myframe')]"))
    iframe = driver.find_element_by_xpath('//*[@id="captcha_entry_recaptcha"]/div/div/iframe')
    driver.switch_to_frame(iframe)
    driver.find_element_by_id('rc-anchor-container').click()

    html_text = driver.page_source
    iframe = driver.find_element_by_xpath('//*[@id="captcha_entry_recaptcha"]/div/div/iframe')
    driver.switch_to_frame(iframe)
    ss =  driver.find_element_by_id('//*/div/div[1]/iframe')

    print(html_text)
    image_file = open('D:\\test\\' + 'test.jpeg', 'wb')
    image_file.write("image")
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key("ac13a890ce94f5f4daf44c15e5a457de")
    id = solver.task_id
    captcha_text = solver.solve_and_return_solution('D:\\test\\test.jpeg')
    if captcha_text != 0:
        print ("captcha text " + captcha_text)
    else:
        print ("task finished with error " + solver.error_code)


    text =  requests.post(url='https://api.anti-captcha.com/getTaskResult',data={"clientKey":"ac13a890ce94f5f4daf44c15e5a457de",
    "taskId": id})
    print(text.content)
    captcha_text = solver.solve_and_return_solution('D:\\test\\test.jpeg')
    #
    #
    #
    if captcha_text != 0:
        print ("captcha text " + captcha_text)
    else:
        print ("task finished with error " + solver.error_code)

    # 点击第一篇博文标题
