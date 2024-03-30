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
> 

#### CSV Rendering & Display

The `gencsv` command can combine all the JSON files for a given year and generate a simple readable CSV file with all the activities of the year. The command can also be used with the shortcuts `gen` and `-g`. 

Once generated, the CSV file will be saved inside a directory named `gen/services/garmin/` on the same level as the `logs/` directory. If those directories don't exist, be sure to create them before you run the command.

> If you are using [activity-metrics](https://github.com/ryt/activity-metrics), the `gen` directory is also used to save generated CSV files for activity logs.

```console
gm  gencsv|gen|-g   {YYYY}
gm  gencsv|gen|-g   2024
```

Additional Note: In this project's main repository, the are currently two under constructions developments of a built-in dashboard: one is a Flask app (gmdash.py) and the other is a Next.js app (gm-dash/ directory). Neither of those projects are currently operational and can be safely ignored.

Also, if you'd like to view generated CSV files through the browser, you can download and use [webcsv](https://github.com/ryt/webcsv) which is built with Flask and goes hand-in-hand with this project as well as activity-metrics.

#### Libraries
This project uses [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) and [Garth](https://github.com/matin/garth) to connect to the Garmin API. It was also originally created to be complementary to [activity-metrics](https://github.com/ryt/activity-metrics), and the same logs directories can be shared by the two projects. The garmin module in activity metrics can also read and use the same exported json files.

