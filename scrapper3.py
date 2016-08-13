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
        text = text.replace('Copyright', '')
        text = text.replace('copyright', '')
        text = re.sub("\d{4}", "", text)
        

    return text

def getAboutUs():
    xpath = "//a[contains(text(), 'About Us')]"
    ele = driver.find_element_by_xpath(xpath)
    if ele is not None:
        ele.click()
        textEle = driver.find_elements_by_xpath("//section[@id='aboutcontent']/div/div/div[2]/p")
        text = ''
        if textEle is not None:
            text = textEle[0].text
            text += textEle[1].text
        return text

def getContacts():
    xpath = "//a[contains(text(), 'Contact Us')]"
    ele = driver.find_element_by_xpath(xpath)
    if ele is not None:
        ele.click()
    contact = {}
    mailpath = "//a[contains(@href, 'mailto')]"
    mailEle = driver.find_element_by_xpath(mailpath)
    if mailEle is not None:
        contact['email'] = mailEle.text
    addresspath = "//div[@class='address clearfix']"
    addEle = driver.find_elements_by_xpath(addresspath)
    if addEle is not None:
        addEle1 = addEle[1].find_elements_by_tag_name("p")
        if addEle1 is not None:   
            contact['address'] = addEle1[0].text
            phone = addEle1[1]#.find_element_by_tag_name("span")
            if phone is not None:
                phone = phone.text
                phone = phone[phone.index('Tel:')+4:phone.index('|')]
                contact['phone'] = phone
            
        
    return contact

def getTeam():
    teampath = "//a[contains(text(), 'Team')]"
    teamele = driver.find_element_by_xpath(teampath)
    if teamele is not None:
        teamele.click()
    xpath = "//div[@id='photoNavigation']/ul/li"
    eles = driver.find_elements_by_xpath(xpath)
    teams = []
    for ele in eles:
        person = {}
        personEle = ele.find_element_by_tag_name("a")
        if personEle is not None:
            pEle = personEle.find_elements_by_tag_name("p")
            if pEle is not None:
                person['name'] = pEle[0].text
                person['designation'] = pEle[1].text
                teams.append(person)
    return teams
        
    

if __name__ == "__main__":
    url = "http://www.pelatro.com/"
    getURL(url)
    company = {}
    text =  getCompanyName()
    text.encode("utf-8")
    company['name'] =  repr(text)
    company['about'] =  getAboutUs()
    company['contacts'] =  getContacts()
    company['team'] = getTeam()
    print company
    driver.close()



    
    
    
