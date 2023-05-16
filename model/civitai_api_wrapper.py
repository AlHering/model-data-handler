# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
import requests
import json
from typing import Any, Optional, List
from ..configuration import configuration as cfg
from abstract_api_wrapper import AbstractAPIWrapper

class CivitaiAbstractAPIWrapper(AbstractAPIWrapper):
    """
    Class, representing civitai API wrapper.
    """
    def __init__(self) -> None:
        """
        Initiation method.
        """
        self.base_url = "https://civitai.com/"
        self.api_base_url = "https://civitai.com/api/v1/"
        self.model_by_versionhash_url = "https://civitai.com/api/v1/model-versions/by-hash/"
        self.model_by_id_url = "https://civitai.com/api/v1/models/"


    def check_connection(self, *args: Optional[List], **kwargs: Optional[dict]) -> bool:
        """
        Method for checking connection.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        :return: True if connection was established successfuly else False.
        """
        return requests.get(self.base_url).status_code == 200

    def collect_metadata(self, identifier: str, model_id: Any, *args: Optional[List], **kwargs: Optional[dict]) -> dict:
        """
        Method for acquring model data by identifier.
        :param identifier: Type of identification.
        :model_id: Identification of specified type.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        :return: Metadata for given model ID.
        """
        resp = requests.get({"hash": self.model_by_versionhash_url, "id": self.model_by_id_url}[identifier] + str(model_id), headers={"Authorization": cfg.CIVITAI_API_KEY})
        try:
            meta_data = json.loads(resp.content)
            if meta_data is not None and not "error" in meta_data:
                return meta_data
        except json.JSONDecodeError:
                return {}