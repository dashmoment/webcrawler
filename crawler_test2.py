import requests
from bs4 import BeautifulSoup as BS
import HTMLParser
import win32com.client
from time import sleep
import sys
import urllib2
import codecs
import lxml.etree as etree
from lxml.html import parse, fromstring
import lxml
from io import StringIO, BytesIO
import csv
#reload(sys)
#sys.setdefaultencoding('utf-8')

url = "http://goo.gl/U45CTo"
#url = "http://bryannotes.blogspot.tw/2014/12/python-crawler_29.html"
def parse_res():

    #encode_url = urllib.quote('https://tw.search.bid.yahoo.com/search/product;_ylt=AvwAtqE5M_4pXJKEVlH49DNyFbN8;_ylv=3?p=ค้ฅป&property=auction&sub_property=auction&srch=product&act=srp&pg=1&poffset=0&aoffset=0')
    #print encode_url
    #html = urlopen(url).read()
    #soup = BS(html)
   
    
    res = requests.get(url,timeout = 3, allow_redirects = True)
    soup_res = BS(res.text.encode("utf-8"))
    result = soup_res.findAll('div', {'class':'att-item item '})
    print soup_res.prettify()

    return result

def parse_html():
    
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible  = 0
    ie.Navigate(url)

    while True:
        state = ie.ReadyState
        if state == 4:
            break
    sleep(1)
    
    text = ie.Document.body.innerHTML
    text = text.encode('utf-8','ignore')
    #print text
    read_bid = open("bid.html",'w')
    read_bid.write(text)
    read_bid.close()
    data = open("bid.html",'r')
    soup_res = BS(data)
    
    print soup_res.prettify()

def parse_inline(filename = "bid.html"):
    data = open("bid.html",'r')
    lines = [line.strip() for line in data]
    print len(lines)
    print lines

def csv_writer():
    a = [["aaaaa",1], [1,2], [2,3], [3,4]]
    b = [4,5,6,7]
    with open('csv_text.csv', 'w') as csvfile:
        writer =csv.writer(csvfile)
        for i in a:
            print i
            writer.writerow(i)

    

csv_writer()
##parser = etree.HTMLParser()
##tree = etree.parse(urllib2.urlopen(url),parser)
##paging = tree.xpath('//a[@class="ellipsis"]')
##print len(paging)
##print  len(paging[1].text)
##print paging[1].text
##print paging[1].text[2]
#result = etree.tostring(tree.getroot(), pretty_print = True, method = "html")#

#parsed = parse(urllib2.urlopen(url))
#doc = parsed.getroot()
#doc.make_links_absolute(url)



#founder = doc.findtext('div')
#lxml.html.open_in_browser(doc)
#print founder

#parse_html()
#parse_inline()
#res_res = parse_res()
#print len(res_res)
#print res_res
