# Buff.163 and Bitskins price comparator
Program that compares the lowest selling prices of csgo items on buff.163 to those on bitskins and cs.deals.
## Requirements
- Python > 3.7 (https://www.python.org/downloads/)
- pip (https://pypi.org/project/pip/)
## installation

1. Clone the repository  
`git clone https://github.com/Vincentelias/buff163-bitskins-price-comparator.git`  
`cd buff163-bitskins-price-comparator`
2. Install the dependencies
`pip install -r requirements.txt`
3. Check your current chrome version and download the corresponding chrome driver (https://chromedriver.chromium.org/). Put the chromedriver.exe file in your PATH or in c:/windows/chromedriver.exe. This browser will be used to scrape from buff.163
4. Enable 2-factor-authentication and API access on your bitskins account and write down your 2FA secret (only shows when first setting up 2FA on your account) as well as your API key
5. Login to your buff.163 account and write down your session id in your cookie (press f12 in chrome -> application -> cookies -> https://buff.163.com -> session)
6. rename config.json.example to config.json and fill in following values:
    - session_id
    - two_factor_secret
    - api_key

## Usage
The program has two modes which can set in the config:
- buy_mode="buff" -> buy on buff, sell on cs.deals (will use bitskins API to get prices)
- buy_mode="csdeals" -> buy on cs.deals, sell on buff.163 

When executing for the first time, make sure to set "reload_all_items" in the config to true.
This will reload the items (save to files locally) from cs.deals, bitskins, and buff, based on the parameters in the config.
When running the program again, you can set "reload_all_items" to false. The program will use the locally saved
items to create new comparisons.


Use `python comparator` in the root folder to start the program

 
It will get a summary of the best discounts based on the config parameters.