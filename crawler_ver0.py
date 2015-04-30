import time
import urllib2
import lxml.etree as etree
from lxml.html import parse, fromstring

timer = time.strftime("%d%b%Y",time.gmtime())

def parser_etree(url):
    parser = etree.HTMLParser()
    tree = etree.parse(urllib2.urlopen(url),parser)
    return tree

def filter_etree(tree, site ='yahoo'):
    if site == 'yahoo':
        print "Derive yahoo page..."
        data = tree.xpath('//a[@class="ellipsis"]')
        print "Get total " + str(len(data)) + " product"
        return data

def collector(data, site ='yahoo'):
    if site == 'yahoo':
        container = data
        filename = "y_bid.txt"
        bid_file = open(filename,'w')
        for item in container:
            line = unicode(item.text).encode('utf-8')
            bid_file.write("%s\n"%line)
        bid_file.close()
        print "writefile finish " + timer

def cal_score(filename):
        data = open(filename,'w')

if __name__ == '__main__':
    url = "http://goo.gl/BxZp2J"
    tree = parser_etree(url)
    data = filter_etree(tree)
    collector(data)
