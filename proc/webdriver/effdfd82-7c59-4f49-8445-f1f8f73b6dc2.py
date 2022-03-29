# wait for tab link to be clickable then click
driver = self.click_xpath(driver, wait, '/html/body/div[1]/nav/div/ul/li[3]/a')
driver = self.click_xpath(driver, wait, '/html/body/div[1]/nav/div/ul/li[3]/ul/li[1]/a')
# whole population coverage
driver = self.click_xpath(driver, wait, '//*[@id="all"]')
# show all data tables
elements = driver.find_elements(by=By.LINK_TEXT, value = 'Data Table')
for element in elements:
    element.click()
