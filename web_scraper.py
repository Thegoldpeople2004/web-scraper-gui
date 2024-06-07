import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import csv

def scrape_website():
    # 获取用户输入的URL
    url = url_entry.get()
    
    # 发送HTTP GET请求
    response = requests.get(url)
    
    if response.status_code == 200:
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找所有商品的容器，假设每个商品在一个<article class='product_pod'>标签中
        products = soup.find_all('article', class_='product_pod')
        
        # 创建并打开CSV文件
        with open('books.csv', 'w', newline='', encoding='utf-8') as csvfile:
            # 定义CSV文件的列名
            fieldnames = ['Title', 'Price', 'Link']
            
            # 创建CSV写入器
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # 写入列名
            writer.writeheader()
            
            # 遍历所有商品并写入CSV文件
            for product in products:
                title = product.find('h3').find('a')['title'].strip()
                price = product.find('p', class_='price_color').text.strip()
                link = url + product.find('a')['href']
                
                # 写入商品信息到CSV文件
                writer.writerow({'Title': title, 'Price': price, 'Link': link})
        
        messagebox.showinfo("成功", "数据已成功保存到books.csv文件中!")
    else:
        messagebox.showerror("错误", f"请求失败，状态码: {response.status_code}")

# 创建主窗口
root = tk.Tk()
root.title("商品信息爬取器")

# 创建并放置标签和输入框
tk.Label(root, text="请输入商品页面的URL:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# 创建并放置按钮
scrape_button = tk.Button(root, text="开始爬取", command=scrape_website)
scrape_button.pack(pady=20)

# 运行主循环
root.mainloop()