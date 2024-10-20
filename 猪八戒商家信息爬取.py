import requests
from lxml import etree
import time

# 使用 requests.Session() 来管理会话
session = requests.Session()

# 设置 headers
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
}


# 函数来解析并处理每一页的商家信息
def parse_page(page_num):
    url = f"https://www.zbj.com/fw/?p={page_num}&osStr=ad-0,np-0,rf-0,sr-112,mb-0,cr-11,ocpc-1,cpc-6,cro-10,lk-0"

    try:
        # 使用 session 进行请求
        resp = session.get(url, headers=headers)

        # 检查是否请求成功
        if resp.status_code != 200:
            print(f"Failed to retrieve page {page_num}")
            return False  # 请求失败，返回 False 以停止循环

        html = etree.HTML(resp.text)

        # 拿到每个服务商的div
        divs = html.xpath("//*[@id='__layout']/div/div[3]/div[1]/div[4]/div/div[2]/div[1]/div[2]/div")
        if not divs:
            print(f"No data found on page {page_num}. Stopping...")
            return False  # 如果找不到 div，说明没有更多数据了，返回 False 以停止循环

        # 遍历每个服务商的div
        for div in divs:
            price = div.xpath("./div/div[3]/div[1]/span/text()")[0] if div.xpath(
                "./div/div[3]/div[1]/span/text()") else ""
            title = div.xpath("./div/div[3]/div[2]/a/span/text()")[0] if div.xpath(
                "./div/div[3]/div[2]/a/span/text()") else ""
            sales = div.xpath("./div/div[3]/div[3]/div[1]//text()")
            comments = div.xpath("./div/div[3]/div[3]/div[2]//text()")
            company = div.xpath("./div/div[5]//text()")

            # 将 sales 和 comments 列表合并为字符串
            sales_str = ' '.join(sales).strip() if sales else ""
            comments_str = ' '.join(comments).strip() if comments else ""
            company_str = ' '.join(company).strip() if company else ""

            # 拼接所有信息
            combined_info = f"Price: {price}, Title: {title}, Sales: {sales_str}, Comments: {comments_str}, Company: {company_str}"

            # 输出拼接后的结果
            print(combined_info)

        return True  # 继续爬取下一页

    except Exception as e:
        print(f"An error occurred: {e}")
        return False  # 如果发生异常，停止爬取


# 循环爬取多页
page_num = 1
while True:
    print(f"Scraping page {page_num}...")
    if not parse_page(page_num):
        break  # 如果当前页面没有数据或请求失败，停止循环
    page_num += 1
    time.sleep(1)  # 避免请求过于频繁，增加一个短暂的延时

# 爬取结束后关闭 session
session.close()
print("Session closed.")
