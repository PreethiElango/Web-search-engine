import requests    
import re    
from urllib.parse import urlparse 
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json

def removeTagsLineDelimiterNumbers(lines): 
    lines=str(lines)
    pattern = re.compile('<.*?>|\n|[0-9].*')
    text = re.sub(pattern,' ',lines)
    return text
    

# takes string of words as a input
def removePunctuationSingleDoubleCharacterGetTokens(lines):
    translator = str.maketrans(string.punctuation,' '*len(string.punctuation))
    lines = lines.translate(translator)
    lines = lines.split()
    return lines

# takes list of words as a input
def removeSingleDoubleCharacterWordStopWordsAndStemming(tokens):
    ps = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    tokens = [ps.stem(token) for token in tokens if token not in stop_words] 
    return [token for token in tokens if len(token)>1 and token not in stop_words]



def url_traversing(url):
#     url="http://cs.uic.edu/"
    visited=[]
    next_link=[]
    content={}
    outlink={}
    next_link.append(url)
    while len(visited)<3000:
        print(len(visited))
        url=next_link.pop(0)
        if url[-1]=='/':
          n=len(url)
          url=url[:n-1]
        if url in visited:
            continue
        else:
            # html = requests.get(url)
            try:
                html = requests.get(url)
            except:
                continue 
            visited.append(url)
            html=html.content.decode('latin-1')
            text=removeTagsLineDelimiterNumbers(html)
            text=removePunctuationSingleDoubleCharacterGetTokens(text)
            text= removeSingleDoubleCharacterWordStopWordsAndStemming(text)
            content[url]=text
            parsed = urlparse(url)
            links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html) #getshref
            base = f"http://{parsed.netloc}"  
            new=[]
            for i, link in enumerate(links): 
                    if  'confluence.' in link or'mailto:' in link or 'jpg' in link or 'tel' in link or'#' in link or'.pdf' in link or 'maps.' in link or 'youtube.' in link or 'twitter' in link or'facebook' in link or 'login'in link:
                        continue
                    else:
                        new.append(link)
            links=[]
            for i, link in enumerate(new):    
                        if not urlparse(link).netloc:
                                link_with_base = base + link    
                                links.append(link_with_base)
                        elif 'uic.edu' not in urlparse(link).netloc:
                            continue
                        else:
                            links.append(link)   
            for i in links:
                next_link.append(i)
            k=set(links)
            outlink[url]=list(k)
    import json
    with open('visited_new_final.json', 'w') as json_file:
        json.dump(visited, json_file)
    with open('next_link_new_final.json', 'w') as json_file:
        json.dump(next_link, json_file)
    with open('content_new_final.json', 'w') as json_file:
        json.dump(content, json_file)
    with open('outlink_new_final.json', 'w') as json_file:
        json.dump(outlink, json_file)