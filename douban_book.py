import requests
import parsel
import time
import csv

bookid = open('Book_id.txt')
f = open('book.csv', mode = 'a', encoding = 'UTF-8', newline = '')
csv_writer = csv.DictWriter(f, fieldnames = [
    '书名',
    '作者',
    '出版社',
    '出版年',
    '页数',
    '定价',
    'ISBN',
    '内容简介',
    '作者简介'
])
csv_writer.writeheader()

idlist = []
for i in range(1000):
    idlist.append(bookid.readline())

for i in range(905, 1000):
    time.sleep(0.5)
    id = idlist[i]
    print(i, ':', idlist[i])
    url = 'https://book.douban.com/subject/' + id
    headers = { 
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    response = requests.get(url = url, headers = headers)

    #print(response.text)

    selector = parsel.Selector(response.text)
    title = selector.css('h1 span::text').get()
    flag = 0
    while title == None:
        if (response.text.find('条目不存在') != -1 or response.text.find('页面不存在') != -1):
            print('不存在')
            flag = 10

        print(title)
        print('error')
        flag += 1
        if flag >= 10:
            break
        time.sleep(10)
        response = requests.get(url = url, headers = headers)
        selector = parsel.Selector(response.text)
        title = selector.css('h1 span::text').get()
    if flag >= 10:
        continue
    print(title)

    rating = selector.css('strong.ll.rating_num::text').get()
    rating = rating.replace(' ', '')
    print(rating)

    info = selector.css('div#info ::text').getall()

    author = ' '
    l = 0
    while (info[l].find('作者') == -1 and l < len(info) - 1):
        l += 1
    if info[l].find('作者') != -1:
        l += 2
        author = ''
        while (info[l].find('出版社') == -1 and info[l].find(':') == -1):
            author += info[l]
            author = author.replace('\n', '')
            author = author.replace(' ', '')
            l += 1
    print(author)


    l = info.index('出版社:') if ('出版社:' in info) else -1
    publish = ' '
    if l != -1:
        if info[l].find('出版社') != -1:
            l += 1
            publish = ''
            while (info[l].find(':') == -1 and info[l].find('译者') == -1 and info[l].find('出版年') == -1):
                publish += info[l]
                publish = publish.replace('\n', '')
                publish = publish.replace(' ', '')
                l += 1
    print(publish)


    year = ' '
    l = info.index('出版年:') if ('出版年:' in info) else -1
    if l != -1 :
        l = l + 1
        year = info[l]
        year = year.replace(' ', '')
    print(year)

    page = ' '
    l = info.index('页数:') if ('页数:' in info) else -1
    if l != -1 :
        l = l + 1
        page = info[l]
        page = page.replace(' ', '')
    print(page)

    price = ' '
    l = info.index('定价:') if ('定价:' in info) else -1
    if l != -1 :
        l = l + 1
        price = info[l]
        price = price.replace(' ', '')
    print(price)

    isbn = ' '
    l = info.index('ISBN:') if ('ISBN:' in info) else -1
    if l != -1 :
        l = l + 1
        isbn = info[l]
        isbn = isbn.replace(' ', '')
    print(isbn)


    sum = ''
    sums = selector.css('div#link-report.indent span.all.hidden div.intro p')
    if sums == []:
        sums = selector.css('div#link-report.indent div div.intro p')
    for s in sums:
        ss = s.css('::text').get()
        if (ss != None):
            ss = ss.replace('\n', '')
            ss = ss.replace('\r', '')
            ss = ss.replace('\u3000', '')
            ss = ss.replace(' ', '')
            #print(ss)
            sum += ss
    print(sum)


    ainfo = ' '
    infos = selector.css('div.related_info div.indent div div.intro')
    if len(infos) >= 2:
        ainfo = ''
        ainfos = infos[1].css('p')
        for ai in ainfos:
            ai = ai.css('::text').get()
            if (ai != None):
                ai = ai.replace('\n', '')
                ai = ai.replace('\r', '')
                ai = ai.replace('\u3000', '')
                ai = ai.replace(' ', '')
                ainfo += ai
    else:
        ainfos = selector.css('div.related_info div.indent span.all.hidden .intro ::text').getall()
        if ainfos != []:
            ainfo = ''
            for ai in ainfos:
                ai = ai.replace('\n', '')
                ai = ai.replace('\r', '')
                ai = ai.replace('\u3000', '')
                ai = ai.replace(' ', '')
                ainfo += ai
    print(ainfo)


    #print(info)


    dit = {
        '书名': title,
        '作者': author,
        '出版社': publish,
        '出版年': year,
        '页数': page,
        '定价': price,
        'ISBN': isbn,
        '内容简介': sum,
        '作者简介': ainfo
    }
    csv_writer.writerow(dit)

bookid.close()
f.close()












