import bs4 as beautifulsoup
import requests
import smtplib 
"""
Script used to get information regarding the visiting chefs from the RIT dining services website.
@Author: Ivan Lin
@Date: 02/12/2024
"""

URL = "https://www.rit.edu/fa/diningservices/"



if __name__ == "__main__":
    page = requests.get(URL)
    soup = beautifulsoup.BeautifulSoup(page.content, "html.parser")
    for chef in soup.find_all("div", class_="block block-block"):
        shitfood = [food.get_text().strip() for food in chef.find_all("div", class_="visitingchef-event")]
        locations = [location.get_text().strip() for location in chef.find_all("div", class_="visitingchef-location")]
        for i, j in zip(shitfood, locations):
            print(f"{i} loction in {j}")



