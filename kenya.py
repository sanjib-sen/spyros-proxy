from time import sleep
from bs4 import BeautifulSoup

DB_CREATED = False


def start__scraping():
    print("For Sale\n")
    SALES = 'https://www.buyrentkenya.com/property-for-sale'
    page_no = 1
    while (True):
        soup = use_requests(SALES)
        properties = ["https://www.buyrentkenya.com"+elem.find("a", recursive=False).get("href") for elem in soup.find_all(
            "div", class_="w-full flex-1")]
        for p in properties:
            scrape_property(p, type="FOR SALE")
        page_no += 1
        if f"https://www.buyrentkenya.com/property-for-sale?page={page_no}" in [
                a["href"] for a in soup.find_all("a", href=True)]:
            SALES = f"https://www.buyrentkenya.com/property-for-sale?page={page_no}"
            # sleep(20)
            print("\nPage: ", page_no)
            continue
        else:
            break

    # sleep(180)
    RENTS = 'https://www.buyrentkenya.com/property-for-rent'
    print("For Rent\n")
    page_no = 1
    while (True):
        soup = use_requests(RENTS)
        properties = ["https://www.buyrentkenya.com"+elem.find("a", recursive=False).get("href") for elem in soup.find_all(
            "div", class_="w-full flex-1")]
        for p in properties:
            scrape_property(p, type="FOR RENT")

        page_no += 1
        if f"https://www.buyrentkenya.com/property-for-rent?page={page_no}" in [
                a["href"] for a in soup.find_all("a", href=True)]:
            RENTS = f"https://www.buyrentkenya.com/property-for-rent?page={page_no}"
            # sleep(20)
            print("\nPage: ", page_no)
            continue
        else:
            break


def getPropertyFromDesc(description: str, property: str):
    description = description.lower()
    if property in description:
        index_property = description.find(property)
        prev_full_stop_index = 0
        next_full_stop_index = 0
        idx = index_property-1
        while (idx > 0):
            if description[idx] == ".":
                prev_full_stop_index = idx
                break
            idx -= 1
        if prev_full_stop_index == 0:
            return "Not found"
        idx = index_property+len(property)
        while (idx < len(description)):
            if description[idx] == ".":
                next_full_stop_index = idx
                break
            idx += 1
        if next_full_stop_index == 0:
            return "Not found"

        full_sentence = description[prev_full_stop_index +
                                    1:next_full_stop_index]

        words = full_sentence.split(" ")

        idx = 0
        for word in words:
            if property in word:
                property_word_idx = idx
                break
            idx += 1

        if len(words) == property_word_idx+1:
            if words[property_word_idx-1].isdigit():
                return words[property_word_idx-1]
            else:
                return "Not found"
        elif words[property_word_idx+1].isdigit() and not words[property_word_idx-1].isdigit():
            return words[property_word_idx+1]
        elif words[property_word_idx-1].isdigit() and not words[property_word_idx+1].isdigit():
            return words[property_word_idx+1]
        elif words[property_word_idx-1].isdigit() and words[property_word_idx+1].isdigit():
            return words[property_word_idx+1]
        else:
            return "Not found"

            # propertyStringBothSide = description[description.find(
            #     property)-3:description.find(property)] if property in description else None
            # if propertyStringBothSide != None:
            #     return int(list(filter(str.isdigit, propertyStringBothSide))[0])
            # else:
            #     return "Not found"
    else:
        return "Not found"


class Listing:
    global_id = 0

    def __init__(self) -> None:
        self.id = Listing.global_id
        Listing.global_id += 1


def use_requests(URL):
    import requests
    return BeautifulSoup(requests.get(URL).content, "html.parser")


def use_requests_html(URL):
    from requests_html import HTMLSession
    session = HTMLSession()
    response = session.get(URL)
    response.html.render()
    return BeautifulSoup(response.html.raw_html, "html.parser")


