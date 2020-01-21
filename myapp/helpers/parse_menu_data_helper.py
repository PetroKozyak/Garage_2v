import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "garage_v2.settings")
from myapp.models import Category, Dish
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


class ParseDataMenu():

    def parse_data(self):
        url = 'https://www.garage.lviv.ua/menu'

        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "html.parser")
        iframe = page_soup.findAll("iframe")[0]

        page_menu = uReq(iframe.attrs['src']).read()
        uReq(iframe.attrs['src']).close()

        page_soup_menu = soup(page_menu, "html.parser")

        menus = page_soup_menu.findChildren("div", {"data-hook": "wixrest-menus-section-wrapper"})[0:3]
        for menu in menus:
            content = menu.div.findChildren("div", recursive=False)[-1]
            items = content.findChildren("div", recursive=False)

            for item in items:
                category_name = item.findChildren("div", {"data-hook": "wixrest-menus-sub-category-title"})[0].text
                category, _ = Category.objects.get_or_create(name=category_name)
                for dish in item.findChildren("div", {"data-hook": "wixrest-menus-item"}):
                    dish_name = dish.find("span", {"data-hook": "wixrest-menus-item-title"}).text
                    dish_price = int(dish.find("div", {"data-hook": "wixrest-menus-item-price"}).text.replace('₴', ''))
                    if dish.find("div", {"data-hook": "wixrest-menus-item-description"}):
                        dish_description = dish.find("div", {"data-hook": "wixrest-menus-item-description"}).text
                        Dish.objects.update_or_create(name=dish_name, defaults={"category": category,
                                                                                "name": dish_name,
                                                                                "description": dish_description,
                                                                                "price": dish_price})
                    else:
                        Dish.objects.update_or_create(name=dish_name, defaults={"category": category,
                                                                                "name": dish_name,
                                                                                "price": dish_price})


