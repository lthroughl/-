# coding=gbk
import requests  # ������Ŀ�
from bs4 import BeautifulSoup  # ����HTML�Ŀ�
import json
import time
from selenium import webdriver  # ����������Ŀ�
from selenium.webdriver.chrome.options import Options
import io
import sys

# ȫ�ֱ�������
overall_url = "https://so.csdn.net/so/search/all?q=%language%&t=all&p=%page%&s=hot&tm=0&lv=-1&ft=0&l=&u="
language_list = ["php", "basic", "ruby"]


# ͳ�Ʊ�������
# ..to be finished..


# ����csdn��ҳ���Ƕ�̬ҳ�棬����js�ű��޷�ֱ��ץȡ���������selenium web���������ץȡ
def get_dynamic_url(url):
    # ָ�����ض�̬ҳ���������ں˵�ַ[[�ô�����Ҫ�ڰ�װ��87.0.4280.141�汾Chrome�Ļ���������
    # ע�����Խ׶���ʹ�þ���·�����ύǰ��Ϊ���·��
    option = webdriver.ChromeOptions()
    # ���ش���
    option.add_argument('headless')
    # ��ֹ��ӡһЩ���õ���־
    option.add_experimental_option(
        "excludeSwitches", ['enable-automation', 'enable-logging'])
    chrome_driver = 'chromedriver.exe'
    driver = webdriver.Chrome(
        executable_path=chrome_driver, chrome_options=option)
    # driver.implicitly_wait(50)
    driver.get(url)  # ����ҳ�棬���һ�����������
    time.sleep(1)  # ����ֵȴ�ʱ���Ƿ�ֹҳ��δ������ɵ������ݶ�ʧ���������޸�   ��ʵ�ʾ�������������������������
    html_text = driver.page_source
    driver.quit()
    return BeautifulSoup(html_text)

# �Եõ���html�ĵ��������ݴ���   languageΪ������ţ�pageΪҳ��


def html_text_analyze(text, language, page, f, f_t):
    # ���������Ľ��(ֻ�ڵ�һҳͳ�Ƹ�����)
    if page == 1:
        ftr_result = text.find("div", "ftr-result").text
        print(ftr_result)

    # �����б�
    list_item = text.find_all(
        "div", {"data-v-08755ee8": "", "class": "list-item"})
    print("��"+str(page)+"ҳͳ�ƽ��: ��"+str(len(list_item))+"��")

    # ÿƪ����
    for i in range(len(list_item)):
        nrb_time = list_item[i].find(
            "span", {"data-v-08755ee8": "", "class": "nrb-time"}).text  # ʱ��
        nrb_type = list_item[i].find(
            "span", {"data-v-08755ee8": "", "class": "nrb-type"}).text  # ����
        nrb_user = list_item[i].find(
            "span", {"data-v-08755ee8": "", "class": "nrb-user"}).text  # ����

        nrb_view = ""
        if len(list_item[i].find_all("span", {"data-v-08755ee8": "", "class": "nrb-view"})) > 0:
            nrb_view = list_item[i].find(
                "span", {"data-v-08755ee8": "", "class": "nrb-view"}).text  # �����
        else:
            nrb_view = "0"
        if nrb_view[-3] == "��":
            nrb_view = nrb_view[1:-3]
            nrb_view = int(float(nrb_view)*10000)
        else:
            nrb_view = int(nrb_view[1:-1])

        nt_title = list_item[i].find(
            "h3", {"data-v-08755ee8": "", "class": "nt-title"}).text  # ����

        nrb_comment = ""
        if len(list_item[i].find_all("span", {"data-v-08755ee8": "", "class": "nrb-comment"})) > 0:
            nrb_comment = list_item[i].find(
                "span", {"data-v-08755ee8": "", "class": "nrb-comment"}).text  # �ظ���
            nrb_comment = int(nrb_comment[1:-1])
        else:
            nrb_comment = 0

        nrb_dig = ""
        if len(list_item[i].find_all("span", {"data-v-08755ee8": "", "class": "nrb-dig"})) > 0:
            nrb_dig = list_item[i].find(
                "span", {"data-v-08755ee8": "", "class": "nrb-dig"}).text  # ����
            # print("@"+nrb_dig+"@")
            nrb_dig = int(nrb_dig[1:-1])
        else:
            nrb_dig = 0

        nrb_tags_ = list_item[i].find(
            "span", {"data-v-08755ee8": "", "class": "nrb-tags"})
        nrb_tags_list = nrb_tags_.find_all("span", {"data-v-08755ee8": ""})
        nrb_tags_num = int(len(nrb_tags_list)/2)  # ��ǩ����
        nrb_tags = []  # ��ǩ�б�
        for j in range(nrb_tags_num):
            nrb_tags.append(nrb_tags_list[j*2].text)

        x = str(nrb_time)+" "+str(nrb_type)+" "+str(nrb_user)+" " + str(nrb_view) + \
            "��� "+str(nrb_comment)+"�ظ� "+str(nrb_dig) + \
            "�� "+"��"+str(nt_title)+"�� "
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
              str(nrb_view)+"���  "+str(nrb_comment)+"�ظ�  "+str(nrb_dig)+"��  "+"��"+str(nt_title)+"��", end="")
        for j in range(nrb_tags_num):
            print("��"+str(nrb_tags[j])+"��", end="")
        print("")'''

# ������


def main():
    # �ı��׼�����Ĭ�ϱ���
    for i in range(len(language_list)):  # ��ѭ��ͳ��ÿ������
        print(language_list[i]+"��ͳ�����: ")
        url_ = overall_url.replace("%language%", language_list[i])
        if(language_list[i][-2:] == "����"):
            language_list[i] = language_list[i][0:-2]
        f = open(language_list[i]+".txt", "w+", encoding="utf-8")
        f_t = open(language_list[i]+"_title.txt", "w+", encoding="utf-8")
        for j in range(1, 21):  # Сѭ��ͳ�Ƹ����Ե�ҳ���1��10 �����Զ�
            url = url_.replace("%page%", str(j))
            html_text_analyze(get_dynamic_url(url), i, j, f, f_t)
    print("�������")


if __name__ == '__main__':
    main()
