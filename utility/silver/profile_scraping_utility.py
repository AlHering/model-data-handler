# -*- coding: utf-8 -*-
"""
****************************************************
*                     Utility                      *
*            (c) 2020-2021 Alexander Hering        *
****************************************************
"""
import os
import re
import subprocess
from subprocess import PIPE
from typing import Any, Optional
from typing import Union, List

import logging
from ..silver import internet_utility
from ..bronze import comparison_utility

logger = logging.Logger("[Utility]")
check_connection = internet_utility.check_connection
wait_for_connection = internet_utility.wait_for_connection
get_proxy = internet_utility.get_proxy
check_port_usable = internet_utility.check_port_usable
timeout = internet_utility.timeout


def download_with_wget(download_link: str, target_path: str, continue_download: bool = True,
                       time_out: int = 10, retry: int = 3, use_torsocks: bool = False) -> bool:
    """
    Function for downloading files to specified target path.
    :param download_link: Download link.
    :param target_path: Full path to download file to.
    :param continue_download: Specifies whether download should continue to download a partly downloaded file.
    Defaults to True.
    :param time_out: Declares timeout in seconds. Defaults to 10
    :param retry: Declares number of retries. Defaults to 3.
    :param use_torsocks: Declaration, whether to use torsocks or not.
    :return: True, if command was successful, else False.
    """
    # Attention! If command fails on Windows: Open administrative command prompt and run 'choco install wget'.
    not_finished = True
    for i in range(retry):
        if use_torsocks:
            command = "torsocks "
        else:
            command = ""
        command += "wget"
        if continue_download:
            command += " -c"
        command += " -T " + str(time_out) + ' -O "' + target_path + '" "' + download_link + '"'
        logger.log("initiate", command)
        if issue_cli_command(command, error_pattern=r"ERROR"):
            not_finished = False
        else:
            continue_download = True
    return not not_finished


def issue_cli_command(command: Union[str, List[str]], success_pattern: str = r'.*', error_pattern: str = r'.*') -> Optional[bool]:
    """
    Function for issuing command and getting live info.
    Taken from @https://stackoverflow.com/a/52091495 and adjusted.
    :param command: Command to issue.
    :param success_pattern: Regular expression to validate successful command run by last line. Defaults to r'.*'.
    :param error_pattern: Regular expression to validate failed command run by last line. Defaults to r'.*'.
    :return: True, if command was successful, False if command failed, None if unknown.
    """
    not_finished = True
    lines = []
    while not_finished:
        lines = []
        process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   stdin=PIPE,
                                   shell=True)

        while process.stdout.readable():
            line = process.stdout.readline()
            if not line:
                not_finished = False
                break
            lines.append(line.decode().strip())
            logger.info((lines[-1]))
    if re.match(error_pattern, lines[-1]):
        return False
    if re.match(success_pattern, lines[-1]):
        return True
    return None


def clean_path(path: str) -> str:
    """
    Function for cleaning paths by replacing double backslashes with single forward slashes.
    :param path: Path to be cleaned.
    :return: Cleaned path.
    """
    return path.replace("\\", "/")


def safely_create_path(path: str) -> None:
    """
    Function for safely creating folder path.
    :param path: Folder path to create.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def avoid_overwrite(path: str) -> str:
    """
    Function for calculating file name to avoid overwrites.
    :param path: Path for file potentially overwriting existing file.
    :return: Path not overwriting any existing files.
    """
    if os.path.exists(path):
        name, ext = os.path.splitext(path)
        path = name + "(1)" + ext
        i = 1
        while os.path.exists(path):
            path = path.replace(f"({str(i)}){ext}", f"({str(i + 1)}){ext}")
            i += 1
    return path


def check_control_values(target_value: Any, control_value: Any, comparison_type: str) -> bool:
    """
    Method for checking control value.
    :param target_value: Target value.
    :param control_value: Control value.
    :param comparison_type: Type of comparison.
        Valid types: 'equals', 'not_equals', 'contains', 'not_contains', 'is_contained' or 'not_is_contained'.
        Can also be a lambda function as string with target value as first parameter and control value as second parameter:
        E.g. 'lambda x, y: x >= y'.
    :return: True, if check succeeds, else False.
    """
    if comparison_type in comparison_utility.COMPARISON_METHOD_DICTIONARY:
        return comparison_utility.COMPARISON_METHOD_DICTIONARY[comparison_type](target_value, control_value)
    elif comparison_type.startswith("lambda"):
        func = eval(comparison_type)
        return func(target_value, control_value)
