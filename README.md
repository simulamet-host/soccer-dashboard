# Soccer Dashboard

[SoccerMon](https://osf.io/uryz9/) is the largest elite soccer athlete health and performance monitoring dataset available today, including both subjective and objective metrics. The dataset was collected during 2020 and 2021 by two professional teams in the Norwegian women's elite soccer league (“Toppserien”) using the [PmSys athlete monitoring system](https://forzasys.com/pmSys.html).

Subjective data was collected in the context of _wellness_, _training load_,_game performance_, _injuries_, and _illnesses_, using the PmSys mobile app [PM Reporter Pro](https://play.google.com/store/apps/details?id=com.forzasys.pmsys&hl=en&gl=US&pli=1). Moreover, during training sessions and games, players used the wearable GPS performance tracking equipment [STATSports APEX](https://eu.shop.statsports.com/products/apex-athlete-series) to monitor objective metrics such as location, heart rate, speed, and acceleration. Overall, the SoccerMon dataset contains 54,485 subjective reports and 10,075 objective report, the latter including 6,248,770,794 GPS positions.

We present SoccerDashboard, a user-friendly, interactive, modularly designed and extendable dashboard for the analysis of the SoccerMon dataset in particular, and health and performance data from soccer athletes in general. SoccerDashboard is open-source and publicly accessible over the Internet for coaches, players and researchers from fields such as sports science and medicine. SoccerDashboard can simplify the analysis of soccer datasets with complex data structures, and serve as a reference implementation for multidisciplinary studies spanning various fields, as well as increase the level of scientific dialogue between professional soccer institutions and researchers.

## Quick Start Locally

- Install Python 3.8 or higher
- Clone the repo and run `cd soccer-dashboard`
- Run `pip install -r requirements.txt`
- Create a `secrets.toml` file in the `.streamlit` directory with connection credentials for the data source (see [Secrets Management](#secrets-management) for details)
- Run `streamlit run homepage.py`

## Deployment to Streamlit Cloud

- Fork the repo to your GitHub account
- Sign in to [Streamlit](https://share.streamlit.io/) with your GitHub account
- Click "New app" and enter the repo, branch, and file path (e.g., `your-account/soccer-dashboard`, `v2`, `homepage.py`)
- Under "Advanced settings", add the connection credentials as secrets (see [Secrets Management](#secrets-management) for details)
- Click "Deploy!"

## Secrets Management

To run the app locally, create a `secrets.toml` file in the `.streamlit` directory with connection credentials for the data source. The file should look like this:

```toml
[connections.mysql]
dialect = 'mysql'
host = 'xxx'
port = 3306
database = 'xxx'
username = 'xxx'
password = 'xxx'
```

Replace `xxx` with the actual connection credentials.

For security reasons, never commit the `secrets.toml` file!

To deploy the app to [Streamlit](https://share.streamlit.io/), paste the contents of the `secrets.toml` file as secrets in the app settings from the admin panel. See the [Streamlit documentation](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management) for more details.

# INTERNAL NOTES

- `main` branch: production branch, alias https://soccer-dashboard.simula.no
- `dev` branch: default branch for development, https://soccer-dashboard.streamlit.app
- `v2` branch: development branch for version 2, https://soccer-dashboard-v2.streamlit.app/

## Development

### Package Management

We recommend using virtual environments to manage the dependencies of the project. The standard library `venv` can be used to create a virtual environment.

To create a virtual environment, run `python -m venv myenv` in the project root directory.

Then, activate the virtual environment with `source myenv/bin/activate` on Unix or `myenv\Scripts\activate` on Windows.

Follow the [official tutorial](https://docs.python.org/3/tutorial/venv.html) for more information.

After creating and activating the virtual environment, install the required packages with `pip install -r requirements.txt`.

If you add new packages to the project, do not edit the `requirements.txt` file manually. Instead, make sure you have all the necessary packages and no unnecessary ones installed in your virtual environment, and then run `pip freeze > requirements.txt` to update the file.
