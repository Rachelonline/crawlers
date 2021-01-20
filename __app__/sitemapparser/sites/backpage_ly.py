from urllib.parse import urljoin
from bs4 import BeautifulSoup

#These IDs correspond to all the sketchy categories on Backpage, from dating to escorts. They are embedded in each listing URL.
category_ids = [
    "category,98", 
    "category,99", 
    "category,100", 
    "category,101", 
    "category,105", 
    "category,104", 
    "category,131", 
    "category,69", 
    "category,70", 
    "category,71", 
    "category,72", 
    "category,73", 
    "category,74"
]

countries = {
    "country0" : "country,US",
    "country1" : "country,CA",
    "country2" : "country,EU",
    "country3" : "country,AP",
    "country4" : "country,AO",
    "country5" : "country,LA",
    "country6" : "country,AF"
}

def backpage_ly(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    #The pattern of region IDs was figured out by observing the website URLs.
    #These starting values below are incremented depending on the alphabetical order of the region.
    us_region_id = 782041
    world_region_id = 782099
    country_id = None
    city_name = None
    states_list = soup.findAll("div", class_= "state-list mx-2")
    for states in states_list:
        for country in countries:
            if (states.get("id") == country):
                country_id = countries[country]
        for state in states.findAll("div", class_="state-container"):
            if (country_id == "country,US"):
                #This if-statement accounts for an error I noticed in the numbering system of states from South Carolina to Texas.
                if (us_region_id == 782082):
                    us_region_id += 11
                elif (us_region_id == 782095):
                    us_region_id -= 9
                else:
                    us_region_id += 1
                for city in state.findAll("li", class_="city-item"):
                    for cityname in city.findAll("a"):
                        city_name = cityname.get("title").replace(" ", "+")
                    for category in category_ids:
                        links.append(f"https://www.backpage.ly/search/region,{us_region_id}/city,{city_name}/{category}/{country_id}")
            else:
                world_region_id += 1
                for city in state.findAll("li", class_="city-item"):
                    for cityname in city.findAll("a"):
                        city_name = cityname.get("title")
                    for category in category_ids:
                        links.append(f"https://www.backpage.ly/search/region,{world_region_id}/city,{city_name}/{category}/{country_id}")
    return links