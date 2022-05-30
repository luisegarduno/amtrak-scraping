1. You should have python3 installed
2. Install requirements:
    . python -m pip install --upgrade pip (upgrade pip)
    . pip install -r requirements.txt (install requirements)
3. Run the script:

python amtrak.py -a from=PVD to=MIA start_date=2022-06-20 end_date=2022-06-22 people=2 trains_only=True specify=True

4. Directions:
 - from: Starting station
 - to: Ending station
 - start_date: First date to search (inclusive)
 - end_date: Last date to search (inclusive)
 - people: Amount of travelers
 - trains_only: Disinclude all trips that include buses
 - specify: Specify train names, meaning multiple segment trips will display all train segments involved
