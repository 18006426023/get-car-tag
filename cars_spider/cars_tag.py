import requests
from lxml import etree
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}


def parse_page(url):
    res = requests.get(url, headers=HEADERS)
    text = res.text
    html = etree.HTML(text)
    chemings = html.xpath("//dt//div//a/text()")
    pics = html.xpath("//dt//a//img//@src")
    cars = []
    for cheming, pic in zip(chemings, pics):
        data = {}
        data['车名'] = cheming
        data['图标'] = pic
        cars.append(data)
    return cars


if __name__ == '__main__':
    urls = 'https://www.autohome.com.cn/grade/carhtml/{}.html'
    a = []
    for i in range(65, 91):
        a.append(chr(i))
    a.remove('U')
    cur_dir = 'E://GitSpace/cars_spider/pics/'
    for j in a:
        folder_name = j
        if os.path.isdir(cur_dir):
            os.mkdir(os.path.join(cur_dir, folder_name))
    for i in a:
        url = urls.format(i)
        cars = parse_page(url)
        print(cars)
        path = 'E://GitSpace/cars_spider/pics/' + i + '/'
        for car in cars:
            car_url = 'https:' + car['图标']
            with open(path + car['车名'] + '.png', 'wb') as f:
                pic = requests.get(car_url, headers=HEADERS)
                f.write(pic.content)
                f.close()
