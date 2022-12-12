
"""
    Developed By : Shubham Jagtap
    linkedIn : https://www.linkedin.com/in/shubham-jagtap-scj4497/
    
    Please install Beautiful Soup and Selenium 4
    
    How to use program:
    1. Run the File
    2. Provide the item name you want to scrape eg. laptop, mobile, etc
    3. Provide pages you want to scrape
    
    The program will generate csv for each webpage
    
    Enjoy Amazon scraping
"""
#----------------------------------------------------------
#please install following packages if not present

#!pip3 install bs4
#!pip3 install Selenium  

from bs4 import BeautifulSoup
from selenium import webdriver
import csv

#----------------------------------------------------------------
def get_url(search_term):
    print('Searching for {} on'.format(search_term))
    template = "https://www.amazon.in/s?k={}&crid=3VP0SAVW3TZS7&sprefix={}%2Caps%2C214&ref=nb_sb_noss_1"
    search_term = search_term.replace(' ','+')
    #print(template.format(search_term,search_term))
    return template.format(search_term,search_term)

#----------------------------------------------------------------------
def start_browser():
    """
    Start the Edge web browser 
    """
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    options.add_argument("start-maximized")
    driver = webdriver.Edge(options=options)
    print('Browser Started...')
    return driver

#-----------------------------------------------------------------------
def extract_record(item):
    """Extract and return data from a single record"""
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.in' + atag.get('href')
    price_parent = item.find('span','a-price')
    try:
        price = price_parent.find('span','a-offscreen').text
    except:
        price = ""
    try:
        rating = item.i.text
    except:
        rating = ""
    try:
        review_count = item.find('span',{'class':'s-underline-text'}).text
    except:
        review_count = ""
    result = (description,price,rating,review_count,url)
    return result

#------------------------------------------------------------------
def get_details(records):
    """
    Extract the details and return tuple of (Details,price,ratings,reviews,url)
    """
    Details = []
    price = []
    ratings = []
    reviews = []   
    url = []
    for i in records:
        Details.append(i[0])
        price.append(i[1])
        ratings.append(i[2])
        reviews.append(i[3])
        url.append(i[4])
    return (Details,price,ratings,reviews,url)

#---------------------------------------------------------------------
def final(soup,page_no):
    """
    Pass the extracted soup and page number to extract
    All the details will be stored in csv format
    """
    print('Getting data from {}'.format(page_no))
    records = []
    results = soup.find_all('div',{'data-component-type':'s-search-result'})
    for item in results:
        record = extract_record(item)
        if record:
            records.append(record) 
    filename='Page-'+str(page_no)+str('.csv')
    with open(filename,'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Price','Rating','ReviewCount','Url'])
        writer.writerows(records)
    print('Done page {}'.format(page_no))
#-----------------------------------------------------------

## Main Code ##

item = str(input("Please Enter searching Item :  "))
pages = int(input("Enter Number of pages you want to extract : "))
driver = start_browser()
for i in range(pages):
    url = get_url(item)
    if i>0:
        url=url+str('&page=')+str(i+1)
    else:
        pass
    driver.get(url)
    print(url)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    final(soup,i)
    if i>15:
        print('Current Page limit reached 15')
        driver.quit()
        print('Browser Closed')
        break
driver.quit()
print('Browser Closed')
