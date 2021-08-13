from django import template

register = template.Library()


@register.simple_tag
def access_list(some_list: list, index: int):
    """
    リストの要素のうち、インデックスで指定した要素を返す
    :param some_list: 要素を取得したいリスト
    :param index: 取得したいリストのインデックス
    :return: 指定したインデックスに格納されているリストの要素
    """
    try:
        result = some_list[int(index)]
        return result
    except:
        return ""
