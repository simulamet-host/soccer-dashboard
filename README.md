# Soccer Dashboard

[SoccerMon](https://osf.io/uryz9/) is the largest elite soccer athlete health and performance monitoring dataset available today, including both subjective and objective metrics. The dataset was collected during 2020 and 2021 by two professional teams in the Norwegian women's elite soccer league (“Toppserien”) using the [PmSys athlete monitoring system](https://forzasys.com/pmSys.html). 

Subjective data was collected in the context of _wellness_, _training load_,_game performance_, _injuries_, and _illnesses_, using the PmSys mobile app [PM Reporter Pro](https://play.google.com/store/apps/details?id=com.forzasys.pmsys&hl=en&gl=US&pli=1). Moreover, during training sessions and games, players used the wearable GPS performance tracking equipment [STATSports APEX](https://eu.shop.statsports.com/products/apex-athlete-series) to monitor objective metrics such as location, heart rate, speed, and acceleration. Overall, the SoccerMon dataset contains 54,485 subjective reports and 10,075 objective report, the latter including 6,248,770,794 GPS positions.

We present SoccerDashboard, a user-friendly, interactive, modularly designed and extendable dashboard for the analysis of the SoccerMon dataset in particular, and health and performance data from soccer athletes in general. SoccerDashboard is open-source and publicly accessible over the Internet for coaches, players and researchers from fields such as sports science and medicine. SoccerDashboard can simplify the analysis of soccer datasets with complex data structures, and serve as a reference implementation for multidisciplinary studies spanning various fields, as well as increase the level of scientific dialogue between professional soccer institutions and researchers.


## Installation

### Python

Make sure you have Python version 3.7 (minimum) before you start the installation. You can check your Python version on the command line/terminal/shell. 

1. Open the terminal:

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
   

2. Display your Python version:

```
python --version
```

OR 

```
python -V
```

3. Install software updates if necessary:

If your version of Python does not fit the requirements, update it by downloading the relevant version [here](https://www.python.org/downloads/).

Update the package management system which can be used to install and manage software packages called [pip](https://pip.pypa.io/en/stable/installation/) if your version of Python has not been downloaded from python.org. 


### Installing Streamlit 

Install Streamlit on on Windows/macOS/Linux (https://docs.streamlit.io/library/get-started/installation).

Streamlit's officially-supported environment manager on Windows is Anaconda Navigator (https://docs.anaconda.com/navigator/). If you don't have Anaconda, follow the steps provided on the Anaconda installation page (https://docs.anaconda.com/anaconda/install/windows/). Demonstration videos for installing Streamlit via Anaconda are available on YouTube:

- https://www.youtube.com/watch?v=Vu5Bw745vXg
- https://www.youtube.com/watch?v=dkvgzL3gJVY


### Cloning the Repository

When a repository is created on GitHub.com, it exists as a remote repository. You can clone a repository to create a local copy on your computer and sync between the two locations (https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository?tool=webui).

You can clone the repository from the command line, or use a Git GUI such as:

- Gitkraken : https://www.gitkraken.com/
- Sourcetree : https://www.sourcetreeapp.com/


### Libraries

In order to run SoccerDashboard, a number of Python libraries need to be installed. 
<!--- 
- streamlit : version >= 1.14.0 (https://pypi.org/project/streamlit/)
- pandas: version >= 0.18 (https://pypi.org/project/pandas/)
- matplotlib: >= 3.6.0 (https://pypi.org/project/matplotlib/)
- numpy: >= 1.23.4 (https://pypi.org/project/numpy/)
- ploty: >= 5.10.0 (https://pypi.org/project/plotly/)
- scikit-learn: >= 1.1.2 (https://pypi.org/project/scikit-learn/)
- seaborn: >= 0.12.1 (https://pypi.org/project/seaborn/)
- statsmodels: >= 0.13.2 (https://pypi.org/project/statsmodels/)
-->

```
pip install -r requirements.txt
```

<!---
**Python virtual environment:** It is recommended to use a virtual environment. This ensures that the dependencies pulled in for Streamlit don't impact any other Python projects you're working on.
Example environment/dependency management tools:

  - poetry (https://python-poetry.org/)
  - conda (https://www.anaconda.com/products/distribution)
-->
    

## Deployment

### Deployment (Local)

To launch the app locally, you can run the following command : 
<!---
```
streamlit run app.py
```
Please make sure that you need to navigate to the directory where the Python script is saved :
```
soccer-dashboard/streamlit_app 
```
Otherwise, you’ll have to specify the full path to the file : 
-->
```
streamlit run soccer-dashboard/streamlit_app.py
```
Open dashboard in the browser :
```
http://localhost:3000 
```

### Deployment (Cloud)

- Sign into https://share.streamlit.io
- Create a new app conected to the relevant branch of your repository and specify the main file path (example: `dev` branch in the `simulamet-host/soccer-dashboard` repository, with `streamlit_app/app.py` as the main file)
- Under `Advanced settings` --> `Secrets`, add the database connection credentials:

```
[mysql]
host = <hostname>
port = <port number>
user = <username>
password = <password>
database = <database name>
``````

- Click "Deploy!" and wait until the app is live on Streamlit cloud.

![Screenshot from 2022-11-04 11-41-22](https://user-images.githubusercontent.com/84230658/199953952-bb704a85-ce38-42aa-87a1-c4217c34db3b.png)


# INTERNAL NOTES

- `main` branch: production branch, alias https://soccer-dashboard.simula.no
- `dev` branch: default branch for development, https://soccer-dashboard.streamlit.app
