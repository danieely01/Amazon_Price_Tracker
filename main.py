import requests
from bs4 import BeautifulSoup
import smtplib
import lxml
import os
MY_EMAIL = os.environ['MAIL']
PASSWORD = os.environ['PASSWORD']
URL = "https://www.amazon.com/CeraVe-Hydrating-Facial-Cleanser-Fragrance/dp/B01MSSDEPK/ref=sr_1_2?keywords=carevera%2Bface%2Bcleanser&qid=1672687000&sprefix=careve%2Caps%2C216&sr=8-2&th=1"

amazon_params = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept-Language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(url=URL, headers=amazon_params)
data = response.text
soup = BeautifulSoup(data, "lxml")
title = soup.select_one(selector="h1 span", id="productTitle").getText()
price_find = soup.find_all(name="span", class_="a-offscreen")

price = price_find[0].getText()
price_list = price.split("$")
actual_price = float(price_list[1])
want_price = 20
if actual_price < want_price:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=f"Subject: Amazon Price Alert!\n\n{title} is now {actual_price}")