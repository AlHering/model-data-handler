# model-data-handler
Toolbox for handling Machine Learning model data.

## Environment
An `.env` file should be added into the `/configuration` folder or filled, if already existing.
If you are using git, it is advised to create or move the `.env` file outside of the scope, tracked by git.
Create a soft-link to that file, name it `.env` and put only the soft-link into the `/configuration` folder.

The `.env` file should contain:
- CIVITAI_API_KEY: Your civitai API key.
- HUGGINGFACE_API_KEY: Your Huggingface API key.
- IGNORE_MODEL_SUBFOLDERS: List of subfolders inside model folders to ignore.
- IGNORE_MODEL_FILES: List of model files inside model folders to ignore.