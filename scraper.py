import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import networkx as ntx
import matplotlib.pyplot as plt
import collections

baseurl = "https://www.flickr.com"
s2="/people/mam08"    #initial page to be scrapped
s3=""
count = 0             #limits the number of nodes in the graph
i=0
user2_list=[]
user1_list=[]
users=[]
count = 0
while(count<181):
    print("waiting")
    time.sleep(1)    #timeout to reduce the traffic on the server
    print("wait over")
    page = requests.get(baseurl + s2 + "/contacts")
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a')                #finds all the anchor tags
    for link in links:
        s1 = link.get('href')                 #finds anchor tags with href
        if (s1 and s1.startswith("/people/") and "page" not in s1):  #setting the scrapping conditions
            s2 = s1;
            print(s2)                          #printing the trailer url of the follwer
            s3 = s2.strip("/people/");
            print(s3)                          #printing only the username of the follower
            user2_list.append(s3)           #adding the users to the list
            count = count + 1               #count the number of nodes added
            print(count)

for i in range(0,len(user2_list)):
    if(i%31 == 0):                          #30 followers are displayed on a single html page
        user1_list.append(user2_list[i])
        g1 = user1_list[i]
    else:
        user1_list.append(g1)

print("Total Number of nodes in the network before:",len(user2_list))
i =0
while(i<len(user2_list)):                    #loop for removing redundant followee-follower pairs where user1 and user2 are the same
    if(user1_list[i] == user2_list[i]):
        user1_list.remove(user1_list[i])
        user2_list.remove(user2_list[i])
    i = i+1

print("Total Number of nodes in the network after removing the redundant pairs:",len(user2_list))  #printing the total Number of nodes in the network

df = pd.DataFrame(                   #storing the pair(users1, users2) in a dataframe for further analysis of the network
    {'User1' : user1_list,
    'User2' : user2_list
     })
print("User1 has User2 as a follower")
print(df)
G1 = ntx.from_pandas_edgelist(df, source='User1', target='User2')      #creating a graph of the network
ntx.draw(G1)

G = ntx.from_pandas_edgelist(df, source='User1', target='User2')
print(G.number_of_nodes())
#Calculating various measures of the network
print("Clustering Co Efficient: ", ntx.average_clustering(G))
print("Diameter: ", ntx.diameter(G))

#printing the histogram for degree distribution
degree_seq = sorted([d for n, d in G.degree()])            #sorting the degrees in ascending order
print(len(degree_seq))
degree_cnt = collections.Counter(degree_seq)            #counter to count the cardinality of each degree
print(degree_cnt.items())                               #printing the degree along with number of nodes with that degree
figure1, axs = plt.subplots()
plt.hist(degree_seq , bins=len(degree_seq), color='b')
axs.set_xticks(range(0,33))
axs.set_xticklabels(range(0,33))

plt.title("Degree Histogram")
plt.ylabel("Number of nodes")
plt.xlabel("Degree")
plt.show()