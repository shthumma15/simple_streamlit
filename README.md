# a simple streamlit app

Using Google Cloud to train models, and Backblaze for data storage, etc.

## Environment Setup

1. [Create a environment.yml](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually) file containing the packages you think you'll need (check your `import` statements). **Make sure all your packages (except `pip` and maybe `python=x.x`) are under the `pip:` section.**
   - See the environment.yml file in this repo as an example.
   - Update this (manually) as you install more packages. It'll make it easier if you or anyone else ever wants to recreate the environment.
2. Create your environment from the file using `conda env create -f environment.yml`. Then, activate it with `conda activate <env name>`.
3. **IMPORTANT: Everything you install in this environment should be done using pip.**
4. Make a requirements file using `pip freeze > requirements.txt`
   - You'll have to rerun this command each time you install (or re-install) a new package.

If you like to use JupyterLab (instead of Notebook):

1. In this environment, install ipykernel with `pip install ipykernel`. 
2. Then, give it a kernel specification so that it shows up as a tile in JupyterLab:

   `python -m ipykernel install --user --name <env name> --display-name "<preferred kernel name>"`

*In most cases, it's okay to just let the `<env name>` be the same as the `<preferred kernel name>`.*

## Modularizing Code

When you feel ready for it, consider dividing your code into separate Python files, saved in modular folders. For example, you'll notice in this repository, there is a *utils* folder. In that folder, we have a few Python files with code that was tested out in Jupyter first. Once it was determined the code worked in Jupyter, it was transferred into the separate Python file as functions or Python [classes](https://www.w3schools.com/python/python_classes.asp).

This *utils* folder, including the *\_\_init__.py* file, creates a Python [package](https://docs.python.org/3/tutorial/modules.html#packages) or module. For instance, if you open a "scratch" notebook from the directory containing this folder, you'll find you can run code like `from utils.modeling import clean_data`. This keeps your notebook(s) clean, and it makes debugging much easier.

## On Git

It is highly encouraged that along with an environment, you should **create a git repo for every data science project**. This repository should contain things like code, .yml files, requirements.txt files, and sometimes .ipynb files. However it should **not** contain things like API keys, secrets, and in most cases it shouldn't contain any data.

Build a [.gitignore file](https://www.atlassian.com/git/tutorials/saving-changes/gitignore) **before your first commit**. In this file, consider setting git to ignore the files you don't want on GitHub. In the case of this project, there is a *config_vars.json* file that is stored only locally and on a protected GCP VM instance (you can't see it here on GitHub). Similarly, a *data* folder, *model.pickle* file, and a *scratch.ipynb* file are not meant to be saved to GitHub.

## Streamlit

The app in this repository is run on Streamlit. Code can be tested locally with `streamlit run app.py` (assuming your app file name is `app.py`, of course). Eventually, it will come time to set up a [Streamlit Cloud](https://streamlit.io/cloud) account, linked to project GitHub repositories.

**Use [Streamlit Secrets](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)** to save things like API keys and secrets (and other variables) behind Streamlit's security wall. You'll notice that the code in *app.py* checks for these variables first (to determine if it's being run on the Streamlit instance), then uses a *config_vars.json* file if it's being run locally. Alternatively, you can use a *.streamlit* folder [as directed by Streamlit](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management#develop-locally-with-secrets) (or add variables to your local environment path).

## Backblaze

Sign up for the [Backblaze B2 Cloud Storage](https://www.backblaze.com/b2/cloud-storage.html) service. At the time of writing this, the first 10GB are free! For more information on Backblaze, check out their [documentation](https://www.backblaze.com/b2/docs/).

1. Set up at least one storage bucket for your project, and at least one app key. It's recommended to keep the bucket *private*.
2. When shown an app key or bucket key, make sure to save it in some file locally somewhere!
3. The easiest way to access files in your Backblaze B2 storage bucket using Python is with the [boto3 package](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
   - For more information on these interactions, and the ones in the *utils/b2.py* file, take a look at the [Backblaze API documentation](https://www.backblaze.com/b2/docs/python.html).

## GCP

1. Set up a very simple compute VM instance in Google Cloud as you like (e.g., you can use the default settings, and the smallest engine).
2. Access the VM terminal by clicking the **SSH** (in-browser) button on the far right side of the VM row, under "Connect".
3. Install Git and Pip with `sudo apt-get install -yq git pip`.
4. Clone your project repository from GitHub with `git clone <repo url>`. To keep things simple, your repo can be public.
5. `cd` into your repository folder, which should have a *requirements.txt* file.
6. Install all your requirements with `pip install -r requirements.txt`.
7. *Note: In a GCP VM, Python may need to be accessed with the `python3` command instead of just `python`.*

Now, you should be able to upload/download files using the "UPLOAD FILE" and "DOWNLOAD FILE" buttons on the upper right of the in-browser terminal.

You can upload something like a *config_vars.json* file to the instance using the **UPLOAD FILE** button. You'll likely have to move this into your repository folder using `mv <filename> <reponame>/<filename>`. Then, you can download something like a *model.pickle* file once its trained using the **DOWNLOAD FILE** button.

#### Training a Model

- Once your VM contains all the files you need it to, you can train your model running a script like the *train_model.py* file, running `python3 train_model.py`. You can manually download the *model.pickle* file once it's trained, and save it to GitHub (or, you can do this from the VM terminal).
- Or, you can add code which sends the pickle file to Backblaze, which you can then gather in your *app.py* file.
- Lastly, you can use [Google Cloud Scheduler](https://cloud.google.com/scheduler/) to run jobs (like running *train_model.py*) on a periodic schedule. This can pull more recent data, update data, update the model, etc.