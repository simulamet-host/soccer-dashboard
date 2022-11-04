# Soccer Dashboard

SoccerMon is the largest data set
Available today with both subjective and objective data collected over two years from two different elite women's football teams
teams. Specifically, our dataset contains *54,485* subjective reports and we have *10,075* objective measurement sessions
where there are *6,248,770,794* GPS positions measured on the fields. Some initial experiments show how different parameters
correlating and demonstrating the potential benefits of artificial intelligence-based forecasting systems. Here's how SoccerMon can play
valuable role in developing better analytical models not only for sport, but also for other areas of subjective relationships, position
information and time data.

## Requirements

### Installation

Make sure you have Python version 3 before you start the installation. 

You can check your Python version by running the following command:
```
python -V
```
After cloning this repo, the packages and Python libraries needed for running the app locally can be installed by running the following commands (*Versions specified in `requirements.txt`.*):
```
streamlit= ">=1.13.0"
pandas= ">=0.18"
matplotlib= ">=3.6.0"
numpy= ">=1.23.4"
pandas= ">=1.5.0"
ploty= ">=5.10.0"
scikit-learn= ">=1.1.2"
seaborn= ">=0.12.1"
statsmodels= ">=0.13.2"
```
You can use Poetry to help you specify, install, and resolve external packages in your projects. 

## Deployment (Local)

To launch the app locally, in the terminal, you can run the following command: `streamlit run app.py`. Please make sure that you need to navigate to the `soccer-dashboard/streamlit_app` directory where the Python script is saved. Otherwise, you’ll have to specify the full path to the file: `streamlit run soccer-dashboard/streamlit_app/app.py`.

Open http://localhost:3000 in the browser. The page will reload if you make edits.


## Deployment (Cloud)

- Sign into https://share.streamlit.io
- Create a new app conected to the relevant branch of your repository and specify the main file path (example: `dev` branch in the `simulamet-host/soccer-dashboard` repository, with `streamlit_app/app.py` as the main file)
- Wait a couple of minutes and your first app will be deployed.
![Screenshot from 2022-11-04 11-41-22](https://user-images.githubusercontent.com/84230658/199953952-bb704a85-ce38-42aa-87a1-c4217c34db3b.png)

