#! python3
# OLX.py - defines functions to scrape OLX.pl in order
# to download requested information from flat offers

import bs4, requests, re, json, pprint

baseURL = 'https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/warszawa/?'
Links = []
flatOfferArray = []

# Location codes and others for URL creation specific for this site
locationCodes = {
    "bemowo": '367',
    "wola": '359',
    "bielany": '369'
}
num2words = {"1": 'one', "2": 'two', "3": 'three', "4": 'four', "5": 'five', "6": 'six'}
marketCode = {'pierwotny': 'primary',
          'wtorny': 'secondary'
          }

## Function to create URL for search of given parameters
def SearchUrl(queryCriteria):
    url = (baseURL
           + 'search%5Bdistrict_id%5D=' + locationCodes[queryCriteria['location']] +'&'
           + 'search%5Bfilter_float_price%3Afrom%5D=' + queryCriteria['priceMin'] + '&'
           + 'search%5Bfilter_float_price%3Ato%5D=' + queryCriteria['priceMax'] + '&'
           + 'search%5Bfilter_float_price_per_m%3Afrom%5D=' + queryCriteria['pricePerM2min'] + '&'
           + 'search%5Bfilter_float_price_per_m%3Ato%5D=' + queryCriteria['pricePerM2max'] + '&'
           + 'search%5Bfilter_float_m%3Afrom%5D=' + queryCriteria['flatSizeMin'] + '&'
           + 'search%5Bfilter_float_m%3Ato%5D=' + queryCriteria['flatSizeMax'] + '&'
           + 'search%5Bfilter_enum_rooms%5D%5B0%5D=' + num2words[queryCriteria['roomsNoSearch']] + '&'
           + 'search%5Bfilter_enum_market%5D%5B0%5D=' + marketCode[queryCriteria['market']])
    return url

# Function to download the page and allow for its scrape
def downloadPage(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    return soup

# TODO: Function to create list of sites from a given search condition

# Function to create a list of offers from a search page
def getOfferLinks(queryCriteria):
    url = SearchUrl(queryCriteria)
    soup = downloadPage(url)
    tempList = list(soup.find_all('tr', class_='wrap'))
    for textLine in tempList:
        Links.append(textLine.h3.a.get('href'))
    return Links

# Function to get required data from a single offer
def getOfferDetailsOLX(url):
    offerSoup = downloadPage(url)
    
    # 1. Find offer title
    offerTitle = offerSoup.h1.getText().strip()

    detailsList = list(offerSoup.find_all('table', class_='item'))
    for textLine in detailsList:
        
        # 2. Find flat size
        if textLine.th.getText() == 'Powierzchnia':
            flatSizeRaw = textLine.td.getText().strip()
            flatSize = ''.join(flatSizeRaw.split()[0:-1])
            pattern = re.compile('(\d+?)(,)(\d*\d$)')
            if pattern.search(flatSize) != None:
                flatSize = pattern.search(flatSize)[1] + '.' + pattern.search(flatSize)[3]
            
        #3. Find number of rooms
        elif textLine.th.getText() == 'Liczba pokoi':
            roomsNo = textLine.td.getText().strip()

        #4. Find offer source
        elif textLine.th.getText() == 'Oferta od':
            offerSource = textLine.td.getText().strip()

    #5. Find price of flat
    priceRaw = offerSoup.find('div', class_='price-label').strong.getText()
    price = ''.join(priceRaw.split()[0:-1])

    return offerTitle, flatSize, roomsNo, price, offerSource

def getOfferDetailsOTODOM(url):
    offerSoup = downloadPage(url)
    
    # 1. Find offer title
    offerTitle = offerSoup.h1.getText().strip()

    detailsList = list(offerSoup.find(class_='section-overview').find_all('li'))
    for textLine in detailsList:
        
        # 2. Find flat size
        if textLine.getText().startswith('Powierzchnia') == True:
            flatSizeRaw = textLine.strong.getText()
            flatSize = ''.join(flatSizeRaw.split()[0:-1])
            pattern = re.compile('(\d+?)(,)(\d*\d$)')
            if pattern.search(flatSize) != None:
                flatSize = pattern.search(flatSize)[1] + '.' + pattern.search(flatSize)[3]
            
        #3. Find number of rooms
        elif textLine.getText().startswith('Liczba pokoi') == True:
            roomsNo = textLine.strong.getText()

    #4. Find offer source
    offerSource = ''
    
    #5. Find price of flat
    priceRaw = offerSoup.find(class_='css-1vr19r7').getText()
    price = ''.join(priceRaw.split()[0:-1])

    return offerTitle, flatSize, roomsNo, price, offerSource