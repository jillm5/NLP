
# coding: utf-8

# # NLTK and Web Scraping

# In[1]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import Counter

def cleanSentence(sentence):
    sentence = sentence.split(' ')
    sentence = [word.strip(string.punctuation+string.whitespace) for word in sentence]
    sentence = [word for word in sentence if len(word) > 1 or (word.lower() == 'a' or word.lower() == 'i')]
    return sentence

def cleanInput(content):
    content = content.upper()
    content = re.sub('\n', ' ', content)
    content = bytes(content, 'UTF-8')
    content = content.decode('ascii', 'ignore')
    sentences = content.split('. ')
    return [cleanSentence(sentence) for sentence in sentences]

def getNgramsFromSentence(content, n):
    output = []
    for i in range(len(content)-n+1):
        output.append(content[i:i+n])
    return output

def getNgrams(content, n):
    content = cleanInput(content)
    ngrams = Counter()
    ngrams_list = []
    for sentence in content:
        newNgrams = [' '.join(ngram) for ngram in getNgramsFromSentence(sentence, n)]
        ngrams_list.extend(newNgrams)
        ngrams.update(newNgrams)
    return(ngrams)


content = str(
      urlopen('http://pythonscraping.com/files/inaugurationSpeech.txt').read(),
              'utf-8')
ngrams = getNgrams(content, 3)
print(ngrams)


# In[3]:


def isCommon(ngram):
    commonWords = ['THE', 'BE', 'AND', 'OF', 'A', 'IN', 'TO', 'HAVE', 'IT', 'I', 'THAT', 'FOR', 'YOU', 'HE', 'WITH', 'ON', 'DO', 'SAY', 'THIS', 'THEY', 'IS', 'AN', 'AT', 'BUT', 'WE', 'HIS', 'FROM', 'THAT', 'NOT', 'BY', 'SHE', 'OR', 'AS', 'WHAT', 'GO', 'THEIR', 'CAN', 'WHO', 'GET', 'IF', 'WOULD', 'HER', 'ALL', 'MY', 'MAKE', 'ABOUT', 'KNOW', 'WILL', 'AS', 'UP', 'ONE', 'TIME', 'HAS', 'BEEN', 'THERE', 'YEAR', 'SO', 'THINK', 'WHEN', 'WHICH', 'THEM', 'SOME', 'ME', 'PEOPLE', 'TAKE', 'OUT', 'INTO', 'JUST', 'SEE', 'HIM', 'YOUR', 'COME', 'COULD', 'NOW', 'THAN', 'LIKE', 'OTHER', 'HOW', 'THEN', 'ITS', 'OUR', 'TWO', 'MORE', 'THESE', 'WANT', 'WAY', 'LOOK', 'FIRST', 'ALSO', 'NEW', 'BECAUSE', 'DAY', 'MORE', 'USE', 'NO', 'MAN', 'FIND', 'HERE', 'THING', 'GIVE', 'MANY', 'WELL']
    for word in ngram:
        if word in commonWords:
            return True
    return False

def getNgramsFromSentence(content, n):
    output = []
    for i in range(len(content)-n+1):
        if not isCommon(content[i:i+n]):
            output.append(content[i:i+n])
    return output

ngrams = getNgrams(content, 3)
print(ngrams)


# In[4]:


def getFirstSentenceContaining(ngram, content):
    #print(ngram)
    sentences = content.upper().split(". ")
    for sentence in sentences: 
        if ngram in sentence:
            return sentence+'\n'
    return ""


print(getFirstSentenceContaining('EXCLUSIVE METALLIC CURRENCY', content))
print(getFirstSentenceContaining('EXECUTIVE DEPARTMENT', content))
print(getFirstSentenceContaining('GENERAL GOVERNMENT', content))
print(getFirstSentenceContaining('CALLED UPON', content))
print(getFirstSentenceContaining('CHIEF MAGISTRATE', content))


# # Using Markov's model - text prediction

# In[5]:


from urllib.request import urlopen
from random import randint

def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

def retrieveRandomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word

def buildWordDict(text):
    # Remove newlines and quotes
    text = text.replace('\n', ' ');
    text = text.replace('"', '');

    # Make sure punctuation marks are treated as their own "words,"
    # so that they will be included in the Markov chain
    punctuation = [',','.',';',':']
    for symbol in punctuation:
        text = text.replace(symbol, ' {} '.format(symbol));

    words = text.split(' ')
    # Filter out empty words
    words = [word for word in words if word != '']

    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
                # Create a new dictionary for this word
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] += 1
    return wordDict

text = str(urlopen('http://pythonscraping.com/files/inaugurationSpeech.txt')
          .read(), 'utf-8')
wordDict = buildWordDict(text)

#Generate a Markov chain of length 100
length = 100
chain = ['I']
for i in range(0, length):
    newWord = retrieveRandomWord(wordDict[chain[-1]])
    chain.append(newWord)

print(' '.join(chain))


# In[6]:


import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='root', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('USE wikipedia')

def getUrl(pageId):
    cur.execute('SELECT url FROM pages WHERE id = %s', (int(pageId)))
    return cur.fetchone()[0]

def getLinks(fromPageId):
    cur.execute('SELECT toPageId FROM links WHERE fromPageId = %s', (int(fromPageId)))
    if cur.rowcount == 0:
        return []
    return [x[0] for x in cur.fetchall()]

def searchBreadth(targetPageId, paths=[[1]]):
    newPaths = []
    for path in paths:
        links = getLinks(path[-1])
        for link in links:
            if link == targetPageId:
                return path + [link]
            else:
                newPaths.append(path+[link])
    return searchBreadth(targetPageId, newPaths)
                
nodes = getLinks(1)
targetPageId = 28624
pageIds = searchBreadth(targetPageId)
for pageId in pageIds:
    print(getUrl(pageId))


# In[ ]:


import nltk
nltk.download()


# In[ ]:


from nltk import word_tokenize
from nltk import Text
tokens=word_tokenize('Example text for testing and testing')
text=Text(tokens)


# In[ ]:


from nltk.book import *


# In[ ]:


len(text6)/len(set(text6))


# In[ ]:


from nltk import FreqDist
fdist=FreqDist(text6)
fdist.most_common(10)


# In[ ]:


from nltk import bigrams
bigrams=bigrams(text6)
bigramsDist=FreqDist(bigrams)
bigarmsDist[('Str', 'Robin')]


# In[ ]:


from nltk import ngrams
fougrams=ngrams(text6, 4)
fourgramsDist=FreqDist(fourgrams)
fourgramsDist[('father', 'smelt', 'of', 'elderberries')]


# In[ ]:


from nltk.book import *
from nltk import ngrams
fourgrams=ngrams(text6, 4)
for fourgram in fourgrams:
    if fourgram[0]=='coconut':
        print(fourgram)


# In[ ]:


#identifying parts of the speech
from nltk import word_tokenize
text=word_tokenize('there were beautiful flowers scattered around the garder')
from nltk import pos_tag
pos_tag(text)


# In[ ]:


text=word_tokenize('the chair was crooked as one of the legs was broken')
pos_tag(text)


# In[ ]:


#searching for specific text
from nltk import word_tokenize, sent_tokenize, pos_tag
sentences= sent_tokenize ('what is the price tag of a company which contributes to the climate change')
nouns=['NN', 'NNS', 'NNP', 'NNP', 'NNPS']

for sentence in sentences:
    if 'climate' in sentence.lower():
        taggedWords=pos_tag(word_tokenize(sentence))
        for word in taggedWords:
            if word[0].lower()=='climate' and word[1] in nouns:
                print(sentence)

