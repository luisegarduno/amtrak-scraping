# Importing libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from undetected_chromedriver import Chrome
import csv
import time
import argparse

def parse_var(s):
    items = s.split('=')
    key = items[0].strip() # we remove blanks around keys, as is logical
    if len(items) > 1:
        # rejoin the rest:
        value = '='.join(items[1:])
    return (key, value)

def parse_vars(items):
    d = {}

    if items:
        for item in items:
            key, value = parse_var(item)
            d[key] = value
    return d


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', metavar='KEY=VALUE', nargs='+')
    args = parse_vars(parser.parse_args().a)
    date = args.get('date').split('-')
    year, month, day = date
    date = '/'.join([month, day, year])

    # Initializing selenium
    driver = Chrome()
    actions = ActionChains(driver)

    # Open website
    website_url = 'https://www.amtrak.com/home.html'
    driver.get(website_url)
    # Accept cookies
    actions.send_keys(Keys.ENTER).perform()
    driver.get(website_url)

    # Get search queries
    from_ = args.get('from')
    to_ = args.get('to')
    date = args.get('date').split('-')
    year, month, day = date
    date = '/'.join([month, day, year])

    # Fill inputs
    driver.find_element(By.CSS_SELECTOR, '#mat-input-0').send_keys(from_)
    driver.find_element(By.CSS_SELECTOR, '#mat-input-1').send_keys(to_)
    driver.find_element(By.CSS_SELECTOR, '#mat-input-2').send_keys(date)
    driver.find_element(By.CSS_SELECTOR, '.pl-lg-3').click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '.pl-lg-3').click()
    time.sleep(3)

    # Get results
    elements = driver.find_elements(By.CSS_SELECTOR, '.search-results-leg')
    results = []
    for element in elements:
        try:
            train = element.find_elements(By.CSS_SELECTOR, '.handpointer')[1].text
        except:
            train = element.find_element(By.CSS_SELECTOR, '.pt-1.ng-star-inserted span').text
        depart = element.find_element(By.CSS_SELECTOR, '.departure-inner .font-light').text
        depart += element.find_element(By.CSS_SELECTOR, '.departure-inner .time-period').text
        travel_elements = element.find_elements(By.CSS_SELECTOR, '.travel-time .text-center')
        travel_time = '\n'.join([e.text for e in travel_elements])
        arrive = element.find_element(By.CSS_SELECTOR, '.arrival-inner .font-light').text
        arrive += element.find_element(By.CSS_SELECTOR, '.arrival-inner .time-period').text
        arrive += '\n' + element.find_element(By.CSS_SELECTOR, '.travel-next-day span').text
        try:
            coach_from = element.find_element(By.CSS_SELECTOR, '.text-center:nth-child(1) .amount').text
        except:
            coach_from = None
        try:
            business_form = element.find_element(By.CSS_SELECTOR, '.text-center:nth-child(2) .amount').text
        except:
            business_form = None
        try:
            rooms_from = element.find_element(By.CSS_SELECTOR, '.text-center:nth-child(3) .amount').text
        except:
            rooms_from = None
        data = {'Train': train, 'Depart time': depart, 'Travel time': travel_time, 'Arrive time': arrive, 'Coach from': coach_from, 'Business form': business_form, 'Rooms from': rooms_from}
        print(data)
        results.append(data)
    
    # Save results in a csv flie
    print(results)
    keys = results[0].keys()
    with open('results.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
