# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
import os
import copy
from typing import Any, Optional, List
from abstract_handler import AbstractHandler
from civitai_api_wrapper import CivitaiAbstractAPIWrapper
from ..utility.bronze import hashing_utility
from ..configuration import configuration as cfg


class CivitaiHandler(AbstractHandler):
    """
    Class, representing civitai API wrapper.
    """
    def __init__(self, api_wrapper: CivitaiAbstractAPIWrapper) -> None:
        """
        Initiation method.
        """
        super().__init__(api_wrapper)

    def load_model_folder(self, model_folder: str, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for loading model folder.
        :param model_folder: Model folder.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        self.cache["local_models"] = []
        self.cache["not_tracked"] = []
        self.cache["ignored"] = []
        for root, dirs, files in os.walk(model_folder, topdown=True):
            ignored_subfolder = False
            if any(subfolder in cfg.IGNORE_MODEL_SUBFOLDERS for subfolder in root.replace(model_folder, "").split("/")):
                ignored_subfolder = True
            for model_file in [file for file in files if any(file.endswith(model_extension) for model_extension in cfg.MODEL_EXTENSIONS)]:
                full_model_path = os.path.join(root, model_file)
                if model_file not in cfg.IGNORE_MODEL_FILES and not ignored_subfolder:
                    file_name, file_ext = os.path.splitext(model_file)
                    model_data = {
                        "file": file_name,
                        "extension": file_ext,
                        "folder": root,
                        "path": full_model_path,
                        "sha256": hashing_utility.hash_with_sha256(full_model_path)
                    }
                    api_data = self.collect_metadata("hash", model_data["sha256"])
                    if api_data:
                        model_data["metadata"] = api_data
                        model_data["api_url"] = self.api.get_api_url("id", api_data["modelId"])
                        model_data["source"] = self.api.base_url
                        self.cache["local_models"].append(copy.deepcopy(model_data))
                    else:
                        self.cache["not_tracked"].append(full_model_path)
                else:
                    self.cache["ignored"].append(full_model_path)



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