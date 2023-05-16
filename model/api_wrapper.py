# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
from typing import Any
import abc


class AbstractAPIWrapper(abc.ABC):
    """
    Abstract class, representing a API wrapper object.
    """

    @abc.abstractmethod
    def collect_metadata(identifier: str, model_id: Any) -> dict:
        """
        Abstract method for acquring model data by identifier.
        :param identifier: Type of identification.
        :model_id: Identification of specified type.
        """
        pass