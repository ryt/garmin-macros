# garmin-macros
A collection of personal helpers and utilities for the Garmin Connect app and website.

#### Install

Create an alias that points to `gm`. Replace `{install}` with your installation directory.

```bash
alias gm='{install}/garmin-macros/gm'
```

#### Usage

Show the help manual.

```console
gm
gm  man|help
```

Retrieve and export all garmin activities for given month as a json file. Exported files are stored inside a `logs/YYYY/` directory. 

```console
gm  cur|current|tod|today|month
gm  {YYYY-MM}
gm  2024-01
```
> The same logs directory can be shared with [activity-metrics](https://github.com/ryt/activity-metrics) if the garmin module is used in activity metrics.

#### Libraries
This project uses [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) and [Garth](https://github.com/matin/garth) to connect to the Garmin API. It was also originally created to be complementary to [activity-metrics](https://github.com/ryt/activity-metrics), and the same logs directories can be shared by the two projects. The garmin module in activity metrics can also read and use the same exported json files.

