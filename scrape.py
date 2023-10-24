from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
url = 'https://www.phrases.org.uk/meanings/phrases-and-sayings-list.html'

response = requests.get(url)

# Retrieve the webpage and store it as an bs4.BeautifulSoup object
html_soup = BeautifulSoup(response.text, 'html.parser')
corpus = []

quotes = html_soup.find_all('p', class_ = 'phrase-list')
for i in quotes:
        text = i.get_text()
        corpus.append(text)
print(len(corpus))

url = "https://www.wisesayings.com/quote-topics/"
html_content = requests.get(url).text

soup = BeautifulSoup(html_content, 'html.parser')

# Find all <q> elements within the HTML
li_elements = soup.find_all('li')
exten = []
# Print the text within each <q> element
for li in li_elements:
    a_tag = li.find('a')
    if a_tag:
        href = a_tag.get('href')
        exten.append(href)

exten = exten[12:-18]


def get_quotes(url):
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    quotes = []
    q_elements = soup.find_all('q')
    for q_element in q_elements:
       quotes.append(q_element.text)
    return quotes
for i in tqdm(exten):
    print("Running extension: " + i)
    url = "https://www.wisesayings.com" + i
    corpus = corpus + (get_quotes(url))


with open('data.txt', 'w',encoding="utf-8") as f:
  for element in corpus:
    print(element)
    f.write(str(element) + '\n')