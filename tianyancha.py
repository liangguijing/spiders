# -*- coding: utf-8 -*-
# @Time 2021/4/19 16:02 
# @Author: liangguijing
# @Remark: 批量获取天眼查公司信息，登录复制cookies到cookies.txt需要放在同文件夹下

from bs4 import BeautifulSoup
from random import random
from requests import Session


def get_text(elem):
    if elem.string:
        return elem.string
    else:
        return elem.next_element


class TianYanCha:
    def __init__(self):
        self._session = Session()
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                  "Chrome/90.0.4430.72 Safari/537.36"
        self._headers = {
            "user-agent": self.ua,
        }
        self._login_by_cookies()

    def _login_by_cookies(self):
        cookies_file = "cookies.txt"
        with open(cookies_file, "r", encoding="utf-8") as f:
            cookies = f.read().strip().strip(";")
            cookies = {ck.split("=")[0].strip(): ck.split("=")[1].strip() for ck in cookies.split(";")}
            self._session.cookies.update(cookies)

    def _get_com_html(self, com_id):
        url = f"https://www.tianyancha.com/company/{com_id}"
        resp = self._session.get(url, headers=self._headers)
        resp.encoding = "utf-8"
        return resp.text

    def get_com_info(self, com_id):
        html = self._get_com_html(com_id)
        soup = BeautifulSoup(html, "lxml")
        com_name = soup.find("h1", attrs={"class": "name"}).string.strip()
        container = soup.find(id="_container_baseInfo")
        tr = container.table.tbody.find_all("tr")
        table = [get_text(i) for row in tr for i in row]
        base_info = {"公司名称": com_name}
        for i in range(0, len(table), 2):
            base_info.update({table[i]: table[i + 1]})
        return base_info

    def get_com_id(self, q):
        """
        获取搜索到的第一个公司的id
        :param q:
        :return:
        """
        url = "https://sp0.tianyancha.com/search/suggestV2.json"
        params = {
            "key": q,
            "_": random() * 1000,
        }
        resp = self._session.get(url, params=params)
        com_id = resp.json()["data"][0]["id"]
        return com_id

    def search(self, com):
        com_id = self.get_com_id(com)
        com_info = self.get_com_info(com_id)
        return com_info


if __name__ == "__main__":
    tyc = TianYanCha()
    print(tyc.search("阿里"))
    print(tyc.search("新浪"))
