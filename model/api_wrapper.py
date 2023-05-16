# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
from typing import Any, Optional, List
import abc


class AbstractAPIWrapper(abc.ABC):
    """
    Abstract class, representing a API wrapper object.
    """
    @abc.abstractmethod
    def check_connection(*args: Optional[List], **kwargs: Optional[dict]) -> bool:
        """
        Abstract method for checking connection.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        :return: True if connection was established successfuly else False.
        """
        pass

    @abc.abstractmethod
    def collect_metadata(identifier: str, model_id: Any, *args: Optional[List], **kwargs: Optional[dict]) -> dict:
        """
        Abstract method for acquring model data by identifier.
        :param identifier: Type of identification.
        :model_id: Identification of specified type.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        :return: Metadata for given model ID.
        """
        pass