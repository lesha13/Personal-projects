# importing files with main code


from yahoo_finance_crawler import Crawler
import time

start = time.time() # counting time

if __name__ == "__main__":
    crawler = Crawler()
    data = crawler.crawl("https://finance.yahoo.com/quote/AMZN?p=AMZN&ncid=yahooproperties_peoplealso_km0o32z3jzm") # start page
    print(crawler.adapter.get_data())

end = time.time() # counting time

print(f"{end-start} seconds")
