# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
from typing import Any, Optional, List
from abstract_api_wrapper import AbstractAPIWrapper

class CivitaiAbstractAPIWrapper(AbstractAPIWrapper):
    """
    Class, representing civitai API wrapper.
    """
    def __init__(self) -> None:
        """
        Initiation method.
        """
        pass

    def check_connection(self, *args: Optional[List], **kwargs: Optional[dict]) -> bool:
        """
        Method for checking connection.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        :return: True if connection was established successfuly else False.
        """
        pass

    def collect_metadata(self, identifier: str, model_id: Any, *args: Optional[List], **kwargs: Optional[dict]) -> dict:
        """
        Method for acquring model data by identifier.
        :param identifier: Type of identification.
        :model_id: Identification of specified type.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        :return: Metadata for given model ID.
        """
        pass