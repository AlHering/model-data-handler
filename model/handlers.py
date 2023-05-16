# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
from typing import Any, Optional, List
import abc
from api_wrapper import AbstractAPIWrapper
from utility.bronze import json_utility

class AbstractHandler(abc.ABC):
    """
    Abstract class, representing a handler object.
    """
    def __init__(api_wrapper: AbstractAPIWrapper) -> None:
        """
        Initiation method for handler objects
        """
        self.cache = {}
        self.api = api_wrapper

    def collect_metadata(identifier: str, model_id: Any) -> dict:
        """
        Method for acquring model data by identifier.
        :param identifier: Type of identification.
        :model_id: Identification of specified type.
        :return: Metadata for given model ID.
        """
        return self.api.collect_metadata(identifier, model_id)

    def import_data(import_path: str) -> None:
        """
        Method for importing data.
        :param import_path: Import path.
        """
        self.cache = json_utility.load(import_path)

    def export_data(export_path: str) -> None:
        """
        Method for exporting data.
        :param export_path: Export path.
        """
        json_utility.save(self.cache, export_path)

    @abc.abstractmethod
    def load_model_folder(*args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Abstract method for loading model folder.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass

    @abc.abstractmethod
    def update_metadata(*args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Abstract method for updating cached metadata.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass

    @abc.abstractmethod
    def organize_models(*args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Abstract method for organizing local models.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass

    @abc.abstractmethod
    def download_model(*args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Abstract method for downloading a model.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass

    @abc.abstractmethod
    def download_asset(*args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Abstract method for downloading an asset.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass
