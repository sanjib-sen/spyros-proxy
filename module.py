import requests
from Proxy_List_Scrapper import Scrapper


def get_google_proxy():
    scrapper = Scrapper(category='ALL', print_err_trace=False)
    data = scrapper.getProxies()
    print("Total Proxies Found:", data.len)
    url = 'https://www.google.com/search?q=google&sxsrf=AJOqlzUeim8HGc7lFn0Dxm85XsoZQMDkWQ%3A1673471120579&source=hp&ei=kCS_Y6uGId3k2roPgfC9mA8&iflsig=AK50M_UAAAAAY78yoBGzWReLIUDW3GoqZEvOLsR1D9k_&ved=0ahUKEwirjrrdtcD8AhVdslYBHQF4D_MQ4dUDCAg&uact=5&oq=google&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBAgjECcyBQgAEJECMgoIABCxAxCDARBDMgQIABBDMgQIABBDMgoIABCxAxCDARBDMhAILhCxAxCDARDHARDRAxBDMgQIABBDUABYiwVglQloAHAAeACAAZwBiAHvBpIBAzAuNpgBAKABAQ&sclient=gws-wiz'
    for i in data.proxies:
        ip_address = i.ip+":"+i.port
        try:
            response = requests.get(
                url, proxies={"http": ip_address, "https": ip_address}, timeout=30)
            if (response.status_code == 200):
                return ip_address
        except:
            pass


# use it as proxy = get_google_proxy()
