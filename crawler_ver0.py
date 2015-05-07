import time
import urllib2
import lxml.etree as etree
from lxml.html import parse, fromstring
import csv
import numpy as np
import operator
import datetime
import os


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

def collector_txt(filename, data, site ='yahoo'):
    if site == 'yahoo' :
        idx = 0
        container_p = data[0]
        container_s = data[1]
        container_t = data[2]
       
        bid_file = open(filename,'w')
        writer =csv.writer(bid_file)
        
        for item in container_p:
            line_p = unicode(item.text).encode('utf-8')
            line_s = unicode(container_s[idx].text).encode('utf-8')
            line_t = unicode(container_t[idx].text).encode('utf-8')
            score = str((len(container_p) - idx))
            data = [score, line_p, line_s, line_t]
            writer.writerow(data)                        
            idx = idx + 1
        
        print "writefile finish "

def readfile(filename):
        content = []
        bid_file = open(filename,'r')
        reader = csv.reader(bid_file)
        for row in reader:
            content.append(row)
        return content

def readfile_dict(filename):
    content = {}
    bid_file = open(filename,'r')
    reader = csv.reader(bid_file)
    for key, value in reader:
        content[key] = value
        #print content
    bid_file.close()
    return content

def sort(content , bytag = 'store', fname_s = 'sorted.csv',fname_rs = 'rankby_s.csv',r_fname = 'rankby_t.csv'):

    
    if bytag == 'store':
        col_tag = 2 #tag for the cols of stors
    elif bytag == 'title':
        col_tag = 3
    elif bytag == 'price':
        col_tag = 1

    if os.path.isfile(fname_rs):
        content_s  = readfile_dict(fname_rs)
        
    else:
        content_s = {}
       

    if os.path.isfile(r_fname):
        r_content = readfile_dict(r_fname)
    else:
         r_content = {}
         
    pool = []
    pool_store = []
    rank = content_s
    rank_t = r_content
    sorted_file = open(fname_s,'w')
    ranked_file = open(fname_rs,'w') 
    f_rank = open(r_fname, 'w')
    
    counter = 0
 
    for idx in range(len(content)): 
        temp = content[idx][col_tag]
        temp_r = content[idx][3]
        in_sorted = matcher(temp,pool_store)
        #print len(pool),in_sorted

        if in_sorted == -1:
            pool.append(content[idx])
            pool_store.append(content[idx][col_tag])
            
            if str(temp) in rank:
                rank[str(temp)] = int(rank[str(temp)]) + 25
            else:
                rank[str(temp)] = 25

        elif in_sorted != -1:
            pool.insert(in_sorted + 1, content[idx])
            pool_store.insert(in_sorted + 1, content[idx][col_tag])
            
            if str(temp) in rank:
                rank[str(temp)] = rank[str(temp)] + 25
            else:
                rank[str(temp)] = 25


        if str(temp_r) in r_content:
            rank_t[str(temp_r)] = int(rank_t[str(temp_r)]) + int(content[idx][0])
           
        else:
            rank_t[str(temp_r)] = int(content[idx][0])
            

    writer_s = csv.writer(sorted_file)
    for p in pool:
        writer_s.writerow(p)

    rank = sorted(rank.items(), key = operator.itemgetter(1))
    rank.reverse()
    rank_t = sorted(rank_t.items(), key = operator.itemgetter(1))
    rank_t.reverse()
    
    writer = csv.writer(ranked_file)
    for value in rank:
        writer.writerow(value)

    print 'sorting by stores complete...'

    print 'Preparing for ranking file'

    w_rank = csv.writer(f_rank)
    for r in rank_t:
        w_rank.writerow(r)
    print 'rank file had been update...'

    sorted_file.close()
    f_rank.close()
    ranked_file.close()

   

def matcher(data, sort_list):

    if type(sort_list) is list:
        if len(sort_list) == 0:
            return -1
        else:
            idx = 0
            flag = -1
            for el in sort_list:
                if el == data:
                    flag = 0
                    tmp = idx
                idx = idx + 1

            if flag != -1:
                return tmp
            else:
                return -1

    elif type(sort_list) is list is False:
        raise ValueError('the type of sort_list should be list')

    elif type(data) != type(sort_list[0]):
        raise ValueError('type should be the same')

def matcher_part(data, sort_list):
    
    if type(sort_list) is list:
        if len(sort_list) == 0:
            return -1
        else:
            idx = 0
            flag = -1
            #print "data = %s"%data
            for el in sort_list:
                #print len(el)
                m_counter = 0 
                for word in data:
                    if word in el and word != ' ':
                        #print word
                        m_counter = m_counter + 1
                        
                        
                if m_counter/len(el) >= 0.75:
                    #print 'counter = %d'%m_counter
                    tmp = idx
                    flag = 0
                    break;
                
                idx = idx + 1
                
            if flag != -1:
                return tmp
            else:
                return -1

    elif type(sort_list) is list is False:
        raise ValueError('the type of sort_list should be list')

    elif type(data) != type(sort_list[0]):
        raise ValueError('type should be the same')


def main():
    url = "http://goo.gl/BxZp2J"
    filename = "y_bid.csv"
    fname_s = 'sorted_t.csv'
    fname_rs = 'ranked_t.csv'

    
    exetime = ['1728','2354','1034']
    key = -1
    while True:
       
        timer = time.strftime("%H%M",time.localtime())
        sec = time.strftime("%S",time.localtime())
        nowtime = datetime.datetime.now()
        msec = str(nowtime.microsecond)
        if timer in exetime:    
            if key == -1:
                key = 0
                tree = parser_etree(url)
                data = filter_etree(tree)
                collector_txt(filename,data)
                content = readfile(filename)
                sort(fname_s, fname_rs ,content)
                

        elif int(msec)%1000000 == 0:
            if key == -1:
                key = 0
                print "waiting..."
        elif (timer in exetime) == False and int(msec)%1000000 != 0:
            key = -1



if __name__ == '__main__':
    url = "http://goo.gl/BxZp2J"
    filename = "y_bid.csv"
    


    #tree = parser_etree(url)
    #data = filter_etree(tree)
    #collector_txt(filename,data)
    content = readfile(filename)
    sort(content)
