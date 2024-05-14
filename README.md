# garmin-macros
A collection of personal helpers and utilities for the Garmin Connect app and website.

#### Install

Create an alias that points to `gm.py`. Replace `{install}` with your installation directory.

```bash
alias gm='{install}/garmin-macros/gm.py'
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
> The same logs directory can be shared with [activity-metrics](https://github.com/ryt/activity-metrics) if the garmin module is used in activity metrics. Read the "Related Projects" section below for more details on that project.
> 

#### CSV Rendering & Display

The `gencsv` command can combine all the JSON files for a given year and generate a simple readable CSV file with all the activities of the year. The command can also be used with the shortcuts `gen` and `-g`. 

Once generated, the CSV file will be saved by default inside a directory named `gen/services/garmin/`* on the same level as the `logs/` directory. If those directories don't exist, be sure to create them before you run the command.

> \* The specific naming of the directories comes from the fact that data storage locations are shared with the [activity-metrics](https://github.com/ryt/activity-metrics) project. The `gen/` directory is also used to save generated CSV files for daily activity logs.

```console
gm  gencsv|gen|-g   {YYYY}
gm  gencsv|gen|-g   2024
```

#### Libraries
This project uses [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) and [Garth](https://github.com/matin/garth) to connect to the Garmin API. As noted above, it was also originally created to be complementary to [activity-metrics](https://github.com/ryt/activity-metrics), and the same logs directories can be shared by the two projects. The garmin module in activity metrics can also read and use the same exported json files.

#### Related Projects

(Author Notes) Aside from activity metrics, which includes a web interface with a specific module for viewing and analyzing the garmin data, if you'd like to simply view generated CSV files through the browser, you can download and use my related project [webcsv](https://github.com/ryt/webcsv), which is a lightweight Flask-based csv viewer for the web.
