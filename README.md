以上是一个具体例子的网页信息爬取例子，
但对于每一个不同的网站，都需要进行一定的定制化开发，
分析该网站的HTML源码，找出其中存储有用信息的HTML元素的结构，然后根据这个结构调整爬虫程序代码。
这是因为不同网站间HTML结构的差异性，使得爬虫代码并不能一概而论，通用于所有网站。
以下是一个通用的爬取框架：
import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox

def scrape_website(url, selectors):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 用户定义的选择器
        product_selector = selectors['product']
        title_selector = selectors['title']
        price_selector = selectors['price']
        link_selector = selectors['link']
        
        products = soup.select(product_selector)
        
        with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['标题', '价格', '链接']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for product in products:
                title = product.select_one(title_selector).text.strip()
                price = product.select_one(price_selector).text.strip()
                link = url + product.select_one(link_selector)['href']
                
                writer.writerow({'标题': title, '价格': price, '链接': link})
                
        messagebox.showinfo("成功", "数据已成功保存到products.csv文件中！")
    except Exception as e:
        messagebox.showerror("错误", f"请求失败，错误信息： {str(e)}")

def start_scraping():
    url = url_entry.get()
    # 假设用户会自己输入或选择预设的规则
    selectors = {
        'product': product_selector_entry.get(),
        'title': title_selector_entry.get(),
        'price': price_selector_entry.get(),
        'link': link_selector_entry.get(),
    }
    scrape_website(url, selectors)

root = tk.Tk()
root.title("通用信息爬取器")

tk.Label(root, text="请输入网页URL：").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

tk.Label(root, text="商品选择器：").pack(pady=10)
product_selector_entry = tk.Entry(root, width=50)
product_selector_entry.pack(pady=5)

tk.Label(root, text="标题选择器：").pack(pady=10)
title_selector_entry = tk.Entry(root, width=50)
title_selector_entry.pack(pady=5)

tk.Label(root, text="价格选择器：").pack(pady=10)
price_selector_entry = tk.Entry(root, width=50)
price_selector_entry.pack(pady=5)

tk.Label(root, text="链接选择器：").pack(pady=10)
link_selector_entry = tk.Entry(root, width=50)
link_selector_entry.pack(pady=5)

scrape_button = tk.Button(root, text="开始爬取", command=start_scraping)
scrape_button.pack(pady=20)

root.mainloop()

通过提供输入框让用户自定义选择器，使得对于没有硬编码在脚本中的网站也能尝试去爬取信息。
用户需要根据目标网站的具体HTML结构，输入合适的CSS选择器。
因此，用户需要具备一定的HTML/CSS知识，能够从浏览器的开发者工具中查找元素并编写CSS选择器。
这样的设计虽然提供了更大的灵活性，但是也增加了使用门槛。
对于不同的网站，用户需要根据具体情况调整selectors中的配置。
