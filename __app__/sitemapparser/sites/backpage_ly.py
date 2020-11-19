from urllib.parse import urljoin
from bs4 import BeautifulSoup

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
    us_region_id = 782041
    world_region_id = 782099
    country_id = " "
    city_name = " "
    states_list = soup.findAll("div", class_= "state-list mx-2")
    for states in states_list:
        for country in countries:
            if (states.get("id") == country):
                country_id = countries[country]
        for state in states.findAll("div", class_="state-container"):
            if (country_id == "country,US"):
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
                        links.append("https://www.backpage.ly/search/region," + str(us_region_id) + "/city," + city_name + "/" + category + "/" + country_id)
            else:
                world_region_id += 1
                for city in state.findAll("li", class_="city-item"):
                    for cityname in city.findAll("a"):
                        city_name = cityname.get("title")
                    for category in category_ids:
                        links.append("https://www.backpage.ly/search/region," + str(world_region_id) + "/city," + city_name + "/" + category + "/" + country_id)
    return links
        

# If we are able to crawl URLS without a download of the HTML file, this would work.
# It would probably be more accurate too.

'''
def get_region_url(html):
    soup = BeautifulSoup(html, "html.parser")
    region_urls = []
    cities = soup.find_all("li", class_="city-item")
    for city in cities:
        for link in city.find_all("a"):
            region_urls.append(urljoin("https://www.backpage.ly", link.get("href")))
    return region_urls

def right_category(str):
    if (category_id not in str):
        return False
    else:
        return True

def get_category_url(region_urls):
    category_urls = []
    for region in region_urls:
        soup = BeautifulSoup(region, "html.parser")
        categories = soup.find_all("li", class_="category-item")
        for category in categories:
            for href in category.find_all("a"):
                link = href.get("href")
                if (right_category(link)):
                    category_urls.append(link)
    return category_urls
'''
    