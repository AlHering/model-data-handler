# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
import os
from dotenv import load_dotenv
from utility.silver.environment_utility import get_lambda_function_from_string
ENV = load_dotenv(".env")


"""
Folder organizing configurations in the form
<HANDLER>_FOLDER_STRUCTURE = {
    "<MODEL_TYPE>": {
        "root_folder": "<absolute root folder for model of the specific type>",
        "staging_folder": "<absolute folder path where unorganized files live, files can be nested in subfolders>",
        "sort_into": <lambda expression for deciding, whether a model is to sort under this model type>,
        "sub_folders": <lambda expressions behind relative subfolder(s) as key, deciding whether to organize model under it>,
    },
    ...
}

Note, that you can use your .env file for sensible information such as folder paths or import lambda functions from strings.
Example: 
...
    "root_folder": ENV["MY_ROOT_FOLDER_FOR_<MODEL_TYPE>"],
    "sort_into": get_lambda_function_from_string(ENV["MY_SORTING_LAMBDA_FOR_<MODEL_TYPE>"]),
...
"""
CIVITAI_FOLDER_STRUCTURE = {
            "BLIP": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "BSRGAN": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BSRGAN"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BSRGAN", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "CHECKPOINTS": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "CHECKPOINTS"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "CHECKPOINTS", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "checkpoint" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and not data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["mixed", "photorealim", "illustration", "cartoon", "anime"]
                }
            },
            "CHECKPOINTS/NSFW": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "CHECKPOINTS", "NSFW"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "CHECKPOINTS", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "checkpoint" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["mixed", "photorealim", "illustration", "cartoon", "anime"]
                }
            },
            "CODEFORMER": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "CODEFORMER"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "CODEFORMER", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "CONTROL_NET": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "CONTROL_NET"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "CONTROL_NET", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "DEEPBOORU": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "DEEPBOORU"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "DEEPBOORU", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "EMBEDDINGS": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "EMBEDDINGS"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "EMBEDDINGS", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "embedding" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and not data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {}
            },
            "EMBEDDINGS/NSFW": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "EMBEDDINGS", "NSFW"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "EMBEDDINGS", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "embedding" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {}
            },
            "ESRGAN": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "ESRGAN"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "ESRGAN", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "GFPGAN": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "GFPGAN"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "GFPGAN", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "HYPERNETWORKS": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "HYPERNETWORKS"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "HYPERNETWORKS", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "hypernetwork" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and not data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            },
            "HYPERNETWORKS/NSFW": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "HYPERNETWORKS", "NSFW"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "HYPERNETWORKS", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "hypernetwork" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            },
            "KARLO": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "KARLO"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "KARLO", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "LDSR": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LDSR"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LDSR", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "LORA": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LORA"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LORA", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "lora" and data["status"] == "qual" and and not data["local_metadata"].get("archived", False) not data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            },
            "LORA/NSFW": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LORA", "NSFW"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LORA", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "lora" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            },
            "LYCORIS": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LYCORIS"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LYCORIS", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "lycoris" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and not data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            },
            "LYCORIS/NSFW": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LYCORIS", "NSFW"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "LYCORIS", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "lycoris" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            },
            "POSES": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "POSES"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "POSES", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "poses" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and not data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {}
            },
            "POSES/NSFW": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "POSES", "NSFW"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "POSES", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "poses" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {}
            },
            "REAL_ESRGAN": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "REAL_ESRGAN"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "REAL_ESRGAN", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "SCUNET": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "SCUNET"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "SCUNET", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "STABLE_DIFFUSION": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "STABLE_DIFFUSION"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "STABLE_DIFFUSION", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "SWINIR": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "SWINIR"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "TEXTUAL_INVERSION": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "TEXTUAL_INVERSION"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "textual inversion" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and not data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            },
            "TEXTUAL_INVERSION/NSFW": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "TEXTUAL_INVERSION", "NSFW"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "textual inversion" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            },
            "TORCH_DEEPDANBOORU": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "TORCH_DEEPDANBOORU"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP", "QUAL"),
                "sort_into": lambda _: False,
                "subfolders": {}
            },
            "VAE": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "VAE"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "vae" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and not data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["mixed", "photorealim", "illustration", "cartoon", "anime"]
                }
            },
            "VAE/NSFW": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "VAE", "NSFW"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "vae" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["mixed", "photorealim", "illustration", "cartoon", "anime"]
                }
            },
            "WILDCARDS": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "WILDCARDS"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "wildcards" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and not data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            },
            "WILDCARDS/NSFW": {
                "root_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "WILDCARDS", "NSFW"),
                "staging_folder": os.path.join(ENV["CIVITAI_MODEL_ROOT"], "BLIP", "QUAL"),
                "sort_into": lambda data: data["metadata"]["type"].lower() == "wildcards" and data["status"] == "qual" and not data["local_metadata"].get("archived", False) and data["local_metadata"]["nsfw"]["ssot"],
                "subfolders": {
                    main_tag: lambda data: data["local_metadata"]["main_tag"] == main_tag for main_tag in ["person", "clothing", "action", "background", "concept", "style"]
                }
            }
        }


"""
Tag organizing configurations in the form
<MODEL_TYPE_COLLECTION> = {
    "<MAIN_TAG>": <LIST OF TAGS THAT IDENTIFY <MAIN TAG>>
    ...
}

Note, that these configurations are used with separate logic inside the apropriate handler to automatically declare main tags.
The format can be freely adjusted. The dictionaries are only placed here for degluttering purposes.
"""
CIVITAI_TAGS_A = {
    "photorealism": ["photorealistic", "photorealism", "realistic"],
    "illustration": ["illustration"],
    "cartoon": ["cartoon"],
    "anime": ["anime"],
    "mixed": ["*"]
}


CIVITAI_TAGS_B = {
    "person": ["person", "character", "celebrity", "star", "singer", "actor", "pornstar"],
    "clothig": ["clothing", "fashion", "dress"],
    "action": ["#CHECK_MANUALLY"],
    "background": ["background", "backgrounds", "landscape", "landscapes", "scenery"],
    "concept": ["concept"],
    "style": ["style"]
}
