from itertools import cycle
import requests
from Proxy_List_Scrapper import Scrapper


SSL = 'https://www.sslproxies.org/'
GOOGLE = 'https://www.google-proxy.net/'
ANANY = 'https://free-proxy-list.net/anonymous-proxy.html'
UK = 'https://free-proxy-list.net/uk-proxy.html'
US = 'https://www.us-proxy.org/'
NEW = 'https://free-proxy-list.net/'
SPYS_ME = 'http://spys.me/proxy.txt'
PROXYSCRAPE = 'https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all'
PROXYNOVA = 'https://www.proxynova.com/proxy-server-list/'
PROXYLIST_DOWNLOAD_HTTP = 'https://www.proxy-list.download/HTTP'
PROXYLIST_DOWNLOAD_HTTPS = 'https://www.proxy-list.download/HTTPS'
PROXYLIST_DOWNLOAD_SOCKS4 = 'https://www.proxy-list.download/SOCKS4'
PROXYLIST_DOWNLOAD_SOCKS5 = 'https://www.proxy-list.download/SOCKS5'
ALL = 'ALL'


scrapper = Scrapper(category=ALL, print_err_trace=False)
data = scrapper.getProxies()
print("Total Proxies Found:", data.len)

validated = 0
url = 'https://www.google.com/search?q=google&sxsrf=AJOqlzUeim8HGc7lFn0Dxm85XsoZQMDkWQ%3A1673471120579&source=hp&ei=kCS_Y6uGId3k2roPgfC9mA8&iflsig=AK50M_UAAAAAY78yoBGzWReLIUDW3GoqZEvOLsR1D9k_&ved=0ahUKEwirjrrdtcD8AhVdslYBHQF4D_MQ4dUDCAg&uact=5&oq=google&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBAgjECcyBQgAEJECMgoIABCxAxCDARBDMgQIABBDMgQIABBDMgoIABCxAxCDARBDMhAILhCxAxCDARDHARDRAxBDMgQIABBDUABYiwVglQloAHAAeACAAZwBiAHvBpIBAzAuNpgBAKABAQ&sclient=gws-wiz'
for i in data.proxies:
    ip_address = i.ip+":"+i.port
    try:
        response = requests.get(
            url, proxies={"http": ip_address, "https": ip_address}, timeout=30)
        if (response.status_code == 200):
            print(ip_address)
            validated += 1
    except:
        pass
print("Validated Proxies:", validated)
