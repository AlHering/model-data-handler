# -*- coding: utf-8 -*-
"""
****************************************************
*                     Utility                      *
*            (c) 2022 Alexander Hering             *
****************************************************
"""
import traceback
from time import sleep
from typing import List, Any, Union

from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http.response import Response
from scrapy.selector import Selector

from ..silver import environment_utility


def start_crawl_process(spider: Spider, args: list, settings: dict) -> None:
    """
    Function for getting crawl process for given spider, arguments and settings.
    :param spider: Spider to execute inside process.
    :param args: Argument list.
    :param settings: Settings for crawler process.
    :return: Crawler process containing given spider, arguments and settings.
    """
    process = CrawlerProcess(settings=settings)
    process.crawl(spider, *args)
    process.start()


def collect(resp: Response, data: dict) -> dict:
    """
    Function for collecting data by xpath into dictionary.
    :param resp: scrapy response
    :param data: data collection dictionary
    :return: in dict collected data
    """
    return_data = {}
    for elem in data:
        if isinstance(data[elem], dict):
            if "#meta_xpath" in data[elem] and "#meta_lambda" in data[elem]:
                web_element = resp.xpath(data[elem]["#meta_xpath"]).get()
                lambda_function = eval(data[elem]["#meta_lambda"])
                return_data[elem] = lambda_function(web_element)
            else:
                return_data[elem] = collect(resp, data[elem])
        else:
            if data[elem].startswith("eval("):
                return_data[elem] = eval(data[elem].replace('eval(', '')[:-1],
                                         {"response": resp, "data": data, "elem": elem})
            else:
                return_data[elem] = resp.xpath(data[elem]).get()
    return return_data


def safely_collect(resp: Response, data: dict) -> dict:
    """
    Function for safely collecting data by xpath into dictionary, meaning not found elements get skipped. In later cases
    the collected value will be None.
    :param resp: Response to collect from.
    :param data: Data collection dictionary.
    :return: In dict collected data.
    """
    return_data = {}
    for elem in data:
        try:
            if isinstance(data[elem], dict):
                if "#meta_xpath" in data[elem] and "#meta_lambda" in data[elem]:
                    web_element = safely_extract_element(resp, data[elem]["#meta_xpath"])
                    if web_element:
                        lambda_function = eval(data[elem]["#meta_lambda"])
                        return_data[elem] = lambda_function(web_element)
                else:
                    return_data[elem] = safely_collect(resp, data[elem])
            else:
                if data[elem].startswith("eval("):
                    return_data[elem] = eval(data[elem].replace('eval(', '')[:-1],
                                             {"response": resp, "data": data, "elem": elem})
                else:
                    web_element = safely_get_elements(resp, data[elem])
                    if web_element:
                        return_data[elem] = web_element.getall()
                    else:
                        return_data[elem] = None
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            return_data[elem] = None
    return return_data


def safely_get_elements(resp: Response, xpath: str) -> List[Any]:
    """
    Function for safely searching for elements in a scrapy response.
    :param resp: Response to search in.
    :param xpath: XPath of the elements to find.
    :return: List of elements if found, else None.
    """
    try:
        return resp.xpath(xpath)
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        return []


def safely_get_element(resp: Response, xpath: str) -> Any:
    """
    Function for safely searching for an element in a scrapy response.
    :param resp: Response to search in.
    :param xpath: XPath of the elements to find.
    :return: Extracted element if found, else None.
    """
    try:
        return resp.xpath(xpath)[0]
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        return None


def safely_extract_elements(resp: Response, xpath: str) -> List[Selector]:
    """
    Function for safely extracting elements in a scrapy response.
    :param resp: Response to search in.
    :param xpath: XPath of the elements to find.
    :return: List of elements if found, else None.
    """
    try:
        return resp.xpath(xpath).getall()
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        return []


def safely_extract_element(resp: Response, xpath: str) -> Any:
    """
    Function for safely extracting an element in a scrapy response.
    :param resp: Response to search in.
    :param xpath: XPath of the elements to find.
    :return: Extracted element if found, else None.
    """
    try:
        return resp.xpath(xpath).get()
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        return None


def safely_get_text_content(resp: Response, xpath: str = ".") -> str:
    """
    Function for safely getting text content of element from response.
    :param resp: Response to search in.
    :param xpath: XPath for target element. Defaults to '.'.
    :return: Content text, if found, else empty string.
    """
    try:
        return resp.xpath("string(" + xpath + ")").getall()[0]
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        return ""


def safely_get_attribute(resp: Response, xpath: str, attribute: str) -> str:
    """
    Function for safely getting attribute content of an element from a scrapy response defined through given xpath.
    :param resp: Response to search in.
    :param xpath: XPath of the target element.
    :param attribute: Attribute name to search for.
    :return: Attribute content, if found, else empty string.
    """
    try:
        return resp.xpath(xpath).attrib[attribute]
    except KeyError:
        print("attributes: " + str(resp.xpath(xpath).attrib))
        traceback.print_exc()
        return ""


def get_targets_by_declaration(resp: Response, declaration: Union[list, str]) -> Any:
    """
    Function for getting targets by declaration.
    :param resp: Response to search in.
    :param declaration: Target declaration.
    :return: Targets.
    """
    if isinstance(declaration, str):
        result = safely_get_elements(resp, declaration)
        if result:
            result = result.getall()
        return result
    else:
        result = safely_get_elements(resp, declaration[0])
        if result:
            result = result.getall()
        func = lambda x: x
        if declaration[1].startwith("eval:"):
            func = declaration[1].replace("eval:", "")
        elif declaration[1].startswith("lambda"):
            func = eval(declaration[1])
        elif ".py" in declaration[1] and ":" in declaration[1]:
            func = environment_utility.get_function_from_path(declaration[1])
        return func(result)


def handle_barrier(resp: Response, barrier_profile: dict) -> None:
    """
    Function for handling barrier.
    :param resp: Response to search in.
    :param barrier_profile: Captcha profile.
    """
    solve_barrier(resp, barrier_profile)


def solve_barrier(resp: Response, barrier_profile: dict) -> None:
    """
    Function for solving barrier.
    :param resp: Response to search in.
    :param barrier_profile: Captcha profile.
    """
    if barrier_profile["solve"] == "wait":
        sleep(barrier_profile["solution"])
    elif barrier_profile["solve"] == "click":
        get_targets_by_declaration(resp, barrier_profile["solution"])
        pass
    elif barrier_profile["solve"] == "call":
        environment_utility.get_function_from_path(barrier_profile["solution"])(resp)
