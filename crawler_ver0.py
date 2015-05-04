import time
import urllib2
import lxml.etree as etree
from lxml.html import parse, fromstring
import csv
import numpy as np


timer = time.strftime("%d%b%Y",time.gmtime())

def parser_etree(url):
    parser = etree.HTMLParser()
    tree = etree.parse(urllib2.urlopen(url),parser)
    print 'url parsed...'
    return tree

def filter_etree(tree, site ='yahoo',tag = 'all'):
    if site == 'yahoo' and tag == 't':
        print "Derive yahoo page..."
        data = tree.xpath('//a[@class="ellipsis"]')
        print "Get total " + str(len(data)) + " product"
        return data

    if site == 'yahoo' and tag == 'all':
        print "Derive yahoo page for all info..."
        title = tree.xpath('//a[@class="ellipsis"]')
        price = tree.xpath('//em[@class="yui3-u"]')
        store = tree.xpath('//div[@class="srp-pdstore"]/a[@href]')

        #data = store
        #print [unicode(p.text).encode('utf-8') for p in store]
        data = [price, store[4:], title]

        print "Get total " + str(len(data[0])) + " product"
        return data

def collector_txt(data, site ='yahoo'):
    if site == 'yahoo' :
        idx = 0
        container_p = data[0]
        container_s = data[1]
        container_t = data[2]
        filename = "y_bid.csv"
        bid_file = open(filename,'w')
        writer =csv.writer(bid_file)
        for item in container_p:
            line_p = unicode(item.text).encode('utf-8')
            line_s = unicode(container_s[idx].text).encode('utf-8')
            line_t = unicode(container_t[idx].text).encode('utf-8')
            score = str((len(container_p) - idx)*5)
            data = [score, line_p, line_s, line_t]

            writer.writerow(data)
                  
            #bid_file.write(','.join(data))
            #bid_file.write('\n')
            idx = idx + 1
        #bid_file.close()
        print "writefile finish " + timer

def readfile(filename):
        content = []
        bid_file = open(filename,'r')
        reader = csv.reader(bid_file)
        for row in reader:
            content.append(row)
        return content

def sort(content , bytag = 'store'):
    if bytag == 'store':
        pool_store = []
        for idx in range(len(content)) 
            temp = content[idx][2]
            
        
##        dt = np.dtype([('title',np.str_,150),('score', np.float64, 1)])
##        title = np.str(data[0])
##        title2 = np.str(data[1])
##        print title
##        data_np = np.array([(title,0)], dtype =dt)


if __name__ == '__main__':
    url = "http://goo.gl/BxZp2J"
    filename = "y_bid.csv"
    tree = parser_etree(url)
    data = filter_etree(tree)
    collector_txt(data)
    readfile(filename)
