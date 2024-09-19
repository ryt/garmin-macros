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

Retrieve and export all garmin activities for given month as a json file. Exported files are stored inside a `logs/YYYY/`<sup>[1](#n1)</sup> directory. 

```console
gm  cur|current|tod|today|month
gm  {YYYY-MM}
gm  2024-01
```

#### CSV Rendering & Display

The `gencsv` command can combine all the JSON files for a given year and generate a simple readable CSV file with all the activities of the year. The command can also be used with the shortcuts `gen` and `-g`. 

Once generated, the CSV file will be saved by default inside a directory named `gen/services/garmin/`<sup>[1](#n1)</sup> on the same level as the `logs/` directory. If those directories don't exist, be sure to create them before you run the command.

> 

```console
gm  gencsv|gen|-g   {YYYY}
gm  gencsv|gen|-g   2024
```

#### Libraries

This project uses [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) and [Garth](https://github.com/matin/garth) to connect to the Garmin API.

##### Related Projects

- <i id="n1">1</i>: The specific naming of the directories comes from the fact that data storage locations are shared with a related project: [activity-metrics](https://github.com/ryt/activity-metrics). The `logs/` and `gen/` directories are used for log files and generated CSV files in activity metrics. This project was originally created to be complementary to activity metrics. The garmin module in activity metrics can also read and use the same exported json files.

- Also, aside from activity metrics, which comes with a web interface for viewing and analyzing garmin data, if you'd like to simply view generated CSV files on your browser, you can use my other related project, [webcsv](https://github.com/ryt/webcsv), which is a lightweight Flask-based csv viewer.
