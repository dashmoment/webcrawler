import requests
from bs4 import BeautifulSoup as BS
import HTMLParser
import win32com.client
from time import sleep
import sys

def parseBS():

    res = requests.get("http://search.ruten.com.tw/search/s000.php?searchfrom=indexbar&k=%A4%E9%A5%BB&t=0")
    soup = BS(res.text.encode("utf-8"))

    bid_table = soup.findAll('label')
    #print bid_table[2].findAll('a',{'href':True})
    print len(bid_table)

    bid_file = open("blog_links.txt",'w')

    for link in bid_table:
        links = str([tag['href'] for tag in link.findAll('a',{'href':True})])
        links = str([tag['href'] for tag in link.findAll('a',{'href':True})])[2:-2]
        bid_file.write(links+"\n")
        print links
    bid_file.close()


def parseHTML(addr):
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = 0
    ie.Navigate(addr)

    while True:
        state = ie.ReadyState
        if state == 4:
            break
    sleep(1)

    #print ie.Document.body.innerHTML
    #soup2 = BS(unicode(ie.Document.body.innerHTML).encode('utf-8'))

    bid_file = open("blog_links.html",'w')
    bid_file.write(unicode(ie.Document.body.innerHTML).encode('utf-8'))
    bid_file.close()
    read_bid = open("blog_links.html",'r')
    soup2 = BS(read_bid)
    
    bid_table2 = soup2.findAll('script',{'type':True})
    print len(bid_table2)
    #print soup2.prettify() #print content of html
    #print bid_table[2].findAll({'href':True})

if __name__ == '__main__':
    sys.argv.append("http://search.ruten.com.tw/search/s000.php?searchfrom=indexbar&k=%A4%E9%A5%BB&t=0")
    #sys.argv.append("https://tw.search.bid.yahoo.com/search/auction/product;_ylt=AiyIvuW9ZTXO5oalcYujiUByFbN8;_ylv=3?p=ค้ฅป&qt=product&cid=24198&clv=1&property=auction&sub_property=auction&srch=product&aoffset=48&poffset=0&pg=2&act=srp")
    if(len(sys.argv) == 1):
        print("Please enter website addr")
    else:
        #parseBS()
        parseHTML(sys.argv[1])
