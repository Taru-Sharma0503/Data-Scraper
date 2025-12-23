import requests
from bs4 import BeautifulSoup
import csv

url='https://books.toscrape.com/catalogue/page-1.html'
content=requests.get(url)
soup=BeautifulSoup(content.text,'html.parser')
with open('webScraper.csv','w',newline='',encoding='utf-8') as f:
    write=csv.writer(f)
    write.writerow(['Title','Price','Availability','Product Description','Rating'])
allBooks=soup.find_all('article',class_="product_pod")
for book in allBooks:
    title=book.h3.a['title']
    price=book.find('div',class_='product_price').find_next('p',class_='price_color').text
    availability=book.find('div',class_='product_price').find_next('p',class_='instock availability').text
    detail_link=book.h3.a['href']
    detail_url='https://books.toscrape.com/catalogue/'+detail_link
    detail_content=requests.get(detail_url)
    detail_soup=BeautifulSoup(detail_content.text,'html.parser')
    product_desc=detail_soup.find('div',id='product_description')
    product_description=product_desc.find_next('p').text if product_desc else 'No description available'
    rating=detail_soup.find('p',class_='star-rating')
    rating_value=rating['class'][1] if rating else 'Not rated'
    print(f'Title: {title}')
    print(f'Price: {price}')
    print(f'Availability: {availability.strip()}')
    print(f'Product Description: {product_description}')
    print(f'Rating: {rating_value}')
    print()
    print('Next Book:')
    print()
    with open('webScraper.csv','a',newline='',encoding='utf-8') as f:
        write=csv.writer(f)
        write.writerow([title,price,availability.strip(),product_description,rating['class'][1]])
print('End of products')