#import warnings
import pandas as pd
import re
import urllib
from bs4 import BeautifulSoup
#warnings.filterwarnings("ignore")
#Sorting by Date in ascending order
df=pd.read_csv('After_Scrape.csv')
df['Published_Date'] = pd.to_datetime(df['Published_Date'])
df = df.sort_values(['Published_Date'], ascending=True)
df.to_csv('After_DateSort.csv', index=False)
excel=pd.read_csv("After_DateSort.csv")

print "Please wait....Bucketizing of comment count is in process"

#To Catagerize the comment count
excel["F_no_comment"]=" "
for i in range(0,len(excel)):
    if (excel.No_Comments[i]<=30):
        excel.F_no_comment[i]=0
    if (excel.No_Comments[i]>30) & (excel.No_Comments[i]<=70):
        excel.F_no_comment[i]=1
    if (excel.No_Comments[i]>70) & (excel.No_Comments[i]<=120):
        excel.F_no_comment[i]=2
    if (excel.No_Comments[i]>120) & (excel.No_Comments[i]<=200):
        excel.F_no_comment[i]=3
    if excel.No_Comments[i]>200:
        excel.F_no_comment[i]=4

#To dintinguish each Genre
excel["F_investigations"] = excel['Domain'].str.count("investigations")
excel["F_sports"] = excel['Domain'].str.count("sports")
excel["F_crime-and-justice"] = excel['Domain'].str.count("crime-and-justice")
excel["F_food"] = excel['Domain'].str.count("food")

"""#To retrieve the individual sum count of each Genre.
excel["count_genre"]=" "
for i in range(0,len(excel)):
    if excel.Domain[i]=="investigations":
        excel.count_genre[i]=excel['Domain'].str.count("investigations").sum()
    if excel.Domain[i]=="sports":  
        excel.count_genre[i]=excel['Domain'].str.count("sports").sum()
    if excel.Domain[i]=="crime-and-justice":  
        excel.count_genre[i]=excel['Domain'].str.count("crime-and-justice").sum()
    if excel.Domain[i]=="food":
        excel.count_genre[i]=excel['Domain'].str.count("food").sum()
        """
#To retrieve the Past_Count_article_author/excel should be sorted by Date       
excel["F_count_article_author"]=" "
excel.F_count_article_author[0]=0
li=list(excel.Author.unique())
for i in range(0,len(li)):
    count=-1
    for j in range(0,len(excel)):
        if li[i]==excel.Author[j]:
                excel.F_count_article_author[j]=count=count+1    
                
#To retrieve the Avg_comment_count_Genre of omain in order to retrieve the Avg.comment count by Genre
excel["Domain_Count"]=" "
excel.Domain_Count[0]=1
li=list(excel.Domain.unique())
for i in range(0,len(li)):
    count=0
    sum_comment=0
    for j in range(0,len(excel)):
        if li[i]==excel.Domain[j]:
                excel.Domain_Count[j]=count=count+1 

excel["Sum_Comment"]=" "
#excel.Domain_Count[0]=1
li=list(excel.Domain.unique())
for i in range(0,len(li)):
    previous=-1
    Sum_Comment=excel.No_Comments[i]
    for j in range(0,len(excel)):
        previous=previous+1
        if li[i]==excel.Domain[j]:
                if j!=0:
                    Sum_Comment=excel.No_Comments[i]
                    excel.Sum_Comment[j]=int(excel.No_Comments[j])+int(excel.Sum_Comment[j-previous])
                    #print int(Sum_Comment)+int(excel.No_Comments[j-previous])
                    Sum_Comment=excel.Sum_Comment[j]
                    previous=0
                else:
                    excel.Sum_Comment[j]=int(excel.No_Comments[j])
                    
#Avg_comment_count_Genre formula
excel["F_avg_count_genre"]=" "
excel.F_avg_count_genre=excel.Sum_Comment/excel.Domain_Count

#Count of Genre
excel["F_genre_count"]=" "
excel.F_genre_count[0]=0
li=list(excel.Domain.unique())
for i in range(0,len(li)):
    count=-1
    for j in range(0,len(excel)):
        if li[i]==excel.Domain[j]:
                excel.F_genre_count[j]=count=count+1 

#Logic for lenght of content

excel["F_length_content"]=" "
li=list()
f = open("vivek.txt", "wb")
def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True
    
print "Please wait....now Positive and Negative content count is in process"

fconn=open('links_300')
links=fconn.read().splitlines()#read the entire html into this variable
fconn.close()
c=0
#l=1
for line in links: 
    #print line+" "+str(l)
    #l=l+1
    html = urllib.urlopen(line)
    soup = BeautifulSoup(html)
    data = soup.findAll(text=True)
 
    result = filter(visible, data)
#print result
#type(result).encode('ascii', 'ignore')
    f.write(str(result)+'\n')
    li.append(str(result))
    excel.F_length_content[c]=len(li[c])/10
    c=c+1
f.close()

