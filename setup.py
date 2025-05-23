import json
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
import pydash
from loguru import logger
import requests
from dataclasses import dataclass, field

from log_to_mongo_col import MongoLog


@dataclass
class PageSama:
    url: str = ""  # 默认为空字符串
    get_params: dict = field(default_factory=dict)
    post_data: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    cookies: dict = field(default_factory=dict)
    proxy: dict = field(default_factory=dict)
    offset: int = 1
    max_page: int = 100  # todo update later
    item_path_dict: dict = field(default_factory=dict)
    multi_thread: bool = True
    is_remote_log: bool = False
    item_path_key: str = ''
    detail_path_list: list = field(default_factory=list)
    break_path: str = ''

    def __post_init__(self):
        self.page_axios = list((self.post_data or self.get_params).keys())[0]
        self.start_offset = int((self.post_data or self.get_params).get(self.page_axios))
        self.is_get_method = True if self.get_params else False

        if self.is_remote_log:
            logger = MongoLog()()

        if self.item_path_dict:
            self.item_path_key = next(iter(self.item_path_dict.keys()))
            self.detail_path_list = self.item_path_dict.get(self.item_path_key)

    def mix_or_pick(self):
        if self.break_path:
            for one_res in self.fetch_one_page():
                if break_point := pydash.get(one_res, self.break_path):
                    # continue iteration
                    # todo 
                    pass
                else:
                    break
        else:
            page_index_list = [self.start_offset + i * self.offset for i in range(self.max_page)]
            if self.multi_thread:
                with ThreadPoolExecutor() as executor:
                    tmp = executor.map(lambda pdex: self.peel(self.fetch_one_page(pdex)), page_index_list)

            else:
                tmp = [self.peel(self.fetch_one_page(pdex)) for pdex in page_index_list]
            if self.item_path_key:
                page_res = list(chain.from_iterable(tmp))
                return [
                    [pydash.get(one, path_) for one in page_res]
                    for path_ in self.detail_path_list
                ]
            else:
                return tmp

    @logger.catch
    def fetch_one_page(self, page_num):
        # todo ? maybe rewrite
        if self.is_get_method:
            current_params = self.get_params.copy()
            # 更改页数
            current_params[self.page_axios] = page_num

            # remake params
            if self.upd_params():
                current_params.update(self.upd_params())

            # remake headers
            if self.upd_hd():
                self.headers.update(self.upd_hd())

            res = requests.get(
                self.url,
                params=current_params,
                headers=self.headers,
                cookies=self.cookies,
                proxies=self.proxy,
            )
        else:
            current_params = self.get_params.copy()
            # 更改页数
            current_params[self.page_axios] = page_num

            # remake params
            if self.upd_params():
                current_params.update(self.upd_params())
            # remake headers
            if self.upd_hd():
                self.headers.update(self.upd_hd())

            res = requests.post(
                self.url,
                data=json.dumps(current_params),
                headers=self.headers,
                cookies=self.cookies,
                proxies=self.proxy,
            )
        return res.json()

    def peel(self, res_json: dict):
        if self.item_path_key:
            return pydash.get(res_json, self.item_path_key) or []
        else:
            return res_json

    def upd_hd(self):
        ...

    def upd_params(self):
        ...


def all_normal_pages():
    url = "https://spa1.scrape.center/api/movie/"
    params = {
        "offset": "10",
        "limit": "10",
    }

    parse_path_dict = {"results": ['name', 'alias']}
    instance_a = PageSama(url=url, get_params=params, offset=20, max_page=3, item_path_dict=parse_path_dict)
    # instance_a = PageSama(url=url, get_params=params, offset=20, max_page=3, )
    print(list(instance_a.mix_or_pick()))


def turn_with_iteration():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    item_path_dict = ''  # todo
    params = {
        # 'offset': 'heat_2913317_18_20', # todo
        'offset': '',
        'topic_id': '1308237',
        'sort_by': '0',
        'page_size': '20',
        'source': 'Web',
        'features': 'itemOpusStyle,listOnlyfans,opusBigCover,onlyfansVote,decorationCard',
    }

    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/topic'
    path_str = 'data.topic_card_list.offset'
    instance_a = PageSama(url=url, get_params=params, break_path=path_str)


if __name__ == "__main__":
    turn_with_iteration()
