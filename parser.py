#-*- coding: utf-8 -*-
### parser para as páginas
import re
import unicodedata

from bs4 import BeautifulSoup

def get_page_links(company_name, html):

    return retrieve_multiple_by_tag('href="/' + company_name, "\"", html)


def retrieve_complaint_info(complete_html, company_name):
    """

        Method resposible for retrieve all the informar needed.

        Complain ID
        User Location
        Category
        Product
        Problem
        Title
        User Complain #1
        Complain Date #1
        ...
        User Complain #N
        Complain Date #N

        Company Answer #1
        Company Answer Date #1
        ...
        Company Answer #N
        Company Answer Date #N
    """

    start_position = [a.start() for a in re.finditer("userAgent", complete_html)][0]

    html = complete_html[start_position:]

    # where all the data will be stored
    complain_info = {}

    search_tags = {
                    'Complain ID': ('legacyId":', ','),
                    'User Location': ('userCity":"', '",'),
                    "Title": ('title":"', '",')
                  }

    complain_info = retrieve_tokens(search_tags, html, complain_info, retrieve_by_unique_tag)


    category_tags = {
                    'Category': (r'href="/empresa/tim-celular/lista-reclamacoes/\?categoria=*', '</a>'),
                    'Product': (r'href="/empresa/tim-celular/lista-reclamacoes/\?produto=*', '</a>'),
                    'Problem': (r'href="/empresa/tim-celular/lista-reclamacoes/\?problema=*', '</a>')
                  }

    complain_info = retrieve_tokens(category_tags, complete_html, complain_info, retrieve_by_unique_tag)

    for key in category_tags.keys():

        complain_info[key] = re.sub(r'[~^0-9]', '', complain_info[key].replace('">', ''))

    multiple_tags = {
                        "Company Answer": ('"sc-1o3atjt-4 JkSWX">', '</p></div></div></div><div>'),
                        "Answer Date": ('"sc-1o3atjt-3 ipwWvs">', '</span>'),
                        "User Complain": ('description":', '",'),
                        "Complain Date": (r'"marketplaceComplain":.*,"created":"', '",'),
                    }

    complain_info = retrieve_tokens(multiple_tags, html, complain_info, retrieve_multiple_by_tag)

    return complain_info


def retrieve_tokens(tags, html, complain_info, method):

    for key in tags:

        start_tag, end_tag = tags[key]

        complain_info[key] = method(start_tag, end_tag, html)

    return complain_info


def retrieve_by_unique_tag(start_tag, end_tag, html):

    start_position = [a.end() for a in re.finditer(start_tag, html)]

    if start_position:

        start_position = start_position[0]

        end_position = [a.start() for a in re.finditer(end_tag, html)]

        final_position = list(filter(lambda position: position > start_position, end_position))[0]

        return html[start_position: final_position]

    return ''


def retrieve_multiple_by_tag(start_tag, end_tag, html):

    start_positions = [a.end() for a in re.finditer(start_tag, html)]

    if start_positions:

        end_positions = [a.start() for a in re.finditer(end_tag, html)]

        token_positions = {start: list(filter(lambda position: position > start, end_positions))[0] for start in start_positions}

        return list(map(lambda start, end: html[start: end], token_positions.keys(), token_positions.values()))

    return ''
