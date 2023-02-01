from module import get_google_proxy
import requests

# Google Search
url = 'https://www.google.com/search?q=google&sxsrf=AJOqlzUeim8HGc7lFn0Dxm85XsoZQMDkWQ%3A1673471120579&source=hp&ei=kCS_Y6uGId3k2roPgfC9mA8&iflsig=AK50M_UAAAAAY78yoBGzWReLIUDW3GoqZEvOLsR1D9k_&ved=0ahUKEwirjrrdtcD8AhVdslYBHQF4D_MQ4dUDCAg&uact=5&oq=google&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBAgjECcyBQgAEJECMgoIABCxAxCDARBDMgQIABBDMgQIABBDMgoIABCxAxCDARBDMhAILhCxAxCDARDHARDRAxBDMgQIABBDUABYiwVglQloAHAAeACAAZwBiAHvBpIBAzAuNpgBAKABAQ&sclient=gws-wiz'

# Use the method to get a single proxy (Randomize every time)
proxy = get_google_proxy()

try:
    response = requests.get(
        url, proxies={"http": proxy, "https": proxy}, timeout=30)
    if (response.status_code == 200):
        print("Working perfectly")
except:
    pass
