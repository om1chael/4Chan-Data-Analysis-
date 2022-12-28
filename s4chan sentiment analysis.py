#  Get the dat data from 4chan website 
#       - Get all the data from the website 
#       - run sentiment anlsysi on it
#       -   -- What does this mean/how do you atually do that ?
#
##
##
'''

driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")

driver.get('https://boards.4channel.org/vg/thread/411424387')

html = driver.page_source

with open('aid.txt', 'w') as file:
    file.write(html)

'''


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



'''   
def Download_html_page(url,url_Name):        
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
    driver.get(url)
    Write_File_Text(url_Name)
#   html = open(url_Name+'.txt', 'r')
#   print("Download_html_page")
    return driver.page_source
    backlink

'''   

def load_website():
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
    html = driver.get(url)
    pageSource = html

print(Write_File_Text("aid"))


def Scrape_Website(url,Json_File_Name, save=True):
    data = {}
     
    soup = BeautifulSoup(url, features="html.parser")
    for i in soup.find_all("blockquote", class_="postMessage"):
    ##  Find all the ID tags of the post 
        extract_NO = " ".join(re.findall("[0-9]+", i.get("id")))
    ##  Find all the Tags in the message     
        match = re.findall(">>[0-9]+", i.text)
    ##  Replace the tag in the message with a space. 
        filter_message = re.sub(r'>>[0-9]+', " ".join(match)+" ", i.text)
    ##  add the data to the Dict 
        data[extract_NO]= filter_message
    if(save):
        drump_json_file(Json_File_Name,data)
    return data
    



## cleaned_data_Non_Mapping = Load_File_Json('User-messages.json')
## MAP OPS with reponses
def Map_Ops_to_Responses(cleaned_data_Non_Mapping, file_name, save=True):
    new_mapping={}
    for keys in cleaned_data_Non_Mapping:
        val_ = cleaned_data_Non_Mapping[keys] 
        new_mapping[keys] = re.findall(">>[0-9]+", val_ )
    if(save):
        drump_json_file(file_name,new_mapping)
    else:
        print(new_mapping)
        return new_mapping


## scrapped_data = Scrape_Website("https://boards.4channel.org/vg/catalog","scrapped_data",True)
## Map_Ops_to_Responses(scrapped_data,"scrapped_data",True)



cleaned_data = Load_File_Json('User-messages.json')
print(cleaned_data)
format_dict = {}






def map_data_add_nodes(cleaned_data):
    pass



map_data_add_nodes(cleaned_data)







'''
from graph_tools import Graph,graph_draw 
graph_tools.Graph.vertices
g = Graph(directed=True)
g.add_edge(1, 2)
g.add_edge(2, 3)
graph_draw(g, vertex_text=g.vertex_index, output="two-nodes.pdf")

print(g)



    g = Network("500px", "500px")
    g = Network(directed =True)
    g.set_options(options)
    new_dic = [k for k,v in cleaned_data.items() if len(v) >= 7]
    print(new_dic)
    for keys in new_dic:
        g.add_node(keys)
        for vals in [re.sub(r'>>', '', i) for i in cleaned_data[keys]][:-2]:
            g.add_node(vals)
        
    for keys in list(cleaned_data):
        filt = [re.sub(r'>>', '', i) for i in cleaned_data[keys]]
        
        if( keys in g.get_nodes()):
            for k in filt:
                g.add_node(k)
                g.add_edge(keys,k)
'''

