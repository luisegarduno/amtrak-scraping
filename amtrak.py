# Importing libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from undetected_chromedriver import Chrome
import csv
import time
import argparse
months_31 = [1, 3, 5, 7, 8, 10, 12]
months_30 = [4, 6, 9, 11]

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
    date = args.get('start_date').split('-')
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

    start_date = args.get('start_date').split('-')
    start_year, start_month, start_day = start_date
    start_date = '/'.join([str(int(start_month)), str(int(start_day)), str(int(start_year))])  # start date

    end_date = args.get('end_date').split('-') #end date
    end_year, end_month, end_day = end_date
    end_date = '/'.join([str(int(end_month)), str(int(end_day)), str(int(end_year))])

    p = int(args.get('people'))

    # Fill inputs
    driver.find_element(By.CSS_SELECTOR, '#mat-input-0').send_keys(from_)
    driver.find_element(By.CSS_SELECTOR, '#mat-input-1').send_keys(to_)
    driver.find_element(By.CSS_SELECTOR, '#mat-input-2').send_keys(start_date)
    driver.find_element(By.CSS_SELECTOR, '.t-title').click()
    while p > 1:
        driver.find_element(By.CSS_SELECTOR, '.increment').click()
        p -= 1
    driver.find_element(By.CSS_SELECTOR, '.pl-lg-3').click()
    time.sleep(1)


    # Get results for the first day
    elements = driver.find_elements(By.CSS_SELECTOR, '.search-results-leg')
    results = []
    opt_results = []
    multiple_trains = []
    for element in elements:
        try:
            train = element.find_element(By.CSS_SELECTOR, '.pt-1.ng-star-inserted span').text + ' ' + element.find_elements(By.CSS_SELECTOR, '.handpointer')[1].text
        except:
            train = element.find_element(By.CSS_SELECTOR, '.pt-1.ng-star-inserted span').text
        # if train != "Mixed Service":
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
            coach_from = 'None'
        try:
            business_from = element.find_element(By.CSS_SELECTOR, '.text-center:nth-child(2) .amount').text
        except:
            business_from = 'None'
        try:
            rooms_from = element.find_element(By.CSS_SELECTOR, '.text-center:nth-child(3) .amount').text
        except:
            rooms_from = 'None'
            """if train == "Multiple Trains":
                element.find_element(By.CSS_SELECTOR, '.details-dropdown.mt-2').click()
                element.find_element(By.CSS_SELECTOR, 'ul > li:nth-child(2) > a').click()
                time.sleep(3)
                multiple_trains.append(element.find_element(By.CSS_SELECTOR, '.tab-pane > div:nth-child(1) .row.segment-details.ng-star-inserted .travel-type .travel-type-service > span > span').text)
                multiple_trains.append(element.find_element(By.CSS_SELECTOR, '.tab-pane > div:nth-child(2) .row.segment-details.ng-star-inserted .travel-type .travel-type-service > span > span').text)
                print(multiple_trains)
                train = ', '.join([i for i in multiple_trains])"""

        data = {'Date': start_date, 'Train': train, 'Depart time': depart, 'Travel time': travel_time, 'Arrive time': arrive, 'Coach from': coach_from, 'Business from': business_from, 'Rooms from': rooms_from}
        results.append(data)
        if train != "Mixed Service" and train != "Multiple Trains":
            opt_data = {'Date': start_date, ' Train': " " + train, ' Rooms from': " " + rooms_from} #create optimized data list
            opt_results.append(opt_data)

    def get_results_for_a_date(the_date): #Gets results for all of the following days
        driver.find_element(By.CSS_SELECTOR, '.refine-search-btn.ng-star-inserted > button').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#mat-input-2').send_keys(Keys.BACKSPACE * 10)
        driver.find_element(By.CSS_SELECTOR, '#mat-input-2').send_keys(the_date)
        driver.find_element(By.CSS_SELECTOR, '.pl-lg-3').click()
        time.sleep(2)

        elements = driver.find_elements(By.CSS_SELECTOR, '.search-results-leg')
        for element in elements:
            try:
                train = element.find_element(By.CSS_SELECTOR, '.pt-1.ng-star-inserted span').text + ' ' + \
                        element.find_elements(By.CSS_SELECTOR, '.handpointer')[1].text
            except:
                train = element.find_element(By.CSS_SELECTOR, '.pt-1.ng-star-inserted span').text
            """depart = element.find_element(By.CSS_SELECTOR, '.departure-inner .font-light').text
            depart += element.find_element(By.CSS_SELECTOR, '.departure-inner .time-period').text
            travel_elements = element.find_elements(By.CSS_SELECTOR, '.travel-time .text-center')
            travel_time = '\n'.join([e.text for e in travel_elements])
            arrive = element.find_element(By.CSS_SELECTOR, '.arrival-inner .font-light').text
            arrive += element.find_element(By.CSS_SELECTOR, '.arrival-inner .time-period').text
            arrive += '\n' + element.find_element(By.CSS_SELECTOR, '.travel-next-day span').text
            try:
                coach_from = element.find_element(By.CSS_SELECTOR, '.text-center:nth-child(1) .amount').text
            except:
                coach_from = 'None'
            try:
                business_from = element.find_element(By.CSS_SELECTOR, '.text-center:nth-child(2) .amount').text
            except:
                business_from = 'None'"""
            try:
                rooms_from = element.find_element(By.CSS_SELECTOR, '.text-center:nth-child(3) .amount').text
            except:
                rooms_from = 'None'
            data = {'Date': new_date, 'Train': train, 'Depart time': depart, 'Travel time': travel_time, 'Arrive time': arrive,
                    'Coach from': coach_from, 'Business from': business_from, 'Rooms from': rooms_from}
            results.append(data)
            if train != "Mixed Service" and train != "Multiple Trains":
                opt_data = {'Date': new_date, ' Train': " " + train, ' Rooms from': " " + rooms_from}  # create optimized data list
                opt_results.append(opt_data)

    new_date = ""
    new_day = int(start_day)
    new_month = int(start_month)
    new_year = int(start_year)
    while new_date != end_date:
        new_day = new_day + 1
        if new_day > 28 and new_year % 4 != 0 and new_month == 2:  # checks feb
            new_day = 1
            new_month = 3
        if new_day > 29 and new_year % 4 == 0 and new_month == 2:  # checks leap feb
            new_day = 1
            new_month = 3
        if new_day > 30 and new_month in months_30:  # checks months with 30 days
            new_day = 1
            new_month += 1
        if new_day > 31 and new_month in months_31:  # checks months with 31 days
            new_day = 1
            new_month += 1
        if new_month > 12:  # checks if a new year is occurring
            new_day = 1
            new_month = 1
            new_year += 1

        new_date = '/'.join([str(int(new_month)), str(int(new_day)), str(int(new_year))])
        # run code that checks date here
        get_results_for_a_date(new_date)

    # Find minimum value over all dates
    min_list = []
    min_dates = []
    for i in range(0, len(opt_results)):
        min_list.append((int(opt_results[i][' Rooms from'].replace("$", ""))))
    min_value = min(min_list)
    for data_set in opt_results:
        if int(data_set[' Rooms from'].replace("$", "")) == min_value:
            min_dates.append(data_set)

    # Save results in a csv flie
    keys = results[0].keys()
    keys2 = opt_results[0]
    prompt = ['Min values: ']
    with open('results.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

    with open('optimization.csv', 'w') as best_file:
        dict_writer = csv.DictWriter(best_file, keys2)
        dict_writer.writeheader()
        dict_writer.writerows(opt_results)
        writer = csv.writer(best_file)
        writer.writerow(prompt)
        dict_wrter.writerows(min_dates)

