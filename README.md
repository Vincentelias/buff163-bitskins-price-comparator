# Buff.163 and Bitskins price comparator
Program that compares the lowest selling prices of csgo items on buff.163 to those on bitskins. The program calculates the discount on buff.163 compared to bitskins and sorts it accordingly (per item). 

## Requirements
- Python > 3.7 (https://www.python.org/downloads/)
- pip (https://pypi.org/project/pip/)
## installation

1. Clone the repository  
`git clone https://github.com/Vincentelias/buff163-bitskins-price-comparator.git`  
`cd buff163-bitskins-price-comparator`
2. Install the dependencies  
`pip install bs4 selenium pyotp requests`
3. Check your current chrome version and download the corresponding chrome driver (https://chromedriver.chromium.org/). Put the chromedriver.exe file in your PATH or in c:/windows/chromedriver.exe. This browser will be used to scrape from buff.163
4. Enable 2-factor-authentication and API access on your bitskins account and write down your 2FA secret (only shows when first setting up 2FA on your account) as well as your API key
5. Login to your buff.163 account and write down your session id in your cookie (press f12 in chrome -> application -> cookies -> https://buff.163.com -> session)
6. rename config.json.example to config.json and fill in following values:
    - session_id
    - two_factor_secret
    - api_key

## Usage
Inside root folder: `python comparator`  
The script will first get item data from bitsksins and after that will start scraping each page on buff.163 and collecting the items. After it scraped all pages, you will get a summary of the best discounts based on the config parameters.