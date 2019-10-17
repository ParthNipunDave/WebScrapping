import re
import requests
from bs4 import  BeautifulSoup

url= "https://www.imdb.com/india/top-rated-indian-movies/?sort=ir,desc&mode=simple&page=1"
response = requests.get(url)
soup = BeautifulSoup(response.text,features="html.parser")

crew = [a.attrs.get("title")for a in soup.select('td.titleColumn a')]

title=[ b.attrs.get('alt')for b in soup.select('td.posterColumn  img') ]


ratings=([float(b.attrs.get('data-value')) for b in soup.select('td.posterColumn span[name=ir]')])
rel_year=[]
year = [ soup.find_all('span',class_='secondaryInfo')]
for i in year[0]:

    rel_year.append(str(i.text).strip('()'))

movie_detail = {}
cnt=0
movie_list=[]
for cast,titles,rel,rate in zip(crew,title,rel_year,ratings):
    cnt=cnt+1

    movie_detail={
        "Rank":cnt,
        "Title":titles,
        "ReleaseDate":rel,
        "Ratings":rate,
        "Cast":cast

    }
    movie_list.append(movie_detail)

def successfulYear():
    from collections import Counter
    year_count = []
    for i in movie_list:

        year_count.append(i["ReleaseDate"])


    year_count = dict(Counter(year_count))




    print("-----------------Most Successful Year of Indian Cinema According To IMBD--------------------",sep="\n")
    print()
    totalShare=0.0
    totalCount=0

    for i in year_count.keys():
        percent = (year_count[i]/len(movie_list))*100

        print('\t\t\t\t\t\tRelease Year\t Count\t Share(%)')
        if year_count[i]>9:
            print('\t\t\t\t\t\t',i,"\t\t\t",year_count[i],"\t\t","{:.2f}".format(percent))
            totalCount = totalCount + year_count[i]
            totalShare = totalShare + percent
        else:
            print('\t\t\t\t\t\t',i, "\t\t\t", year_count[i], "\t\t\t", "{:.2f}".format(percent))
            totalCount = totalCount + year_count[i]
            totalShare = totalShare + percent

    print("Total number of movies \t\t ",totalCount," Total Number of share ","{:.0f}".format(totalShare))




from collections import Counter
def favDirector():

    director=[]
    actor=[]

    for i in movie_list:
        cast_crew=[str(i["Cast"]).split(',')]
        for i in cast_crew:


            director.append(str(i[0]).strip(' (dir.)'))
            actor.append(str(i[1]).lstrip(' '))
            actor.append(str(i[2]).lstrip(' '))
    print("-------------------List of Top Director in Descending Order--------------")
    print(Counter(director))
    print("-------------------List of Top Actors/Actress in Descending Order--------------")
    print(Counter(actor))








successfulYear()
print('----------------------------------------')
favDirector()