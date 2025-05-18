import json

import pydash
# todo  用自己封装的方法
from loguru import logger
import requests
from dataclasses import dataclass, field


@dataclass
class PageSama:
    url: str = ""  # 默认为空字符串
    get_params: dict = field(default_factory=dict)  # 默认为空字典
    post_data: dict = field(default_factory=dict)  # 默认为空字典
    headers: dict = field(default_factory=dict)  # 默认为空字典
    cookies: dict = field(default_factory=dict)  # 默认为空字典
    proxy: dict = field(default_factory=dict)  # 默认为空字典
    max_page: int = 1  # 默认为 1

    def __post_init__(self):
        self.page_axios = list((self.post_data or self.get_params).keys())[0]
        self.is_get_method = True if self.get_params else False

    def run(self):
        pass

    @logger.catch
    def fetch_one_page(self, page_num):
        # todo
        if self.is_get_method:
            res = requests.get(self.url, params=self.get_params, headers=self.headers, cookies=self.cookies,
                               proxies=self.proxy)
        else:
            req_data = json.dumps(self.post_data)
            res = requests.post(self.url, data=req_data, headers=self.headers, cookies=self.cookies, proxies=self.proxy)

        return res.json()

    def peel(self, res_json: dict, item_path: str):
        parsed_items = pydash.get(res_json, item_path) or []
        return parsed_items


if __name__ == '__main__':
    # todo  1.无差别翻页
    # 2. 找一个测试的网站，manga porn
    PageSama()
