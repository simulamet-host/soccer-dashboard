# Soccer Dashboard

[SoccerMon](https://osf.io/uryz9/) is the largest elite soccer athlete health and performance monitoring dataset available today, including both subjective and objective metrics. The dataset was collected during 2020 and 2021 by two professional teams in the Norwegian women's elite soccer league (“Toppserien”) using the [PmSys athlete monitoring system](https://forzasys.com/pmSys.html). 

Subjective data was collected in the context of _wellness_, _training load_, _game performance_, _injuries_, and _illnesses_, using the PmSys mobile app [PM Reporter Pro](https://play.google.com/store/apps/details?id=com.forzasys.pmsys&hl=en&gl=US&pli=1). Moreover, during training sessions and games, players used the wearable GPS performance tracking equipment [STATSports APEX](https://eu.shop.statsports.com/products/apex-athlete-series) to monitor objective metrics such as __[TODO: replace with raw metrics] total distance, high-speed running distance, sprint distance, accelerations and decelerations, and peak speed.[/TODO]__ 

Overall, the SoccerMon dataset contains 54,485 subjective reports and 10,075 objective measurement sessions, with 6,248,770,794 GPS positions measured in the field. Initial experiments have shown how different subjective and objective parameters are correlated, and have demonstrated the potential benefits of AI-based athlete performance forecasting applications. SoccerMon can play a valuable role in developing better analytical models, not only for soccer but also for other sports where athlete mobility and subjective wellbeing provide important insights into performance.

## Requirements

Make sure you have Python version 3.7 (minimum) before you start the installation. You can check your Python version on the command line/terminal/shell. 

### 1. Open the terminal

_Windows_

    Press Win+R
    Type powershell
    Press OK or Enter

_macOS_

    Go to Finder
    Click on Applications
    Choose Utilities -> Terminal

_Linux_

    Open the terminal window
   

### 2. Display your Python version

```
python --version
```

OR 

```
python -V
```


### 3. Install software updates if necessary

If your version of Python does not fit the requirements, update it by downloading the relevant version [here](https://www.python.org/downloads/).

Update the package management system which can be used to install and manage software packages called [pip](https://pip.pypa.io/en/stable/installation/) if your version of Python has not been downloaded from python.org. 


### Python virtual environment

It is recommend running the commands in a virtual environment. This ensures that the dependencies pulled in for Streamlit don't impact any other Python projects you're working on.
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
