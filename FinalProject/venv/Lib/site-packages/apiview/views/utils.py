# encoding: utf-8
"""
View utils package
"""
from __future__ import unicode_literals, absolute_import


def split_camel_name(name, fall=False):
    """Split camel formated names:

    GenerateURLs => [Generate, URLs]
    generateURLsLite => [generate, URLs, Lite]
    """
    if not name:
        return []

    lastest_upper = name[0].isupper()
    idx_list = []
    for idx, char in enumerate(name):
        upper = char.isupper()
        # rising
        if upper and not lastest_upper:
            idx_list.append(idx)
        # falling
        elif fall and not upper and lastest_upper:
            idx_list.append(idx-1)
        lastest_upper = upper

    l_idx = 0
    name_items = []
    for r_idx in idx_list:
        name_items.append(name[l_idx:r_idx])
        l_idx = r_idx
    name_items.append(name[l_idx:])

    return name_items
