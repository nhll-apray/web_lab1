import requests
import parsel
import time
import csv

movieid = open('Movie_id.txt')
f = open('movie.csv', mode = 'a', encoding = 'UTF-8', newline = '')
csv_writer = csv.DictWriter(f, fieldnames = [
    '标题',
    '年份',
    '评分',
    '导演',
    '编剧',
    '主演',
    '类型',
    '制片国家/地区',
    '语言',
    '上映日期',
    '片长',
    '剧情简介'
])
#csv_writer.writeheader()

idlist = []
for i in range(1000):
    idlist.append(movieid.readline())

for i in range(174, 1000):
    time.sleep(1)
    print(i, ':')
    id = idlist[i]
    url = 'https://movie.douban.com/subject/' + id
    headers = { 
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    response = requests.get(url = url, headers = headers)

    #print(response.text)

    selector = parsel.Selector(response.text)
    error = selector.css('li[style]:nth-child(1)::text').get()
    if error != None:
        print('error')
        continue
    title = selector.css('h1 span::text').get()
    while title == None:
        print(title)
        time.sleep(10)
        response = requests.get(url = url, headers = headers)
        selector = parsel.Selector(response.text)
        title = selector.css('h1 span::text').get()
    print(title)
    year = selector.css('h1 span.year::text').get()
    print(year)
    rating = selector.css('strong.ll.rating_num::text').get()
    print(rating)

    attrs = selector.css('#info span.attrs')
    
    attr1 = attrs[0].css('a::text').get()
    print(attr1)


    if len(attrs) == 3:
        attr2 = ''
        attr2s = attrs[1].css('a')
        for attr in attr2s:
            attr2 += attr.css('::text').get()
            attr2 += ' '
        print(attr2)

        attr3 = ''
        attr3s = attrs[2].css('a')
        for attr in attr3s:
            attr3 += attr.css('::text').get()
            attr3 += ' '
        print(attr3)
    elif len(attrs) == 2:
        attr2 = ' '
        print(attr2)

        attr3 = ''
        attr3s = attrs[1].css('a')
        for attr in attr3s:
            attr3 += attr.css('::text').get()
            attr3 += ' '
        print(attr3)
    elif len(attrs) == 1:
        attr2 = ' '
        print(attr2)

        attr3 = ' '
        print(attr3)


    info = selector.css('div#info ::text').getall()
    #print(info)


    l = info.index('类型:')
    l += 1
    type = ''
    while info[l].find('\n') == -1:
        type += info[l]
        l += 1
    type = type.replace(' ', '')
    print(type)

    l = info.index('制片国家/地区:')
    country = info[l + 1]
    country = country.replace(' ', '')
    print(country)

    l = info.index('语言:') if ('语言:' in info) else -1
    lang = ' '
    if l != -1:
        lang = info[l + 1]
        lang = lang.replace(' ', '')
    print(lang)

    l = info.index('上映日期:') if ('上映日期:' in info) else -1
    if l == -1:
        l = info.index('首播:') if ('首播:' in info) else -1
    date = ' '
    if l != -1 :
        l = l + 1
        date = ''
        while info[l].find('\n') == -1:
            date += info[l]
            l += 1
        date = date.replace(' ', '')
    print(date)

    l = info.index('片长:') if ('片长:' in info) else -1
    if l == -1:
        l = info.index('单集片长:') if ('单集片长:' in info) else -1
    length = ' '
    if l != -1:
        l = l + 1
        length = ''
        while info[l].find('\n') == -1:
            length += info[l]
            l += 1
        length = length.replace(' ', '')
    print(length)

    sum = ''
    sums = selector.css('.all.hidden::text').getall()
    if sums == []:
        sums = selector.css('span[property="v:summary"]::text').getall()
    for s in sums:
        s = s.replace('\n', '')
        s = s.replace('\r', '')
        s = s.replace('\u3000', '')
        s = s.replace(' ', '')
        sum += s
    print(sum)

    dit = {
        '标题': title,
        '年份': year,
        '评分': rating,
        '导演': attr1,
        '编剧': attr2,
        '主演': attr3,
        '类型': type,
        '制片国家/地区': country,
        '语言': lang,
        '上映日期': date,
        '片长': length,
        '剧情简介': sum
    }
    csv_writer.writerow(dit)

movieid.close()
f.close()












