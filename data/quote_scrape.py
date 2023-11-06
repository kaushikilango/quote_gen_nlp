from bs4 import BeautifulSoup
import requests,string,csv
from tqdm import tqdm
import random
GLOBAL_RANDOM_IDS = []
data = {}
csv_file = 'data.csv'
def clean_quote(quote,category = None):
    for quote in quote_element:
        key = random_key()
        q = quote.find('div',class_ = 'quoteText')
        q = q.get_text(strip=True).replace("“","").replace("”","").split("―")
        quote = q[0]
        author = q[1].split(',')[0]
        try:
            source = q[1].split(',')[1]
        except:
            source = ""
        x = list(data.keys())
        data[key] = {'quote':quote,'author':author,'source':source,'category':category}

def write_to_csv(data):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['Key', 'Author', 'Quote','Source','Category'])

        # Write the data rows
        for key, values in data.items():
            try:
                writer.writerow([key, values['author'], values['quote'],values['source'],values['category']])
            except:
                continue


def random_key():
    c = string.ascii_letters + string.digits
    key =  ''.join(random.choice(c) for i in range(20))
    if key not in GLOBAL_RANDOM_IDS:
        GLOBAL_RANDOM_IDS.append(key)
        return key
    else:
        random_key()

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
# Find all the <a> elements within the <ul> element
for category in categories:
    print("Scraping category: ",category)
    for i in range(100):
        durl = url + '/tag/' + category + '?page=' + str(i+1)
        response = requests.get(durl)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        quote_element = html_soup.find_all('div',class_ = 'quote mediumText')
        try:
            clean_quote(quote_element,category)
        except:
            continue

write_to_csv(data)