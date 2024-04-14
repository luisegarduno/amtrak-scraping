# Amtrak - Scraping

## Pre-requisites
  - python3:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip3 install -r requirements.txt

# Ensure 'requests' is up-to-date
pip3 install --upgrade requests
```


## Instructions

1. Run the script:
```bash
python3 amtrak.py -a from=PVD to=MIA start_date=2024-06-20 end_date=2024-06-22 people=2 trains_only=True specify=True
```

### Parameters
* `from`: Starting station
* `to`: Ending station
* `start_date`: First date to search (inclusive)
* `end_date`: Last date to search (inclusive)
* `people`: Amount of travelers
* `trains_only`: Disinclude all trips that include buses
* `specify`: Specify train names, meaning multiple segment trips will display all train segments involved
