import requests
from bs4 import BeautifulSoup
import os

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203',
          'Cookie':'_gid=GA1.2.1703358248.1692260776; FCNEC=%5B%5B%22AKsRol_hZvx3Xu7iugm4wZ9zfP9CUk_1P97QgEqQagcA1PqG2Wejexl3m_mx7cnSWXiUHPaadD6kcRGYsf91VxPvRMejjMypfjsslzZNWT9dQ6CaSXRLNc1_65N4-lyN3q45MIr9aPNqGklLSJmixpqQocJQKEdHOg%3D%3D%22%5D%2Cnull%2C%5B%5D%5D; __gads=ID=590231382231eaf6-22c49f57eae2002e:T=1692260777:RT=1692349235:S=ALNI_MY-AiS7AkdDujyfYurC6UJSEUPbFg; __gpi=UID=00000c2de9549530:T=1692260777:RT=1692349235:S=ALNI_Ma_WxSDSbFpMDDVPZJSGp8m3bOt5Q; _ga_4QEWBNE9J8=GS1.1.1692347828.4.1.1692349236.0.0.0; _ga=GA1.1.117591981.1692260775'  }

main_url='https://www.51shucheng.net/kehuan/jidi'

def open_page(url):
   html=requests.get(url,headers=headers)
   html.encoding='utf-8'
   html=html.text
   return html

def get_content(html, selector, class_):
   soup=BeautifulSoup(html,features='lxml')
   content=soup.find_all(selector,class_=class_)
   return content

def write_content(name,chapter_name, content):
   path=os.path.join(f"./{name}")
   if os.path.exists(path):
       file = os.path.join(path, f"{chapter_name + '.txt'}")
       with open(file, 'w', encoding='utf-8') as f:
           f.write(content)
   else:
       os.mkdir(path)
       file = os.path.join(path, f"{chapter_name + '.txt'}")
       with open(file, 'w', encoding='utf-8') as f:
           f.write(content)

if __name__ == '__main__':
    main_html=open_page(main_url)
    fictions = get_content(main_html, "div", "mulu-list")
    fiction_names = get_content(main_html, 'div', 'mulu-title')
    fiction_urls = []

    urls = fictions[0].find_all("a")
    name = fiction_names[0].text

    for j in range(len(urls)):
        url, title = urls[j]['href'], urls[j].text
        fiction_urls.append([name, title, url])
        name = fiction_urls[j][0]
        title = fiction_urls[j][1]  # 章节名称
        print(f"{'*' * 5}开始小说《{name}》的  {title}  爬取{'*' * 5}")
        html = open_page(fiction_urls[j][2])
        content =get_content(html, 'div', "neirong")[0].text
        write_content(name, title, content)