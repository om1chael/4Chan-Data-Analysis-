#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from selenium import webdriver
import re
import json 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pyvis.network import Network

##### Save files:
def Write_File_Text(File_Name):
    with open(File_Name+'.txt', 'w') as file:
        file.write(File_Name)
        
def drump_json_file(name,data):
    with open(name+'.json', 'w') as file:
        json.dump(data, file)

##### load files:
def Load_File_Json(File_Name):
    with open(File_Name) as f:
        Json_file = json.load(f)
        print(File_Name+" Loaded")
        return Json_file
def load_website():
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
    html = driver.get(url)
    return html


# # Scrapping WebData 

# In[412]:


def Scrape_Website(url,Json_File_Name, save=False):
    data = {}
    core_data = []
    user_responses= {}
    soup = BeautifulSoup(url, features="html.parser")
    
    for i in soup.find_all("div", class_="postContainer replyContainer"):
    #   Find all the ID tags of the post 
        extract_NO = " ".join(re.findall("[0-9]+", i.get("id")))
    #   Find all the Tags in the message     
        match = re.findall(">>[0-9]+", i.text)
    #   Replace the tag in the message with a space. 
        filter_message = re.sub(r'>>[0-9]+', " ".join(match)+" ", i.text) 
        message_find = i.find("blockquote",class_="postMessage")
        Response = i.find("div", class_="backlink")
    #   filter_message,
    #   data[extract_NO] = [core_data]
    
        OP_ID = i.get("id")[2:]
    
        Response = i.find("div", class_="backlink")
        match = re.findall(">>[0-9]+", message_find.text)
        filter_message = re.sub(r'>>[0-9]+', " ".join(match)+" ", message_find.text)
                
        # data[OP_Id] = ops_origal_message,people_who are_replying
        if(Response != None):
            user_backLink = []
 
            print("A", "\n",OP_ID,"\n", message_find.text, filter_message) 
            print("-------",match)
            
            for i in Response.get_text().split():
                user_backLink.append(i)
            print(user_backLink)
            data[">>"+OP_ID] = [filter_message,user_backLink] 

        else:
            print("B", "\n",OP_ID,"\n",filter_message)
            data[">>"+OP_ID] = [filter_message,None]
            
    print("done")   
    return data


# In[413]:


Html = open("aid.txt")
check = Scrape_Website(Html, "Text")


# In[ ]:

soup = BeautifulSoup(Html, features="html.parser")

chat = []
# Reccursive alg that finds all the back liknk for the website 
def find_None(check,backlink,chat):
    start = check[backlink]
    #Base Case, if dict has None in the options it will stop 
    if(None in start):
        return start[0]
    else:
        backlink = start[1]
        for i in backlink:
            find_None(check,i,chat)
            chat.append(i)
    return chat

# Final_mapping

def Final_mapping(check):
    # Go though each key in the dict and align each conversion 
    # With the reply that came after that message
    user_dis_op= []
    final_data = {}
    g_ = []
    for keys in check.keys():
        if(None in check[keys]):
            final_data[str(check[keys][0])] = None
        else:
            chat = []
            val = find_None(check,keys,chat)
            for fina in val:
                chat = []
                g_.append(check[fina][0])
            final_data[str(check[keys][0])] = g_
            g_ = []
    return final_data


# In[776]:


res = Final_mapping(check)


# In[636]:


res['>>411462387 Sorry, but I prefer my fairies less human.']


# In[1144]:


def clean_data(data):
    cleaned_data = []
    for i in set(new_dict[data[1]]):
        ##  Replace the tag in the message with a space.
        ## Replace >>68567628 with an empty space 
        filter_message = re.sub(r'>>[0-9]+'," ", i)
        cleaned_data.append(filter_message)
    return cleaned_data   
        
# In[822]:


def clean_clone_keys_vals(res):
    # copy the dict and makes sure that copies are not present as keys
    new_dict = res.copy()
    for topics in res.copy().keys():
        if(res[topics] == None):
            pass
        else:
            topic = list(res.copy()[topics])
            for words in topic:
                if(words in new_dict.keys()):
                    del new_dict[words]
        return new_dict
new_dict = clean_clone_keys_vals(res)


# In[871]:


new_dict[">>411424387  (OP)Whats the next big thing for textgen, and how soon can we expect it?"]

print(new_dict["this is not ok"])


# In[922]:


def Sorted_Stop_words(new_dict):
    sorted_data = []
    finally_Done = []
    sorted_ = {}
    sub_comments = []

    tokens_without_sw = [word for word in new_dict.keys() if not word in STOPWORDS]

    for text in tokens_without_sw:
        filter_ = [word for word in text.split() if not word in STOPWORDS]
        finally_Done.append(" ".join(filter_))


    for i in finally_Done:
        ##  Replace the tag in the message with a space. 
        filter_message = re.sub(r'>>[0-9]+'," ", i)
        sorted_data.append(filter_message)
        sorted_[i] = sub_comments
        sub_comments = []
        
        
    return sorted_data


# In[963]:

# In[964]:


sorted_data = Sorted_Stop_words(new_dict)
sorted_data


# # Sentiment Analysis

# In[1167]:


from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt

def Make_worldCloud(sorted_data,title):
    wordcloud = WordCloud(
        background_color="#6B5B95",
        colormap="Set2",
        collocations=False).generate(str(sorted_data))
    plt.figure(figsize=[11,11])
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    
    if(len(title.split())>6):
        f = int(len(title.split())/2)
        plt.title(" ".join(title.split()[0:f]))
    else:
        plt.title(title)
    plt.show()


# In[1165]:


def find_Biggest_chat(data,convo_length):
    # Find the topic with the longest converstion 
    # Return the converstion title 
    # Return length of converstion
    Meaningful_convs = {}
    biggest_convo = 0
    topic = ""
    for  keys in data.keys():
        if(data[keys] != None):
            set_convo = len(set(data[keys]))
            if(set_convo > convo_length):
                topic = keys
                
                Meaningful_convs[keys] = set(data[keys])
                if(set_convo > biggest_convo):
                    biggest_convo=set_convo
                    topic = data[keys]
    # ("Topics:-",Meaningful_convs.keys(),"Length of converstaion:-",biggest_convo)
    return Meaningful_convs.keys()
        


# In[ ]:

# In[1169]:


for Topics in Biggest_Topics:
    print(Topics)
    Make_worldCloud(new_dict[Topics], Topics)
