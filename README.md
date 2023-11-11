# a simple streamlit app

In this tutorial, we will:

1. Train a predictive model on our local computer, built on the Seattle House Prices dataset.
2. Build a web app which uses this model, and test it out locally.
3. Host the web app online using Streamlit (and GitHub).
   - Note: this web app uses GitHub as the data storage mechanism. In general, **this is not a good habit to get into.** But, we use it here for educational purposes.

## Prerequisites

This tutorial assumes the following:

- You are using [Miniconda](https://docs.conda.io/en/latest/miniconda.html) as your Python package manager.
- You have a GitHub account, and you're familiar with using git and .gitignore files.
- You can build and manage a pip Python environment using Miniconda.
- You are familiar with environment variables.

*A few notes:*

- *Below, `<myenv>` should be replaced with your project environment name. This should clearly allude to your project uniquely (usually, I let the environment name match the GitHub repository name).*
- *In Windows, if you lose the anaconda prompt, you can activate anaconda with `call C:\anaconda3\Scripts\activate.bat` (depending on where that `activate.bat` file is).*

## Project Setup

1. Create a new folder for your web app (give it an [appropriate](https://gravitydept.com/blog/devising-a-git-repository-naming-convention) name), and place it in your GitHub "projects" folder.
2. Initiate a Git repository in this folder with `git init` in the command line (after navigating to that folder with `cd`). Then, [add it to your GitHub Desktop](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/adding-a-repository-from-your-local-computer-to-github-desktop). You'll want to use Git early and often to ensure that your changes are tracked, and you can always go back to (or compare with) a past version that works.
   - Note the contents of the .gitignore file. Environment files (such as the .env file) should be strictly ignored.
3. Initialize a pip environment in this folder using the *environment.yml* file in this directory using `conda env create -f environment.yml`. 
4. Any time you add new packages to the environment, update the environment file, and save a new requirements file with `pip freeze > requirements.txt`.
   - **Note: all packages should be installed using pip.**

## Modularizing Code

When you feel ready for it, consider dividing your code into separate Python files, saved in modular folders. For example, you'll notice in this repository, there is a *utils* folder. In that folder, we have a few Python files with code that was tested out in Jupyter first. Once it was determined the code worked in Jupyter, it was transferred into the separate Python file as functions or Python [classes](https://www.w3schools.com/python/python_classes.asp).

This *utils* folder, including the *\_\_init__.py* file, creates a Python [package](https://docs.python.org/3/tutorial/modules.html#packages) or module. For instance, if you open a "scratch" notebook from the directory containing this folder, you'll find you can run code like `from utils.modeling import clean_data`. This keeps your notebook(s) clean, and it makes debugging much easier.

## Streamlit

The app in this repository is run on [Streamlit](https://streamlit.io/). Code can be tested locally with `streamlit run app.py` (assuming your app file name is `app.py`, of course). Eventually, you will need to set up a [Streamlit Cloud](https://streamlit.io/cloud) account to link your project GitHub repository.

Use [dotenv](https://github.com/theskumar/python-dotenv#getting-started) to manage environment variables. You'll need to `pip` install it, as directed in the instructions, then create a file with the name *.env* (notice the period) in your project directory to hold any keys or secrets. We'll be using dotenv to access Backblaze, below. **Make sure ".env" is added to your [.gitignore file](https://www.atlassian.com/git/tutorials/saving-changes/gitignore)**.

## Backblaze

Sign up for the [Backblaze B2 Cloud Storage](https://www.backblaze.com/b2/cloud-storage.html) service. At the time of writing this, the first 10GB are free! For more information on Backblaze, check out their [documentation](https://www.backblaze.com/b2/docs/).

1. Set up at least one storage bucket for your project, and at least one app key. It's recommended to keep the bucket *private*.
   - You can set the "Default Encryption" to be "Disabled". Enabling this just adds another level of protection which you can experiment with *if you like* (this tutorial assumes this is disabled).
2. You can use a Master App Key, or you can set up another one specific to your project.
   - When shown an app key or bucket key, make sure to save it in some file locally somewhere!
3. The easiest way to access files in your Backblaze B2 storage bucket using Python is with the [boto3 package](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) (already included in the environment.yml file). This package includes a few helper functions in the *utils/b2.py* file.
   - For more information on these interactions, and the ones in the *utils/b2.py* file, take a look at the [Backblaze API documentation](https://www.backblaze.com/b2/docs/python.html).
