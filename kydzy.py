# coding=gbk
import requests  # 发请求的库
from bs4 import BeautifulSoup  # 解析HTML的库
import json
import time
from selenium import webdriver  # 加载浏览器的库
from selenium.webdriver.chrome.options import Options
import io
import sys

# 全局变量定义
overall_url = "https://so.csdn.net/so/search/all?q=%language%&t=all&p=%page%&s=hot&tm=0&lv=-1&ft=0&l=&u="
language_list = ["php", "basic", "ruby"]


# 统计变量定义
# ..to be finished..


# 由于csdn的页面是动态页面，包含js脚本无法直接抓取，因而采用selenium web框架来进行抓取
def get_dynamic_url(url):
    # 指定加载动态页面的浏览器内核地址[[该代码需要在安装有87.0.4280.141版本Chrome的环境下运行
    # 注：测试阶段先使用绝对路径，提交前改为相对路径
    option = webdriver.ChromeOptions()
    # 隐藏窗口
    option.add_argument('headless')
    # 防止打印一些无用的日志
    option.add_experimental_option(
        "excludeSwitches", ['enable-automation', 'enable-logging'])
    chrome_driver = 'chromedriver.exe'
    driver = webdriver.Chrome(
        executable_path=chrome_driver, chrome_options=option)
    # driver.implicitly_wait(50)
    driver.get(url)  # 请求页面，会打开一个浏览器窗口
    time.sleep(1)  # 加这局等待时间是防止页面未加载完成导致数据丢失，可酌情修改   【实际经常出现来不及加载完的情况】
    html_text = driver.page_source
    driver.quit()
    return BeautifulSoup(html_text)

# 对得到的html文档进行数据处理   language为语言序号，page为页码


def html_text_analyze(text, language, page, f, f_t):
    # 总搜索到的结果(只在第一页统计该数据)
    if page == 1:
        ftr_result = text.find("div", "ftr-result").text
        print(ftr_result)

    # 文章列表
    list_item = text.find_all(
        "div", {"data-v-08755ee8": "", "class": "list-item"})
    print("第"+str(page)+"页统计结果: 共"+str(len(list_item))+"个")

    # 每篇文章
    for i in range(len(list_item)):
        nrb_time = list_item[i].find(
            "span", {"data-v-08755ee8": "", "class": "nrb-time"}).text  # 时间
        nrb_type = list_item[i].find(
            "span", {"data-v-08755ee8": "", "class": "nrb-type"}).text  # 类型
        nrb_user = list_item[i].find(
            "span", {"data-v-08755ee8": "", "class": "nrb-user"}).text  # 作者

        nrb_view = ""
        if len(list_item[i].find_all("span", {"data-v-08755ee8": "", "class": "nrb-view"})) > 0:
            nrb_view = list_item[i].find(
                "span", {"data-v-08755ee8": "", "class": "nrb-view"}).text  # 浏览量
        else:
            nrb_view = "0"
        if nrb_view[-3] == "万":
            nrb_view = nrb_view[1:-3]
            nrb_view = int(float(nrb_view)*10000)
        else:
            nrb_view = int(nrb_view[1:-1])

        nt_title = list_item[i].find(
            "h3", {"data-v-08755ee8": "", "class": "nt-title"}).text  # 标题

        nrb_comment = ""
        if len(list_item[i].find_all("span", {"data-v-08755ee8": "", "class": "nrb-comment"})) > 0:
            nrb_comment = list_item[i].find(
                "span", {"data-v-08755ee8": "", "class": "nrb-comment"}).text  # 回复量
            nrb_comment = int(nrb_comment[1:-1])
        else:
            nrb_comment = 0

        nrb_dig = ""
        if len(list_item[i].find_all("span", {"data-v-08755ee8": "", "class": "nrb-dig"})) > 0:
            nrb_dig = list_item[i].find(
                "span", {"data-v-08755ee8": "", "class": "nrb-dig"}).text  # 点赞
            # print("@"+nrb_dig+"@")
            nrb_dig = int(nrb_dig[1:-1])
        else:
            nrb_dig = 0

        nrb_tags_ = list_item[i].find(
            "span", {"data-v-08755ee8": "", "class": "nrb-tags"})
        nrb_tags_list = nrb_tags_.find_all("span", {"data-v-08755ee8": ""})
        nrb_tags_num = int(len(nrb_tags_list)/2)  # 标签数量
        nrb_tags = []  # 标签列表
        for j in range(nrb_tags_num):
            nrb_tags.append(nrb_tags_list[j*2].text)

        x = str(nrb_time)+" "+str(nrb_type)+" "+str(nrb_user)+" " + str(nrb_view) + \
            "浏览 "+str(nrb_comment)+"回复 "+str(nrb_dig) + \
            "赞 "+"《"+str(nt_title)+"》 "
        temp = [str(nrb_time), str(nrb_type), str(
            nrb_user), nrb_view, nrb_comment, nrb_dig, str(nt_title)]
        for j in range(nrb_tags_num):
            temp.append(str(nrb_tags[j]))
        f.write(str(temp))
        f.write("\n")
        y = str(nt_title)
        y += "\n"
        f_t.write(y)
        '''
        print("["+str(i+1)+"] "+str(nrb_time)+"  "+str(nrb_type)+"  "+str(nrb_user)+"  " +
              str(nrb_view)+"浏览  "+str(nrb_comment)+"回复  "+str(nrb_dig)+"赞  "+"《"+str(nt_title)+"》", end="")
        for j in range(nrb_tags_num):
            print("【"+str(nrb_tags[j])+"】", end="")
        print("")'''

# 主进程


def main():
    # 改变标准输出的默认编码
    for i in range(len(language_list)):  # 大循环统计每种语言
        print(language_list[i]+"的统计情况: ")
        url_ = overall_url.replace("%language%", language_list[i])
        if(language_list[i][-2:] == "语言"):
            language_list[i] = language_list[i][0:-2]
        f = open(language_list[i]+".txt", "w+", encoding="utf-8")
        f_t = open(language_list[i]+"_title.txt", "w+", encoding="utf-8")
        for j in range(1, 21):  # 小循环统计该语言的页码从1到10 可以自定
            url = url_.replace("%page%", str(j))
            html_text_analyze(get_dynamic_url(url), i, j, f, f_t)
    print("程序结束")


if __name__ == '__main__':
    main()
