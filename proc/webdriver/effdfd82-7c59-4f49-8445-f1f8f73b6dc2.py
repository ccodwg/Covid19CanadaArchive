# wait for tab link to be clickable then click
self.click_xpath(wait, '/html/body/div[1]/nav/div/ul/li[3]/a')
self.click_xpath(wait, '/html/body/div[1]/nav/div/ul/li[3]/ul/li[1]/a')
# whole population coverage
self.click_xpath(wait, '//*[@id="all"]')
# show all data tables
elements = self.wd.find_elements(by=By.LINK_TEXT, value = 'Data Table')
for element in elements:
    element.click()
