from AllInOne import item_grabber

from bs4 import BeautifulSoup

test_cases = [
    ("empty element", "<div class='card'></div>"),
    ("missing price", "<div class='card'><a href='/x' title='Laptop'></a></div>"),
    ("non-numeric price", "<div class='card'><a href='/x' title='Laptop'></a><p itemprop='price'>abcde</p></div>"),
    ("unicode mess", "<div class='card'><a href='/x' title='Ноутбук™ \xa0\u200b'></a><p itemprop='price'>$10</p></div>"),
]
failed=[]
category="electronic"

for case in test_cases:
    soup=BeautifulSoup(case[1],'lxml')
    tf,schema=item_grabber(soup,category,failed)
    print(tf)
    print(schema)