from selenium import webdriver
import re

driver= webdriver.Firefox()


def getURL(url):
    if 'http://' not in url:
        url = 'http://' + url
    driver.get(url)


def getCompanyName():
    xpath = "//*[contains(text(), 'Copyright')]"
    textEle = driver.find_element_by_xpath(xpath)

    text = "test"
    if textEle is not None:
        text = textEle.text
        ##text.replace('&copy;', '')
        text.replace('Copyright', '')
        text.replace('copyright', '')
        

    return text

def getAboutUs():
    xpath = "//a[contains(text(), 'About Us')]"
    ele = driver.find_element_by_xpath(xpath)
    if ele is not None:
        ele.click()
        driver.switch_to.frame(driver.find_element_by_id("modal-content"))
        textEle = driver.find_element_by_xpath("//div[@class='modal-body']/p")
        text = ''
        if textEle is not None:
            text = textEle.text
        driver.switch_to.default_content()
        return text

def getContacts():
    driver.get("http://wisecells.com/contact-us/")
    xpath = "//*[@id='nav-change']//b"
    ele = driver.find_elements_by_xpath(xpath)
    contact = []
    if ele is not None:
        email = ele[0].text
        phone = ele[1].text
        contact.append(email)
        contact.append(phone)

    addressPath = "//*[contains(text(), 'our offices')]/parent::div/p"
    addressEle = driver.find_elements_by_xpath(addressPath)
    address = {}
    for addEle in addressEle:
        officeEle = addEle.find_element_by_tag_name("b")
        if officeEle is not None:
            office = officeEle.text
            location = addEle.text
            address[office] = location
    contact.append(address)
        
    return contact
    

if __name__ == "__main__":
    url = "wisecells.com"
    getURL(url)
    company = {}
    text =  getCompanyName()
    text.encode("utf-8")
    company['name'] =  repr(text)
    company['about'] =  getAboutUs()
    company['contacts'] =  getContacts()
    print company
    driver.close()



    
    
    
