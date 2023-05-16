# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
import paths as PATHS
from dotenv import load_dotenv


ENV = load_dotenv(".env")
CIVITAI_API_KEY = ENV["CIVITAI_API_KEY"]
HUGGINGFACE_API_KEY = ENV["HUGGINGFACE_API_KEY"]
