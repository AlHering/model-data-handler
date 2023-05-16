# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
import os


BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DATA_PATH = os.path.join(BASE_PATH, "data")
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)