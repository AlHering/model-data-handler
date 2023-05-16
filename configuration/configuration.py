# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
import paths as PATHS
from dotenv import load_dotenv

"""
ENVIRONMENT FILE
"""
ENV = load_dotenv(".env")
CIVITAI_API_KEY = ENV.get("CIVITAI_API_KEY", "")
HUGGINGFACE_API_KEY = ENV.get("HUGGINGFACE_API_KEY", "")
IGNORE_MODEL_SUBFOLDERS = ENV.get("IGNORE_MODEL_SUBFOLDERS", [])
IGNORE_MODEL_FILES = ENV.get("IGNORE_MODEL_FILES", [])


"""
Further configuration
"""
MODEL_EXTENSIONS = [".ckpt", ".safetensors", ".pt", ".pth", ".zip"]