def scrape_property(URL, type="Undefined"):
    # Either use requests or requests_html
    # soup = use_requests_html(URL)
    soup = use_requests(URL)

    def get_by_tagNclass(tagName, class_):
        elements = soup.find_all(
            tagName, class_=class_)
        return elements[0].text.strip() if len(elements) > 0 else "Not found"

    listing = Listing()

    # Getting the Attributes
    title = get_by_tagNclass(
        "h1", class_="text-lg md:text-2xl inline font-bold")
    if title == "Not found":
        sleep(2)
        return
    address = get_by_tagNclass("p", class_="text-sm mb-4 text-grey-darker")
    units = get_by_tagNclass("div", class_="flex items-center text-sm")
    description = get_by_tagNclass(
        "div", class_="mb-2 leading-normal text-justify whitespace-pre-line")
    amenities = [elem.text.strip() for elem in soup.find_all(
        "div", class_="flex-auto lg:mr-12 text-sm overflow-hidden break-words")]
    date_listed = get_by_tagNclass(
        "div", class_="flex justify-between py-2").split("\n")[1]
    whatsapp = soup.find_all(
        "a", class_="rounded-md bg-white border border-[#81C14B] flex-grow w-full p-3 text-[#81C14B] flex items-center justify-center no-underline text-sm flex-1")[0].get("href").split("wa.me/")[1].split("?")[0] if len(soup.find_all(
            "a", class_="rounded-md bg-white border border-[#81C14B] flex-grow w-full p-3 text-[#81C14B] flex items-center justify-center no-underline text-sm flex-1")) else "Not found"
    agency = get_by_tagNclass(
        "h4", class_="font-light text-accent-500 hover:text-accent-darker mt-4")
    price = get_by_tagNclass("span", class_="text-xl font-bold block mr-3")
    size = get_by_tagNclass("span", class_="flex items-center mr-5 max-w-24")
    bedrooms = get_by_tagNclass(
        "span", class_="flex items-center mr-5 max-w-24 truncate")
    bathrooms = get_by_tagNclass(
        "span", class_="flex items-center max-w-24 truncate")
    parking = "Yes" if "Parking" in amenities else "No"

    # TODO: Does not work for now
    # market_range = get_by_tagNclass(
    #     "span", class_="mt-2 justify-between flex flex-row w-full text-sm text-gray-500")

    floors = getPropertyFromDesc(description, "floor")
    floors = floors if floors.isdigit() else "Not found"
    units = getPropertyFromDesc(
        description, "unit") if units == "Not found" else units
    units = units if units.isdigit() else "Not found"

    address_list = [elem.text.strip() for elem in soup.find_all(
        "a", "text-accent-500 no-underline breadcrumbs__list-item__link")]

    address = address_list[2] + "," + \
        address_list[3] if address == "Not found" else address
    listing.title = title
    listing.address = address
    listing.units = units
    listing.floors = floors
    # listing.description = description
    listing.amenities = ",".join(amenities)
    listing.date_listed = date_listed
    listing.whatsapp = whatsapp
    listing.agency = agency
    listing.price = price
    listing.size = size
    listing.bedrooms = bedrooms
    listing.bathrooms = bathrooms
    listing.parking = parking
    listing.type = type
    listing.url = URL

    use_db(listing)
    # sleep(3)


def use_db(listing_object):
    global DB_CREATED
    import sqlite3
    conn = sqlite3.connect('LISTINGS.db')
    listing_keys = list(listing_object.__dict__.keys())
    listing_values = list(listing_object.__dict__.values())
    if DB_CREATED == False:
        attributes_string = ""
        for attribute in listing_keys:
            if attribute == "id":
                continue
            attributes_string += attribute+"  TEXT,"
        conn.execute(
            f"CREATE TABLE LISTINGS (id INT PRIMARY KEY    NOT NULL, {attributes_string[:-1]});")
        print("Table created successfully")
        DB_CREATED = True
    listing_keys_as_str = ",".join(listing_keys)

    listing_values_as_str = "'" + "','".join(
        [listing_values[i] for i in range(1, len(listing_values))])+"'"

    conn.execute(
        f"""INSERT INTO LISTINGS ({listing_keys_as_str}) VALUES ({listing_values[0]},{listing_values_as_str})""")

    conn.commit()
    print("Data Inserted for", listing_object.url)
    conn.close()


start__scraping()
