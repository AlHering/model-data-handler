# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
import os
import shutil
import copy
import numpy
from logging import Logger
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
        self._logger = Logger("[CivitaiHandler]")

    def load_model_folder(self, model_folder: str, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for loading model folder.
        :param model_folder: Model folder.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        self._logger.info(f"Loading model folders under '{model_folder}'...")
        self.cache["local_models"] = []
        self.cache["tracked"] = []
        self.cache["not_tracked"] = []
        self.cache["ignored"] = []
        for root, _, files in os.walk(model_folder, topdown=True):
            self._logger.info(f"Checking '{root}'...")
            ignored_subfolder = False
            if any(subfolder in cfg.IGNORE_MODEL_SUBFOLDERS for subfolder in root.replace(model_folder, "").split("/")):
                ignored_subfolder = True
            for model_file in self.extract_model_files(files):
                self._logger.info(f"Found '{model_file}'.")
                full_model_path = os.path.join(root, model_file)
                if full_model_path not in self.cache["tracked"]:
                    if model_file not in cfg.IGNORE_MODEL_FILES and not ignored_subfolder:
                        self._logger.info(f"'{model_file}' is not tracked, collecting data...")
                        self._logger.info(f"Loading '{root}'...")
                        _, file_ext = os.path.splitext(model_file)
                        model_data = {
                            "file": model_file,
                            "extension": file_ext,
                            "path": full_model_path,
                            "sha256": hashing_utility.hash_with_sha256(full_model_path),
                            "status": "found"
                        }
                        api_data = self.collect_metadata("hash", model_data["sha256"])
                        if api_data:
                            model_data["metadata"] = api_data
                            model_data["api_url"] = self.api.get_api_url("id", api_data["modelId"])
                            model_data["source"] = self.api.base_url
                            model_data["status"] = "collected"
                            self.cache["local_models"].append(copy.deepcopy(model_data))
                            self.cache["tracked"].append(full_model_path)
                        else:
                            self._logger.info(f"Could not load metadata, handler will not track '{model_file}'.")
                            self.cache["not_tracked"].append(full_model_path)
                    else:
                        self._logger.info(f"Ignoring '{model_file}'.")
                        self.cache["ignored"].append(full_model_path)
                else:
                    self._logger.info(f"'{model_file}' is already tracked.")
    
    def extract_model_files(self, files: List[str]) -> List[str]:
        """
        Method for extracting model files from a list of files (by extension).
        :param files: List of all files.
        :return: List of extracted model files.
        """
        return [file for file in files if any(file.endswith(model_extension) for model_extension in cfg.MODEL_EXTENSIONS)]

    def update_metadata(self, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for updating cached metadata.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        for model in self.cache["local_models"]:
            self._logger.info(f"Updating '{model['file']}' metadata.")
            metadata = self.collect_metadata("hash", model["sha256"])
            if metadata and not dictionary_utility.check_equality(model["metadata"], metadata):
                self._logger.info(f"Changes detected for '{model['file']}', updating...")
                model["metadata"] = copy.deepcopy(metadata)

    def calculate_local_metadata(self, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for calculating local cached metadata.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        for model in [m for m in self.cache["local_models"] if "metadata" in m]:
            self._logger.info(f"Calculating local metadata for '{model['file']}'...")
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
        self._logger.info("Starting model organization...")
        for profile in [cfg.DICTS.CIVITAI_FOLDER_STRUCTURE[model_type] for model_type in cfg.DICTS.CIVITAI_FOLDER_STRUCTURE]:
            for root, _, files in os.walk(profile["staging_folder"], topdown=True):
                for file in self.extract_model_files(files):
                    self._sort_model(os.path.join(root, file), profile)

    
    def reorganize_models(self, *args: Optional[List], **kwargs: Optional[dict]) -> None:
        """
        Method for reorganizing local models.
        :param args: Arbitrary arguments.
        :param kwargs: Arbitrary keyword arguments.
        """
        self._logger.info("Starting model reorganization...")
        for profile in [cfg.DICTS.CIVITAI_FOLDER_STRUCTURE[model_type] for model_type in cfg.DICTS.CIVITAI_FOLDER_STRUCTURE]:
            for root, _, files in os.walk(profile["root_folder"], topdown=True):
                for file in self.extract_model_files(files):
                    self._sort_model(os.path.join(root, file), profile)  
                    

    def _sort_model(self, file_path: str, sorting_profile: dict) -> None:
        """
        Internal method for sorting a model file.
        :param file_path: Model file path.
        :param sorting_profile: Sorting profile.
        """
        if file_path in self.cache["tracked"]:               
            model_data_options = [entry for entry in self.cache["local_models"] if entry["path"] == file_path]
            self._logger.info(f"Handling '{file_path}'...")
            if len(model_data_options) != 1:
                self._logger.warn(f"Found {len(model_data_options)} options for '{file_path}'! Skipping...")
            else:
                model_entry = model_data_options[0]
                if sorting_profile["sort_into"](model_entry):
                    self._logger.info(f"Validated '{file_path}' for sorting.")
                    for sub_folder in sorting_profile["subfolders"]:
                        if sorting_profile["subfolders"][sub_folder](model_entry):
                            target_path = os.path.join(sorting_profile["root_folder"], sub_folder)
                            self._move_model(model_entry, target_path)
                            self._logger.info(f"'{file_path}' sorted into '{target_path}'.")
                            break
        else:
            self._logger.warn(f"'{file_path}' is not tracked.")

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

    def _calculate_image_nsfw_score(self, model: dict) -> Optional[float]:
        """
        Internal method for calculating the image based NSFW-score for a model.
        :param model_metadata: Model data.
        :return: Float, describing the models image based NSFW-score or None if image check failed.
        """
        self._logger.info(f"Calculating image NSFW-score for '{model['file']}'...")
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
            self._logger.warn(f"Could not calculate version specific score for '{model['file']}',\ncalculating score over all versions...")
            score = numpy.round(numpy.true_divide(full_nsfw_count, full_image_count), decimals=2)
        self._logger.info(f"Calculated {score} for '{model['file']}'.")
        return score

    def _calculate_main_tag(self, model: dict) -> Optional[str]:
        """
        Internal method for calculating the main model tag.
        :param model_metadata: Model data.
        :return: Main model tag or None, if none was found.
        """
        result = None
        self._logger.info(f"Calculating main tag for '{model['file']}'...")
        if model["metadata"]["type"].lower() in ["checkpoint", "vae"]:
            current_reference = cfg.DICTS.CIVITAI_TAGS_A
        else:
            current_reference = cfg.DICTS.CIVITAI_TAGS_B

        for main_type in current_reference:
            containing_main = any(tag in model["local_metadata"]["tags"] for tag in current_reference[main_type]) 
            not_containing_other = not any(any(tag in model["local_metadata"]["tags"] for tag in current_reference[other_type]) for other_type in current_reference if other_type != main_type)
            if containing_main and not_containing_other:
                result =  main_type
        if main_type is None:
            for main_type in current_reference:
                if "*" in current_reference[main_type]:
                    result = main_type
        self._logger.info(f"Calculated '{result}' for '{model['file']}'...") if result is not None else self._logger.warn(f"Could not calculate main tag for '{model['file']}'.")
        return result
            
    def _interactively_set_model_tag(self, model: dict) -> Optional[str]:
        """
        Internal method for interactively adding the main model tag.
        :param model_metadata: Model data.
        :return: Main model tag or None, if none was set.
        """
        pass

    def _move_model(self, model_entry: dict, to_folder: str) -> None:
        """
        Internal method for moving model file.
        :param model_entry: Model data entry.
        :param to_folder: Target folder for model file.
        """ 
        target_path = os.path.join(to_folder, model_entry["file"])
        shutil.move(model_entry["path"], target_path)
        self.cache["tracked"][self.cache["tracked"].index(model_entry["path"])] = target_path
        model_entry["path"] = target_path
        model_entry["status"] = "sorted"
