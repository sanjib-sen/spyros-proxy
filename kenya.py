from bs4 import BeautifulSoup

DB_CREATED = False


def start__scraping():
    SALES = 'https://www.buyrentkenya.com/property-for-sale'
    page_no = 1
    while (True):
        response_data = use_requests(SALES)
        soup = BeautifulSoup(response_data, "html.parser")
        properties = [elem.get("href") for elem in soup.find_all(
            "h3", class_="hidden show-title text-black text-base leading-normal mb-1 capitalize font-normal")]
        for p in properties:
            scrape_property(p, type="FOR SALE")
        page_no += 1
        if len(soup.find_all(
                "h3", class_="hidden show-title text-black text-base leading-normal mb-1 capitalize font-normal")) > 0:
            SALES += f"?page={page_no}"
            continue
        else:
            break

    RENTS = 'https://www.buyrentkenya.com/property-for-rent'
    page_no = 1
    while (True):
        response_data = use_requests(RENTS)
        soup = BeautifulSoup(response_data, "html.parser")
        properties = [elem.get("href") for elem in soup.find_all(
            "h3", class_="hidden show-title text-black text-base leading-normal mb-1 capitalize font-normal")]
        for p in properties:
            scrape_property(p, type="FOR RENT")

        page_no += 1
        if len(soup.find_all(
                "h3", class_="hidden show-title text-black text-base leading-normal mb-1 capitalize font-normal")) > 0:
            RENTS += f"?page={page_no}"
            continue
        else:
            break


class Listing:
    global_id = 0

    def __init__(self) -> None:
        self.id = Listing.global_id
        Listing.global_id += 1


def use_requests(URL):
    import requests
    page = requests.get(URL)
    return page.content


def use_requests_html(URL):
    from requests_html import HTMLSession
    session = HTMLSession()
    response = session.get(URL)
    response.html.render()
    return response.html.raw_html


def scrape_property(URL, type="Undefined"):
    # Either use requests or requests_html
    # response_data = use_requests_html(URL)
    response_data = use_requests(URL)
    soup = BeautifulSoup(response_data, "html.parser")

    def get_by_tagNclass(tagName, class_):
        elements = soup.find_all(
            tagName, class_=class_)
        return elements[0].text.strip() if len(elements) > 0 else "Not found"

    listing = Listing()

    # Getting the Attributes
    title = get_by_tagNclass(
        "h1", class_="text-lg md:text-2xl inline font-bold")
    address = get_by_tagNclass("p", class_="text-sm mb-4 text-grey-darker")
    units = get_by_tagNclass("div", class_="flex items-center text-sm")
    description = get_by_tagNclass(
        "div", class_="mb-2 leading-normal text-justify whitespace-pre-line")
    amenities = [elem.text.strip() for elem in get_by_tagNclass(
        "div", class_="flex-auto lg:mr-12 text-sm overflow-hidden break-words")]
    date_listed = get_by_tagNclass(
        "div", class_="flex justify-between py-2").split("\n")[1]
    whatsapp = soup.find_all(
        "a", class_="rounded-md bg-white border border-[#81C14B] flex-grow w-full p-3 text-[#81C14B] flex items-center justify-center no-underline text-sm flex-1")[0].get("href").split("wa.me/")[1].split("?")[0]
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

    # TODO: Floors

    listing.title = title
    listing.address = address
    listing.units = units
    listing.description = description
    listing.amenities = amenities
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


def use_db(listing_object):
    import sqlite3
    conn = sqlite3.connect('LISTINGS.db')
    print("Opened database successfully")
    if DB_CREATED == False:
        attributes_string = ""
        listing_keys = listing_object.__dict__.keys()
        listing_values = listing_object.__dict__.values()
        for attribute in listing_keys:
            if attribute == "id":
                continue
            attributes_string += attribute+"  TEXT,"
        conn.execute(f'''CREATE TABLE LISTINGS
                (id INT PRIMARY KEY    NOT NULL,
                {attributes_string}
                );''')
        print("Table created successfully")
        DB_CREATED = True
    listing_keys_as_str = ",".join(listing_keys)
    listing_values_as_str = ",".join(listing_values)

    conn.execute(f"INSERT INTO LISTINGS ({listing_keys_as_str}) \
      VALUES ({listing_values_as_str})")

    conn.close()
