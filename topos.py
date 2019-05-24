
# coding: utf-8

# ### Libraries
# 
# Importing required libraries like requests, beautifulsoup and pandas
# 
# Note : requirements.txt is provided for it.

# In[282]:


from urllib.request import urlopen
from bs4 import BeautifulSoup

import pandas as pd


# ## Table from Wikipedia
# 
# There are many tables on the given 
# url : "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
# 
# We are only interested in the fourth table, and hence while querying the page, we only want Pandas to return the 4th table.
# Also, some columns have a colspan of 2, so we remove the first row of the table and create our own headings with the colspan = 2 as two different columns in the final dataframe.
# 
# 
# This is done below.
# 

# In[250]:




url =  "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
df = (pd.read_html(url)[4])
df = df[1:]

headings = df[:1]

df.columns = ['2017rank','City','State[c]','2017estimate','2010 Census','Change',
                 '2016 land area(sq m)', '2016 land area(sq km)','2016 population density(per sq mi)', 
                 '2016 population density(per sq km)', 'Location']




df.tail()


# ### Adding City URL
# 
# The city names have a html tag along, so we extract the individual links for each city in the 'City' column and save it to a list and eventually add that to the final dataframe. 
# 
# Also, extracting the city names and saving them over the city names given by Pandas as Pandas doesnt remove the superscipts. 

# In[283]:



city = []
city_url = []


url =  "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
soup = BeautifulSoup(urlopen(url).read())

for row in soup.findAll('table')[4].tbody.findAll('tr')[1:]:
#     print(row)
    
    row_td = (row.findAll('td')[1].find_all('a'))
#     print(row_td)
    title = (row_td[0].contents)
#     print("title",title)
    url = (row_td[0]['href'])
    city.append(title[0])
    city_url.append(base_url + url)

print(len(city))
print(len(city_url))

df['City'] = city
df['City_urls'] = city_url


# ### Extra Information:
# 
# Finally, we add some extra information from individual city pages. For this we have chosen "Elevation" and "Timezone" as it is mentioned on almost all pages.
# 
# Elevation: Some pages have Elevation specifically mentioned, some have "Highest and Lowest Elevation" 
# However, three pages dont have anything:
# https://en.wikipedia.org//wiki/Chesapeake,_Virginia
# https://en.wikipedia.org//wiki/Jurupa_Valley,_California
# https://en.wikipedia.org//wiki/Everett,_Washington
# 
# For these three pages, we add '0'.
# 
# Similarly, for Timezone, we add '0' if it is none or empty.
# 
# 

# In[278]:


Elevation = []
Timezone = []
for link in city_url:

#     print(link)
    html = urlopen(link)
    soup = BeautifulSoup(html, 'html.parser')

    table = (soup.find('table', {'class' : 'infobox geography vcard'}))


    counter = 0
    for tr in table.find_all('tr'):
        if tr.get('class') == ['mergedtoprow']:
  
            t = (tr.find_all('th'))
    
            if len(t) > 0:
                if "Elevation" in (t[0].get_text().strip('\n'))  or "elevation" in (t[0].get_text().strip('\n')):
                    counter+=1
                    t = (tr.find_all('td'))
                    if len(t) > 0 :

                        if (t[0].get_text().strip('\n')) == None:
                            Elevation.append(str(0))
                        else:
                            Elevation.append(t[0].get_text().strip('\n'))
    if counter == 0:
        Elevation.append(str(0))


    for tr in table.find_all('tr'):
        if tr.get('class') == ['mergedtoprow']:
            link = tr.find('a')
            if link != None:
                t = (tr.find_all('td'))
                if len(t) > 0 and (link.get_text().strip()) == 'Time zone':
                    if t[0].get_text().strip('\n') == None:
                        Timezone.append(str(0))
                    else:
                        Timezone.append(t[0].get_text().strip('\n'))

                  
print(len(Elevation))
print(len(Timezone))


# In[279]:



df['Elevation'] = Elevation
df['Timezone'] = Timezone


# ### Final Dataframe
# 
# This is what the final dataframe looks like.
# We then save it to a .csv file to be later loaded into a BigQuery table.

# In[284]:


df.head()


# In[281]:


df.to_csv("topos.csv")

