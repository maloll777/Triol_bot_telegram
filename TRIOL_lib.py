import requests
import sqlite3


def get_page_product(id_item):
    # поиск товара по id на сайте amma.pet
    # возвращает адрес старницы с товаром

    page = requests.post('https://amma.pet/search/?q=' + id_item)

    if 'По вашему запросу ничего не найдено' in page.text:
        return -1

    for page_line in page.text.replace('>', '>\n').split():

        if 'href="/product' in page_line:
            return 'https://amma.pet' + page_line[6:-1]


def get_info_item(product_page_link):
    # сбор информации о товаре со траницы

    if product_page_link == -1:
        return []
    elif product_page_link is None:
        return []

    page = requests.post(product_page_link)
    text = page.text.replace('<', '\n<')
    text = text.replace('>', '>\n').splitlines()
    # чистим страницу от мусора
    text = [i for i in text if i != '']
    text = [i for i in text if '</' not in i]
    text = [i for i in text if len(i) > 4]

    for index, cont in enumerate(text):
        if 'Главная' in cont:
            text = text[index:]

    for index, cont in enumerate(text):
        if '<div class="product-controls__item">' in cont:
            text = text[:index]
    image = [i[14:-2] for i in text if 'jpg' in i]
    text = [i for i in text if '<' not in i]

    if len(text) < 3:
        return []

    del text[0]
    try:
        del text[3]
    except IndexError:
        return []
    del text[-3:]

    out = {'name': text[3].replace('&quot;', ''), 'description': text[4], 'category': text[2], 'pets_type': text[0],
           'material': text[-1], 'brand_name': text[-8], 'composition': text[-1], 'item_number': text[-10],
           'item_size': text[-6], 'country': text[-4], 'image': image}

    return out


def get_image_product(product_page_link):
    # Поиск картинки товара на сайте amma.pet
    # возвращает ссылку на первую картинку

    if product_page_link == -1:
        return None
    elif product_page_link is None:
        return None

    page = requests.post(product_page_link)
    text_page = page.text.replace('<', '\n<')
    text_page = text_page.replace('>', '>\n').splitlines()
    # чистим страницу от мусора
    text_page = [i for i in text_page if i != '']
    text_page = [i for i in text_page if '</' not in i]
    text_page = [i for i in text_page if len(i) > 4]

    for i, line in enumerate(text_page):

        if line.find('img alt src') > 0 \
                and \
                line.find('_q') < 0:
            return 'https://amma.pet/' + text_page[i][14:-2]


def get_item_info(id_item):
    # возвращает строку и наименованием и описанием товара
    # Ищет информацию в БД

    con = sqlite3.connect('./TRIOL.db')
    cursor = con.cursor()
    cursor.execute('select name, description FROM Product where item_number = ' + id_item)
    try:
        out = cursor.fetchall()[0]
    except IndexError:
        return 'Описание товара не найдено'

    return out[0] + '\n\n' + out[1]
