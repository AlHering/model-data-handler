# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
import os
import copy
import numpy
from typing import Any, Optional, List
from abstract_handler import AbstractHandler
from civitai_api_wrapper import CivitaiAbstractAPIWrapper
from ..utility.bronze import hashing_utility, dictionary_utility
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
        self.nsfw_image_score_threshold = 0.3

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
                        "file": model_file,
                        "extension": file_ext,
                        "folder": root,
                        "path": full_model_path,
                        "sha256": hashing_utility.hash_with_sha256(full_model_path),
                        "status": "found"
                    }
                    api_data = self.collect_metadata("hash", model_data["sha256"])
                    if api_data:
                        model_data["metadata"] = api_data
                        model_data["api_url"] = self.api.get_api_url("id", api_data["modelId"])
                        model_data["source"] = self.api.base_url
                        self.cache["local_models"].append(copy.deepcopy(model_data))
                        model_data["status"] = "collected"
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
        for model in self.cache["local_models"]:
            metadata = self.collect_metadata("hash", model["sha256"])
            if metadata and not dictionary_utility.check_equality(model["metadata"], metadata):
                model["metadata"] = copy.deepcopy(metadata)

    def calculate_local_metadata(self, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for calculating local cached metadata.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        for model in [m for m in self.cache["local_models"] if "metadata" in m]:
            model["local_metadata"] = model.get("local_metadata", {})
            model["local_metadata"]["nsfw"] = model["local_metadata"].get("nsfw", 
                                                                          {"model": model["metadata"]["nsfw"],
                                                                           "image_score": self._calculate_image_nsfw_score(model)})
            if "ssot" not in model["local_metadata"]["nsfw"]:
                model["local_metadata"]["nsfw"]["ssot"] = model["local_metadata"]["nsfw"]["model"] or model["local_metadata"]["nsfw"]["image_score"] >= self.nsfw_image_score_threshold
            
            model["local_metadata"]["tags"] = model["metadata"].get("tags", {}).values()
            model["local_metadata"]["main_tag"] = self._calculate_main_tag(model)
            model["status"] = "qual"

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

    def _calculate_image_nsfw_score(model: dict) -> Optional[float]:
        """
        Internal method for calculating the image based NSFW-score for a model.
        :param model_metadata: Model data.
        :return: Float, describing the models image based NSFW-score or None if image check failed.
        """
        score = None
        full_image_count = 0
        full_nsfw_count = 0
        for model_version in model["metadata"]["modelVersions"]:
            full_image_count += len(model_version["images"])
            full_nsfw_count += len([img for img in model_version["images"] if img["nsfw"]])
            if any(model["file"] == file for file in model_version["files"]):
                image_count = len(model_version["images"])
                nsfw_count = len([img for img in model_version["images"] if img["nsfw"]])
                score = numpy.round(numpy.true_divide(nsfw_count, image_count), decimals=2)
        if score is None:
            score = numpy.round(numpy.true_divide(full_nsfw_count, full_image_count), decimals=2)
        return score

    def _calculate_main_tag(model: dict) -> Optional[str]:
        """
        Internal method for calculating the main model tag.
        :param model_metadata: Model data.
        :return: Main model tag or None, if none was found.
        """
        if model["metadata"]["type"].lower() in ["checkpoint", "vae"]:
            current_reference = cfg.DICTS.CIVITAI_TAGS_A
        else:
            current_reference = cfg.DICTS.CIVITAI_TAGS_B

        for main_type in current_reference:
            containing_main = any(tag in model["local_metadata"]["tags"] for tag in current_reference[main_type]) 
            not_containing_other = not any(any(tag in model["local_metadata"]["tags"] for tag in current_reference[other_type]) for other_type in current_reference if other_type != main_type)
            if containing_main and not_containing_other:
                return main_type
        for main_type in current_reference:
            if "*" in current_reference[main_type]:
                return main_type