excel["Author_Count"]=" "
excel.Author_Count[0]=1
li=list(excel.Author.unique())
for i in range(0,len(li)):
    count=0
    sum_comment=0
    for j in range(0,len(excel)):
        if li[i]==excel.Author[j]:
                excel.Author_Count[j]=count=count+1 
                
# Postive and Negative Comment count
excel["F_pos_count"]=" "
excel["F_neg_count"]=" "
def loadLexicon(fname):
    newLex=set() #make a new empty set
    lex_conn=open(fname)#open a connection to the lexicon file
    #add every word in the file to the set
    for line in lex_conn: # for every line in the file
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close() #cloes the collection

    return newLex # work is done, return the lexicon


#load the positive and negative lexicons
posLex=loadLexicon('positive-words.txt')
negLex=loadLexicon('negative-words.txt')

file_writer=open('results.txt','w') #open a write connection to the output file

data_conn=open('vivek.txt') # open a read connection to the input file
k=0
for line in data_conn: # for every line in the file (1 review per line)
    posList=[] #list of positive words in the review
    negList=[] #list of negative words in the review

    line=line.lower().strip()#lower-case and remove dead space from the beginning and end of the string
    
    words=line.split(' ') # split on the space to get list of words
    for word in words: #for every word in the review
        if word in posLex: # if the word is in the positive lexicon
            posList.append(word) #update the positive list for this review
            
        if word in negLex: # if the word is in the negative lexicon
            negList.append(word) #update the negative list for this review
            #print len(negList)

    decision='Neutral'#in the beginning the decision is netural        
    if len(posList)>len(negList): # more pos words than neg
        decision='Positive' #update decision
        
    elif len(negList)>len(posList):  # more neg than pos
        decision='Negative' # update decision
        
         
    file_writer.write(line+'\n') #write the review
    file_writer.write(str(posList)+'\n') # write list of positive words
    file_writer.write(str(negList)+'\n') # write list of negative words     
    file_writer.write(decision+'\n\n') #write the decision
    excel.F_pos_count[k]=len(posList)
    excel.F_neg_count[k]=len(negList)
    k+=1

#close the two file connectionss
file_writer.close()
data_conn.close()


#Avg past comment count by each author
excel["Sum_Author_Comment"]=" "
#excel.Domain_Count[0]=1
li=list(excel.Author.unique())
for i in range(0,len(li)):
    previous=-1
    Sum_Author_Comment=excel.No_Comments[i]
    for j in range(0,len(excel)):
        previous=previous+1
        if li[i]==excel.Author[j]:
                if j!=0:
                    Sum_Author_Comment=excel.No_Comments[i]
                    excel.Sum_Author_Comment[j]=int(excel.No_Comments[j])+int(excel.Sum_Author_Comment[j-previous])
                    #print int(Sum_Comment)+int(excel.No_Comments[j-previous])
                    Sum_Author_Comment=excel.Sum_Author_Comment[j]
                    previous=0
                else:
                    excel.Sum_Author_Comment[j]=int(excel.No_Comments[j])
excel["F_avg_comment_author"]=" "
excel.F_avg_comment_author=excel.Sum_Author_Comment/excel.Author_Count

print "Please wait....now Past article count of each Author for each Genre is in process"
#Past article count of each Author for each Genre

Dmn=list(excel.Domain.unique())
Auth=list(excel.Author.unique())
excel["F_past_count_article_genre_author"]=" "
c=0
k=-1
for i in Auth:
        k=k+1
        c=0
        for j in range(0,len(excel)):
            if (excel.Domain[j]=="crime-and-justice") & (excel.Author[j]==Auth[k]):
                    excel.F_past_count_article_genre_author[j]=c
                    #print j
                    #print c
                    #print "inside:"+str(k)
                    c=c+1
                    #print excel.Author[j]
                    #if (excel.Author[j]!=Auth[k]):
c=0
k=-1
for i in Auth:
        k=k+1
        c=0
        for j in range(0,len(excel)):
            if (excel.Domain[j]=="sports") & (excel.Author[j]==Auth[k]):
                    excel.F_past_count_article_genre_author[j]=c
                    #print j
                    #print c
                    #print "inside:"+str(k)
                    c=c+1
c=0
k=-1
for i in Auth:
        k=k+1
        c=0
        for j in range(0,len(excel)):
            if (excel.Domain[j]=="investigations") & (excel.Author[j]==Auth[k]):
                    excel.F_past_count_article_genre_author[j]=c
                    #print j
                    #print c
                    #print "inside:"+str(k)
                    c=c+1
c=0
k=-1
for i in Auth:
        k=k+1
        c=0
        for j in range(0,len(excel)):
            if (excel.Domain[j]=="food") & (excel.Author[j]==Auth[k]):
                    excel.F_past_count_article_genre_author[j]=c
                    #print j
                    #print c
                    #print "inside:"+str(k)
                    c=c+1

#Export to seperate csv file
excel.to_csv("After_Feature.csv",index=False)
print "Thank you very much for having the patience, file has been processes with the name After_Feature.csv"