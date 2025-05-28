# encoding:utf-8
# @Function:
from setup import PageSama


# todo add normal recursive code 

def turn_with_iteration():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    item_path_dict = {'data.topic_card_list.items': ['dynamic_card_item.modules.module_author.name']}
    params = {
        'offset': '',
        'topic_id': '1308237',
        'sort_by': '0',
        'page_size': '20',
        'source': 'Web',
        'features': 'itemOpusStyle,listOnlyfans,opusBigCover,onlyfansVote,decorationCard',
    }

    url = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/topic'
    break_path_str = 'data.topic_card_list.offset'
    res = PageSama(url=url, get_params=params, break_path=break_path_str, headers=headers,
                   item_path_dict=item_path_dict).mix_or_pick()
    print(res)


if __name__ == "__main__":
    turn_with_iteration()
