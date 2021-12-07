# Fetch metal prices from [lme](https://www.lme.com/)'s website

A simple python selenium script that uses the headless firefox browser.

## Usage

-s flag: disable debug mode (silent mode)

Just run the script with -s flag to get current prices from the webpage
```
:>python3 script.py -s

log_date:07/12/2021 20/31/50,close_date: 07 Dec 2021,LME Aluminium:2588.00,LME Copper:9505.00,LME Zinc:3162.50,LME Nickel:19820.00,LME Lead:2196.00,LME Tin:38734.00
```
Data is formatted json like. Commas seperate key value pairs.

## Dependencies

- Python 3.9
- Selenium
