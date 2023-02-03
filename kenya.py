import requests
from bs4 import BeautifulSoup

URL = "https://www.buyrentkenya.com/listings/3-bedroom-apartment-for-rent-kilimani-3577567"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
title = soup.find_all(
    "h1", class_="text-lg md:text-2xl inline font-bold")[0].text.strip()
# address = soup.find_all(
#     "p", class_="text-sm mb-4 text-grey-darker")[0].text.strip()
# units = soup.find_all(
#     "div", class_="flex items-center text-sm")[0].text.strip()
description = soup.find_all(
    "div", class_="mb-2 leading-normal text-justify whitespace-pre-line")[0].text.strip()
amenities = [elem.text.strip() for elem in soup.find_all(
    "div", class_="flex-auto lg:mr-12 text-sm overflow-hidden break-words")]
date_listed = soup.find_all(
    "div", class_="flex justify-between py-2")[0].text.strip().split("\n")[1]
whatsapp = soup.find_all(
    "a", class_="rounded-md bg-white border border-[#81C14B] flex-grow w-full p-3 text-[#81C14B] flex items-center justify-center no-underline text-sm flex-1")[0].get("href").split("wa.me/")[1].split("?")[0]
agency = soup.find_all(
    "h4", class_="font-light text-accent-500 hover:text-accent-darker mt-4")[0].text.strip()
price = soup.find_all(
    "span", class_="text-xl font-bold block mr-3")[0].text.strip()

size_and_beds = soup.find_all(
    "span", class_="flex items-center mr-5 max-w-24")

print(len(size_and_beds))
print()

bedrooms = size_and_beds[1].text.strip() if len(
    size_and_beds) > 1 else size_and_beds[0].text.strip()
size = size_and_beds[0].text.strip() if len(size_and_beds) > 1 else None

bathrooms = soup.find_all(
    "span", class_="flex items-center max-w-24 truncate")[0].text.strip()
parking = "Parking" in amenities
print(bedrooms, bathrooms, size)
