from bs4 import BeautifulSoup
import requests
from tqdm import tqdm



url = 'https://www.goodreads.com/quotes'

response = requests.get(url)

# Retrieve the webpage and store it as an bs4.BeautifulSoup object

html_soup = BeautifulSoup(response.text, 'html.parser')

# Find the <ul> element with the specified class
ul_elements = html_soup.find_all('ul', class_='listTagsTwoColumn')
categories = []
for ul_element in ul_elements:
    a_elements = ul_element.find_all('a')
    for a_element in a_elements:
        x = a_element.get_text(strip=True)
        x = x.replace("Quotes","",1)
        categories.append((x.lstrip()).rstrip())
categories.remove("Life  Quotes")
categories.remove("Love  Quotes")
categories.remove("Inspirational  Quotes")
categories = [x.lower() for x in categories]
categories = [x.replace(" ","-") for x in categories]
print(categories)
# Find all the <a> elements within the <ul> element

data = {}

for i in tqdm(range(100)):
    durl = url + '/tag/' + 'love' + '?page=' + str(i+1)
    response = requests.get(durl)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    quote_element = html_soup.find_all('div',class_ = 'quote mediumText')
    
def clean_quote(quote):
    data ={}
    for quote in quote_element:
        q = quote.find('div',class_ = 'quoteText')
        q = q.get_text(strip=True).replace("“","").replace("”","").split("―")
        quote = q[0]
        author = q[1].split(',')[0]
        try:
            source = q[1].split(',')[1]
        except:
            source = ""
        x = list(data.keys())
        if len(x) == 0:
            data[1] = {'quote':quote,'author':author,'source':source}
        else:
            data[max(x)+1] = {'quote':quote,'author':author,'source':source}

        return data