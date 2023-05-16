# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
from typing import Any, Optional, List
from abstract_handler import AbstractHandler
from civitai_api_wrapper import CivitaiAbstractAPIWrapper

class CivitaiHandler(AbstractHandler):
    """
    Class, representing civitai API wrapper.
    """
    def __init__(self, api_wrapper: CivitaiAbstractAPIWrapper) -> None:
        """
        Initiation method.
        """
        super().__init__(api_wrapper)

    def load_model_folder(self, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for loading model folder.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass

    def update_metadata(self, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for updating cached metadata.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass

    def organize_models(self, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for organizing local models.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass

    def download_model(self, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for downloading a model.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass

    def download_asset(self, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for downloading an asset.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        pass