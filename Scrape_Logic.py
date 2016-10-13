from urllib import urlopen
import urllib2,os,sys,time
from bs4 import BeautifulSoup
import re
import csv
title=[]
date=[]
author=[]
cluster=[]
comment=[]

fo=open("MJ_URL_1","wb")

#make a new browser, this will download pages from the web for us. This is done by calling the 
#build_opener() method from the urllib2 library
browser=urllib2.build_opener()

#desguise the browser, so that websites think it is an actual browser running on a computer
browser.addheaders=[('User-agent', 'Mozilla/5.0')]
if not os.path.exists('MJ_2'):os.mkdir('MJ_2')
links=set()   # Ride-off duplicates
domain1=set()
page1=1
pg_no=0       #traverse through different page URL

#urlf="http://www.motherjones.com/topics/sports?page=0"
meta="05/14"
urlc=["http://www.motherjones.com/environment","http://www.motherjones.com/politics",
"http://www.motherjones.com/media","http://www.motherjones.com/topics/crime-and-justice"
,"http://www.motherjones.com/topics/investigations"]
for urlb in urlc:
    for pg_no in range(0,8):
        urlf=urlb+"?page="+str(pg_no)
        
        #print urlf
        #print urlb+"**********"
        pg_no=pg_no+1
        optionsUrlf=urlopen(urlf)
        soupf = BeautifulSoup(optionsUrlf,"lxml")
        for tagf in soupf.findAll('a', href=True):                     #To retrieve all the hyperlinks of particular page
                if str(tagf['href']).startswith("/") and len(str(tagf['href']))>25:
                            temp=(str(tagf['href']))
                            if "page" not in temp:
                                    tempf=("http://www.motherjones.com"+temp)
                                    M=re.search("/(.*?)/",temp)
                                    if M: 
                                        if M.group()!="/about/" and M.group(1)!="photoessays":
                                            S=re.search('http://www.motherjones.com/topics/(.*)$',urlb)
                                            if S:
                                                      #if S.group(1)=="sports" or S.group(1)=="food":
                                                               #print str(S.group(1))
                                                               links.add(tempf+"     "+str(S.group(1)))
data="/08 04:40"
urla=["http://www.motherjones.com/topics/sports","http://www.motherjones.com/topics/food"]
for urlb in urla:
    for pg_no in range(0,2):
        urlf=urlb+"?page="+str(pg_no)
        #print urlf
        #print urlb+"**********"
        pg_no=pg_no+1
        optionsUrlf=urlopen(urlf)
        soupf = BeautifulSoup(optionsUrlf,"lxml")
        for tagf in soupf.findAll('a', href=True):                     #To retrieve all the hyperlinks of particular page
                if str(tagf['href']).startswith("/") and len(str(tagf['href']))>25:
                            temp=(str(tagf['href']))
                            if "page" not in temp:
                                    tempf=("http://www.motherjones.com"+temp)
                                    M=re.search("/(.*?)/",temp)
                                    if M: 
                                        if M.group()!="/about/" and M.group(1)!="photoessays":
                                            S=re.search('http://www.motherjones.com/topics/(.*)$',urlb)
                                            if S:
                                                      #if S.group(1)=="sports" or S.group(1)=="food":
                                                               #print str(S.group(1))
                                                               links.add(tempf+"     "+str(S.group(1)))


                                                            
"""urld=["http://www.motherjones.com/environment","http://www.motherjones.com/politics",
"http://www.motherjones.com/media","http://www.motherjones.com/topics/crime-and-justice"
,"http://www.motherjones.com/topics/investigations"]
for urlb in urld:
    for pg_no in range(9,17):
        urlf=urlb+"?page="+str(pg_no)
        pg_no=pg_no+1
        optionsUrlf=urlopen(urlf)
        soupf = BeautifulSoup(optionsUrlf,"lxml")
        for tagf in soupf.findAll('a', href=True):                     #To retrieve all the hyperlinks of particular page
                if str(tagf['href']).startswith("/") and len(str(tagf['href']))>25:
                            temp=(str(tagf['href']))
                            if "page" not in temp:
                                    tempf=("http://www.motherjones.com"+temp)
                                    M=re.search("/(.*?)/",temp)
                                    if M: 
                                        if M.group()!="/about/" and M.group(1)!="photoessays":
                                            S=re.search('http://www.motherjones.com/topics/(.*)$',urlb)
                                            if S:
                                                      #if S.group(1)=="sports" or S.group(1)=="food":
                                                               #print str(S.group(1))
                                                               links.add(tempf+"     "+str(S.group(1)))"""
                            
urle=["http://www.motherjones.com/topics/sports","http://www.motherjones.com/topics/food"]
for urlb in urle:
    for pg_no in range(0,2):
        urlf=urlb+"?page="+str(pg_no)
        #print "Entered inside sir" + urlf
        #print urlf
        #print urlb+"**********"
        pg_no=pg_no+1
        optionsUrlf=urlopen(urlf)
        soupf = BeautifulSoup(optionsUrlf,"lxml")
        for tagf in soupf.findAll('a', href=True):                     #To retrieve all the hyperlinks of particular page
                if str(tagf['href']).startswith("/") and len(str(tagf['href']))>25:
                            temp=(str(tagf['href']))
                            #print temp
                            if "page" not in temp:
                                    tempf=("http://www.motherjones.com"+temp)
                                    M=re.search("/(.*?)/",temp)
                                    if M: 
                                            if M.group(1)!="about" and M.group(1)!="photoessays" and M.group(1)!="authors":
                                                    S=re.search('http://www.motherjones.com/topics/(.*)$',urlb)
                                                    if S:
                                                      #if S.group(1)=="sports" or S.group(1)=="food":
                                                               #print str(S.group(1))+" "+str(pg_no)
                                                               links.add(tempf+"     "+str(S.group(1)))
                                                               
for link in links:
    fo.write(link+'\n')
    url=link
    M=re.search(".*?     (.*?)$",link)
    if M:
        d=str(M.group(1))
        d=re.sub('\s','',d)
        #print d
        cluster.append(d)
    print 'processing page :', page1
    print link
    try:
        #use the browser to get the url.
        response=browser.open(url)# this might throw an exception if something goes wrong.
    
    except Exception as e: # this describes what to do if an exception is thrown
        error_type, error_obj, error_info = sys.exc_info()# get the exception infomration
        print 'ERROR FOR LINK:',url #print the link that cause the problem
        print error_type, 'Line:', error_info.tb_lineno #print error info and line that threw the exception
        continue#ignore this page.
    
    #read the response in html format. This is essentially a long piece of text
    myHTML=response.read()

    #write the page to a new html file
    fwriter=open('MJ_2/'+str(page1)+'.html','w')
    fwriter.write(myHTML)
    fwriter.close()
    
    #wait for 5 seconds
    time.sleep(5)
    page1+=1
    
var=1
print '\n'
    
for r in range(1,page1):
    fconn1=open('MJ_2/'+str(r)+'.html')
    html_new=fconn1.read()#read the entire html into this variable
    tree=BeautifulSoup(html_new,'lxml')
    fconn1.close()
    
    Nam=re.finditer('<h1 class="title">(.*?)</h1>',html_new) #search names
    for N in Nam:
        q=str(N.group(1))
        q=re.sub('[^a-zA-Z\n\.;\s]', '', q)
        #print q
        title.append(q)
    
        dat=re.finditer('<span id="dateline">(.*?)</span>',html_new)
    for D in dat:
        d=str(D.group(1))
        #print "d is:"+str(d)
        if len(d)>25:
            #M=re.search('http://.*?motherjones.com/toc/(.*?)$',d)
            M=re.search('/toc/(.*?)>',d)
            #print M.group(1)
            e=M.group(1)+data
            #print "e is:"+str(d)
            e=re.sub('["]', '', e)
            date.append(e)
        else:
            d=re.sub('[\.>]', '', d)
            date.append(d)
            #print d      
        
    auth=re.finditer('<span class="byline byline-byline">(.*?)</span>',html_new) #search Authorname
    print str(auth)
    if auth:     
          for M in auth:
            p=str(M.group(1))
            if "href" in p:
                if len(p)>70:
                        G=re.search('<a .*?>(.*?)</a>',M.group(1))
                        #— By <a href="/authors/wilbert-rideau">Wilbert Rideau</a> 
                        x=G.group(1)
                        author.append(str(x))
                        break
                else:
                    M=re.search('Photographs by <.*?>(.*?)</a>.*?<.*?>(.*?)</a>',p)  #To extract the author name present inside hyperlink
                    if M:
                        temp_a=M.group(1),"and",M.group(2)
                        temp_a=M.group(1)
                        author.append(str(temp_a))
                        #print temp_a
                        break
            if "Photographs" in p:
                M=re.search('[bB]y (.*?); .*? by (.*?)$',p)
                if M:
                            #temp_a=M.group(1),"and",M.group(2)
                            temp_a=M.group(1)
                            author.append(str(temp_a))
                            #print temp_a
                            break
            else:      
                author.append(p)
                break                
    if len(author)!=len(title):   #If author is absent
                author.append(" ")   
                #print len(author)
                #print len(title)
                continue

print len(title)
print len(date)
print len(author)
print len(cluster)

with open('After_Scrape.csv', 'w') as csvfile:
    fieldnames = ['Title', 'Published_Date','Author','Domain','No_Comments']
    #No_Comments we extracted manually because there was issue with block and thus cant extract through Web Driver
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n') 
    writer.writeheader()
    for i in range(0,len(links)):
        writer.writerow({'Title': title[i], 'Published_Date': date[i], 'Author': author[i],'Domain': cluster[i],'No_Comments':''})