#-*- coding: utf-8 -*-

import os
import re
import requests
import time
import unicodedata

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import parser

def get_html(link):

    html_return = "return document.getElementsByTagName('html')[0].innerHTML"

    start_time = time.time()

    driver.get(link)

    final_time = time.time()

    if final_time - start_time >= 1:

        driver.refresh()

    html = driver.execute_script(html_return)

    return html


def retrieve_links(page, company_name, forbidden_links):

    company_url = "https://www.reclameaqui.com.br/empresa/" + company_name + "/lista-reclamacoes/?pagina=" + str(page)

    html = get_html(company_url)

    links = parser.get_page_links(company_name, html)

    links = filter_forbidden_links(forbidden_links, links)

    return links, company_name


def read_data(file_name):

    with open(file_name, 'r') as file:

        return file.read().split('\n')


def filter_forbidden_links(forbidden_links, links):
    '''Retira links que estão listados no arquivo de links proibidos'''

    if links is not None:

        return list(filter(lambda link: link not in forbidden_links, links))

    return links


if __name__ == "__main__":

    forbidden_links = read_data("Aux/links_proibidos.txt")

    ids = ['tim-celular']

    amount_instances = 1

    #chrome_options = Options()
    #chrome_options.add_argument("--headless")

    driver = webdriver.Chrome()

    for company_id in ids:
        qt = 0
        page = 1
        ### fazer flag dos 15 minutos
        while qt < amount_instances:

            while True:

                links, company_name = retrieve_links(page, company_id, forbidden_links)

                if links is None or links:

                    break

            if links is not None and company_name is not None:

                complete_links = list(map(lambda link: "https://www.reclameaqui.com.br/" + company_name + link.replace('"', ''), links))

                for link in complete_links:

                    html = get_html(link)

                    time.sleep(1)

                    info = parser.retrieve_complaint_info(html, company_name)

                exit()

            qt += 1
            page = page + 1
        break
    driver.close()
