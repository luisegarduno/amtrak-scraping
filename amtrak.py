# Importing libraries
from turtle import title
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
    key = items[0].strip()
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
    website_url = 'https://www.amtrak.com/planning-booking/policies/cookie-policy.html'
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
    trains_only = args.get('trains_only')
    specify = args.get('specify')

    # Fill inputs
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '.show-navbar .site-secondary-nav__li_link_text').click()
    driver.find_element(By.CSS_SELECTOR, '#mat-input-0').send_keys(from_)
    driver.find_element(By.CSS_SELECTOR, '#mat-input-1').send_keys(to_)
    driver.find_element(By.CSS_SELECTOR, '#mat-input-2').send_keys(start_date)
    try:
        driver.find_element(By.CSS_SELECTOR, '.t-title').click()
    except:
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.t-title').click()
    while p > 1:
        driver.find_element(By.CSS_SELECTOR, '.increment').click()
        p -= 1
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '.col-12 .ml-2').click()
    driver.find_element(By.CSS_SELECTOR, '.pl-lg-3').click()
    time.sleep(2)
    # solve person count errors
    try:
        if driver.find_element(By.CSS_SELECTOR, '.traveler-number').text != args.get('people'):
            p = int(args.get('people'))
            driver.find_element(By.CSS_SELECTOR, '.refine-search-btn.ng-star-inserted > button').click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '.t-title').click()
            while p > 1:
                driver.find_element(By.CSS_SELECTOR, '.increment').click()
                p -= 1
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, '.col-12 .ml-2').click()
            driver.find_element(By.CSS_SELECTOR, '.pl-lg-3').click()
            time.sleep(2)
    except:
        pass

    results = []
    opt_results = []

    def enter_a_date(the_date):
        actions.send_keys(Keys.ARROW_UP * 30).perform()
        time.sleep(1)
        try:
            driver.find_element(By.CSS_SELECTOR, '.refine-search-btn.ng-star-inserted > button').click()
            time.sleep(1)
        except:
            pass
        driver.find_element(By.CSS_SELECTOR, '#mat-input-2').send_keys(Keys.BACKSPACE * 10)
        driver.find_element(By.CSS_SELECTOR, '#mat-input-2').send_keys(the_date)
        driver.find_element(By.CSS_SELECTOR, '.pl-lg-3').click()
        time.sleep(1)

    def get_results_for_a_date(): # Gets results for all of the following days
        try:
            alert_ = driver.find_element(By.CSS_SELECTOR, '.alert.alert-danger').text
            if alert_ == "We don't have train service matching your request.":
                alert = True
            else:
                alert = False
        except:
            alert = False
        if alert == True:
            data = {'Title': ' Sold out', 'Date': new_date, 'Depart time': ' Sold out', 'Travel time': ' Sold out',
                    'Arrive time': ' Sold out',
                    'Coach from': ' Sold out', 'Business from': ' Sold out', 'Rooms from': ' Sold out',
                    'Train names': ' Sold out'}
            results.append(data)
            opt_data = {'Date': new_date, ' Trains': ' Sold out', ' Rooms/First from': ' Sold out'}
            opt_results.append(opt_data)
        else:
            trains = driver.find_elements(By.CSS_SELECTOR, '.search-results-leg')
            for train in trains:
                try:
                    title = train.find_element(By.CSS_SELECTOR, '.pt-1.ng-star-inserted span').text + ' ' + \
                            train.find_elements(By.CSS_SELECTOR, '.handpointer')[1].text
                except:
                    title = train.find_element(By.CSS_SELECTOR, '.pt-1.ng-star-inserted span').text
                depart = train.find_element(By.CSS_SELECTOR, '.departure-inner .font-light').text
                depart += train.find_element(By.CSS_SELECTOR, '.departure-inner .time-period').text
                travel_elements = train.find_elements(By.CSS_SELECTOR, '.travel-time .text-center')
                travel_time = ' '.join([e.text for e in travel_elements])
                arrive = train.find_element(By.CSS_SELECTOR, '.arrival-inner .font-light').text
                arrive += train.find_element(By.CSS_SELECTOR, '.arrival-inner .time-period').text
                arrive += train.find_element(By.CSS_SELECTOR, '.travel-next-day span').text
                try:
                    coach_from = train.find_element(By.CSS_SELECTOR, '.text-center:nth-child(1) .amount').text
                except:
                    coach_from = 'None'
                try:
                    business_from = train.find_element(By.CSS_SELECTOR, '.text-center:nth-child(2) .amount').text
                except:
                    business_from = 'None'
                try:
                    if train.find_element(By.CSS_SELECTOR, '.text-center:nth-child(3) .service-type').text == 'Rooms from':
                        rooms_from = train.find_element(By.CSS_SELECTOR, '.text-center:nth-child(3) .amount').text
                    elif train.find_element(By.CSS_SELECTOR, '.text-center:nth-child(3) .service-type').text == 'First from':
                        rooms_from = train.find_element(By.CSS_SELECTOR, '.text-center:nth-child(4) .amount').text
                except:
                    try:
                        rooms_from = train.find_element(By.CSS_SELECTOR, '.text-center:nth-child(4) .amount').text
                    except:
                        rooms_from = 'None'
                def grab_names():
                    if specify == 'True':
                        Trip_Details = train.find_element(By.CSS_SELECTOR, '.dropdown-toggle span')
                        while True:
                            try:
                                Trip_Details.click()
                                train.find_element(By.XPATH, '//*[contains(text(), "Services")]').click()
                                break
                            except:
                                actions.move_to_element(train.find_element(By.CSS_SELECTOR, '.departure-inner .font-light'))
                                actions.click()
                                actions.send_keys(Keys.ARROW_DOWN * 20)
                                actions.perform()
                                continue
                        services = train.find_elements(By.CSS_SELECTOR, '.dropdown-container .travel-type-service')
                        if len(services) == 0:
                            train_names = title
                        else:
                            train_names = []
                            for segment in services:
                                a = segment.text.replace('\n', ' ')
                                a = a.replace('Operated by Amtrak Chartered Motorcoach ', '')
                                train_names.append(a)
                            train_names = ', '.join(train_names)
                        actions.send_keys(Keys.ESCAPE).perform()
                    else:
                        train_names = title
                    data = {'Title': title, 'Date': new_date, 'Depart time': depart, 'Travel time': travel_time, 'Arrive time': arrive,
                            'Coach from': coach_from, 'Business from': business_from, 'Rooms from': rooms_from,
                            'Train names': train_names}
                    results.append(data)

                    if rooms_from != 'None':
                        opt_data = {'Date': new_date, ' Trains': " " + train_names, ' Rooms/First from': " " + rooms_from}
                        opt_results.append(opt_data)
                    if rooms_from == 'None':
                        opt_data = {'Date': new_date, ' Trains': " " + train_names, ' Rooms/First from': " " + business_from}
                        opt_results.append(opt_data)

                if trains_only == 'False':
                    grab_names()
                elif trains_only == 'True' and title != 'Mixed Service':
                    grab_names()
                else:
                    pass

    new_date = start_date
    get_results_for_a_date()
    new_date = ""
    new_day = int(start_day)
    new_month = int(start_month)
    new_year = int(start_year)
    while new_date != end_date and start_date != end_date:
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
        enter_a_date(new_date)
        get_results_for_a_date()


    # Find minimum value over all dates
    min_list = []
    min_dates = []
    for i in range(0, len(opt_results)):
        if opt_results[i][' Rooms/First from'] != ' None' and opt_results[i][' Rooms/First from'] != ' Sold out':
            min_list.append(int(opt_results[i][' Rooms/First from'].replace("$", "")))
    if min_list:
        min_value = min(min_list)
        for data_set in opt_results:
            if data_set[' Rooms/First from'] != ' None' and data_set[' Rooms/First from'] != ' Sold out':
                if int(data_set[' Rooms/First from'].replace("$", "")) == min_value:
                    min_dates.append(data_set)
    else:
        min_dates.append({' Rooms/First from': ' Sold out'})

    # Save results in a csv flie
    keys = results[0].keys()
    keys2 = opt_results[0].keys()
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
        dict_writer.writerows(min_dates)