# Soccer Dashboard

SoccerMon is the largest data set available today with both subjective and objective data. The data were collected and used by two professional teams during the 2020 and 2021 seasons in the Norwegian women's elite soccer league (“Toppserien”). The teams used the PmSys athlete monitoring system34 to log subjective parameters, including training load, wellness, sickness, and injuries after every session, in addition to wellness once a day and sickness and injuries whenever they occurred. Moreover, during the training sessions, the players used wearable tracking equipment (STATSports APEX) to monitor total distance, high-speed running distance, sprint distance, accelerations and decelerations, and peak speed. 
In total, the dataset contains 54,485 subjective reports and 10,075 objective measurement sessions and 6,248,770,794 GPS positions measured on the fields.
Here's how SoccerMon can play valuable role in developing better analytical models not only for sport, but also for other areas of subjective relationships, position information and time data.

## Requirements

Make sure you have, at least, Python version 3.7 before you start the installation.You can check your Python version on the command line/terminal/shell. 

Windows

    Press Win+R
    Type powershell
    Press OK or Enter

macOS

    Go to Finder
    Click on Applications
    Choose Utilities -> Terminal

Linux

    Open the terminal window
   

### Display your Python version
```
Run the following command :  python --version OR python -V, on the command line and press Enter. 
```
### Softwares update installation

If your version of Python doesn't fit the requirments, update it by downloading the latest version at :  https://www.python.org/downloads/

Update the package-management system used to install and manage software packages, pip, (https://pip.pypa.io/en/stable/installation/) if your version of python hasn't been downloaded from python.org 

### Python virtual environment

We recommend running the commands in a virtual environment. This ensures that the dependencies pulled in for Streamlit don't impact any other Python projects you're working on.
Exemple of environment management/dependencies:

  - poetry (https://python-poetry.org/)
 
  - conda (https://www.anaconda.com/products/distribution)

## Installation
    
### Install Streamlit with Anaconda 

Streamlit's officially-supported environment manager on Windows is Anaconda Navigator (https://docs.anaconda.com/navigator/).

If you don't have Anaconda install yet, follow the steps provided on the Anaconda installation page (https://docs.anaconda.com/anaconda/install/windows/).

### Install Streamlit

Install Streamlit on on Windows/macOS/Linux (https://docs.streamlit.io/library/get-started/installation)

### Install Python libraries

In order to run the repository locally, a list of Python libraries needed downloaded and installed : 

- streamlit : version >= 1.14.0 (https://pypi.org/project/streamlit/)
```
pip install streamlit
```
- pandas: version >= 0.18 (https://pypi.org/project/pandas/)
```
pip install pandas
```
- matplotlib: >= 3.6.0 (https://pypi.org/project/matplotlib/)
```
pip install matplotlib
```
- numpy: >= 1.23.4 (https://pypi.org/project/numpy/)
```
pip install numpy
```
- ploty: >= 5.10.0 (https://pypi.org/project/plotly/)
```
pip install plotly
```
- scikit-learn: >= 1.1.2 (https://pypi.org/project/scikit-learn/)
```
pip install -U scikit-learn
```
- seaborn: >= 0.12.1 (https://pypi.org/project/seaborn/)
```
pip install seaborn
```
- statsmodels: >= 0.13.2 (https://pypi.org/project/statsmodels/)
```
pip install statsmodels
``` 
## Cloning the repository

When a repository is created on GitHub.com, it exists as a remote repository. You can clone your repository to create a local copy on your computer and sync between the two locations (https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository?tool=webui)

Another option is to download an install a Git GUI. Exemple of Git GUI:

- Gitkraken : https://www.gitkraken.com/
- Sourcetree : https://www.sourcetreeapp.com/

## Deployment (Local)

To launch the app locally, in the terminal, you can run the following command : 
```
streamlit run app.py
```
Please make sure that you need to navigate to the directory where the Python script is saved :
```
soccer-dashboard/streamlit_app 
```
Otherwise, you’ll have to specify the full path to the file : 
```
streamlit run soccer-dashboard/streamlit_app/app.py
```
Open in the browser :
```
http://localhost:3000 
```

## Deployment (Cloud)

- Sign into https://share.streamlit.io
- Create a new app conected to the relevant branch of your repository and specify the main file path (example: `dev` branch in the `simulamet-host/soccer-dashboard` repository, with `streamlit_app/app.py` as the main file)
- Wait a couple of minutes and your first app will be deployed.

![Screenshot from 2022-11-04 11-41-22](https://user-images.githubusercontent.com/84230658/199953952-bb704a85-ce38-42aa-87a1-c4217c34db3b.png)

### Demonstration Videos

Demonstration videos for installing Streamlit via Anaconda are available on YouTube:

•	https://www.youtube.com/watch?v=Vu5Bw745vXg

•	https://www.youtube.com/watch?v=dkvgzL3gJVY
