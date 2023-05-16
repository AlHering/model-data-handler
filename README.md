# model-data-handler
Toolbox for handling Machine Learning model data.

## Environment
An `.env` file should be added into the `/configuration` folder.
If you are using git, it is advised to create a .env file outside of the scope, tracked by git.
Create a soft-link to that file, name it `.env` and put it into the `/configuration` folder.

The `.env` file should contain:
- CIVITAI_API_KEY: Your civitai API key.
- HUGGINGFACE_API_KEY: Your Huggingface API key.