# encoding:utf-8
# @Function:
from setup import PageSama


# todo add normal loop code

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


if __name__ == "__main__":
    all_normal_pages()
