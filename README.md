# Soccer Dashboard

[SoccerMon](https://osf.io/uryz9/) is the largest elite soccer athlete health and performance monitoring dataset available today, including both subjective and objective metrics. The dataset was collected during 2020 and 2021 by two professional teams in the Norwegian women's elite soccer league (“Toppserien”) using the [PmSys athlete monitoring system](https://forzasys.com/pmSys.html).

Subjective data was collected in the context of _wellness_, _training load_,_game performance_, _injuries_, and _illnesses_, using the PmSys mobile app [PM Reporter Pro](https://play.google.com/store/apps/details?id=com.forzasys.pmsys&hl=en&gl=US&pli=1). Moreover, during training sessions and games, players used the wearable GPS performance tracking equipment [STATSports APEX](https://eu.shop.statsports.com/products/apex-athlete-series) to monitor objective metrics such as location, heart rate, speed, and acceleration. Overall, the SoccerMon dataset contains 54,485 subjective reports and 10,075 objective report, the latter including 6,248,770,794 GPS positions.

We present SoccerDashboard, a user-friendly, interactive, modularly designed and extendable dashboard for the analysis of the SoccerMon dataset in particular, and health and performance data from soccer athletes in general. SoccerDashboard is open-source and publicly accessible over the Internet for coaches, players and researchers from fields such as sports science and medicine. SoccerDashboard can simplify the analysis of soccer datasets with complex data structures, and serve as a reference implementation for multidisciplinary studies spanning various fields, as well as increase the level of scientific dialogue between professional soccer institutions and researchers.

# INTERNAL NOTES

- `main` branch: production branch, alias https://soccer-dashboard.simula.no
- `dev` branch: default branch for development, https://soccer-dashboard.streamlit.app
- `v2` branch: development branch for version 2
