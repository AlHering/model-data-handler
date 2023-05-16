# -*- coding: utf-8 -*-
"""
****************************************************
*                     Utility                      *
*            (c) 2020-2021 Alexander Hering        *
****************************************************
"""
from time import sleep
from typing import Union, List, Any

import requests
from lxml import html

from ..silver import environment_utility, internet_utility

REQUEST_METHODS = {
    "GET": requests.get,
    "POST": requests.post,
    "PATCH": requests.patch,
    "DELETE": requests.delete
}


def get_page_content(url: str) -> html.HtmlElement:
    """
    Function for getting page content from URL.
    :param url: URL to get page content for.
    :return: Page content.
    """
    page = requests.get(url)
    return html.fromstring(page.content)


def get_session(proxy_flag: Union[str, dict] = "none") -> requests.Session:
    """
    Function for getting requests session.
    :param proxy_flag: Flag describing session configuration.
        Defaults to 'none', in which case a normal requests session is returned.
        'torsocks' sets the session proxies to standard tor socks proxy.
        'random' sets session to random proxy.
        'file' set session to random proxy from standard proxy file.
        Dictionary inputs are directly interpreted as session proxy dictionary, mapping protocols to proxy addresses.
    :return: Session.
    """
    session = requests.session()
    if isinstance(proxy_flag, dict):
        session.proxies = proxy_flag
    elif proxy_flag == "torsocks":
        session.proxies = {'http':  'socks5://127.0.0.1:9050',
                           'https': 'socks5://127.0.0.1:9050'}
    elif proxy_flag == "random":
        proxy = internet_utility.get_proxy(source="package")
        session.proxies = {'http': proxy,
                           'https': proxy}
    elif proxy_flag == "file":
        proxy = internet_utility.get_proxy(source="file")
        session.proxies = {'http': proxy,
                           'https': proxy}

    return session


def safely_get_elements(html_element: html.HtmlElement, xpath: str) -> List[Any]:
    """
    Function for safely searching for elements in a Selenium WebElement.
    :param html_element: LXML Html Element.
    :param xpath: XPath of the elements to find.
    :return: List of elements if found, else empty list.
    """
    return html_element.xpath(xpath)


def safely_collect(html_element: html.HtmlElement, data: dict) -> dict:
    """
    Function for safely collecting data by xpath into dictionary, meaning not found elements get skipped. In later cases
    the collected value will be None. Does not support dynamic cleaning method calls! Use collect function if necessary.
    :param html_element: LXML Html Element.
    :param data: Data collection dictionary.
    :return: In dict collected data.
    """
    return_data = {}
    for elem in data:
        if isinstance(data[elem], dict):
            return_data[elem] = safely_collect(html_element, data[elem])
        elif isinstance(data[elem], str):
            return_data[elem] = safely_get_elements(html_element, data[elem])
        else:
            return_data[elem] = get_targets_by_declaration(html_element, data[elem])
    return return_data


def get_targets_by_declaration(html_element: html.HtmlElement, declaration: Union[list, str]) -> Any:
    """
    Function for getting targets by declaration.
    :param html_element: LXML Html Element.
    :param declaration: Target declaration.
    :return: Targets.
    """
    if isinstance(declaration, str):
        return safely_get_elements(html_element, declaration)
    else:
        elements = safely_get_elements(html_element, declaration[0])
        func = lambda x: x
        if declaration[1].startwith("eval:"):
            func = declaration[1].replace("eval:", "")
        elif declaration[1].startswith("lambda"):
            func = eval(declaration[1])
        elif ".py" in declaration[1] and ":" in declaration[1]:
            func = environment_utility.get_function_from_path(declaration[1])
        return func(elements)


def safely_request_page(url, tries: int = 5, delay: float = 2.0) -> requests.Response:
    """
    Function for safely requesting page response.
    :param url: Target page URL.
    :param tries: Maximum number of tries. Defaults to 5.
    :param delay: Delay to wait before sending off next request. Defaults to 2.0 seconds.
    :return: Response.
    """
    resp = requests.get(url)
    j = 0
    while (resp.status_code == 404 or resp.status_code == 403) and j < tries:
        j += 1
        sleep(delay)
    return resp


def handle_barrier(html_element: html.HtmlElement, barrier_profile: dict) -> None:
    """
    Function for handling barrier.
    :param html_element: LXML Html Element.
    :param barrier_profile: Captcha profile.
    """
    solve_barrier(html_element, barrier_profile)


def solve_barrier(html_element: html.HtmlElement, barrier_profile: dict) -> None:
    """
    Function for solving barrier.
    :param html_element: LXML Html Element.
    :param barrier_profile: Captcha profile.
    """
    if barrier_profile["solve"] == "wait":
        sleep(barrier_profile["solution"])
    elif barrier_profile["solve"] == "click":
        get_targets_by_declaration(html_element, barrier_profile["solution"])
        pass
    elif barrier_profile["solve"] == "call":
        environment_utility.get_function_from_path(barrier_profile["solution"])(html_element)
