#!/usr/bin/env python3

v = '0.0.1'
c = 'Copyright (C) 2024 Ray Mentose.'
man="""
Garmin Macros: Utilities & helper functions for Garmin Connect.
--
Usage

  param[0]      param[1]            param[2]
  --------      --------            --------

  Retrieve all activities for given month and export them as a json file
  ----------------------------------------------------------------------
  gm            (YYYY-MM|tod|today|now|cur|current|month)

  Combine all activity json files for a given year and convert them to a simplified CSV
  -------------------------------------------------------------------------------------
  gm            (gencsv|gen|-g)     {year}

  Copy gmdash.html to the gen directory of your personal 'Metrics' location
  -------------------------------------------------------------------------
  gm            (cpd|copy-dash)     {gen_directory}

  Help manual and version
  -----------------------
  gm            (man|help|-h|--help)
  gm            (-v|--version)

--

"""

import os
import re
import sys
import json
import shutil
import calendar
import datetime

from garth.exc import GarthHTTPError

sys.path.append(f'{os.path.dirname(os.path.abspath(os.path.realpath(__file__)))}/lib/python-garminconnect')

from garminconnect import (
  Garmin,
  GarminConnectAuthenticationError,
  GarminConnectConnectionError,
  GarminConnectTooManyRequestsError,
)


# Function from python-garminconnect/example.py

def init_api(email, password):
  """Initialize Garmin API with your credentials."""

  try:
    # Using Oauth1 and OAuth2 token files from directory
    print(f"Trying to login to Garmin Connect using token data from directory '{tokenstore}'...")

    garmin = Garmin()
    garmin.login(tokenstore)

  except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
    # Session is expired. You'll need to log in again
    print('Login tokens not present, login with your Garmin Connect credentials to generate them.\n' f"They will be stored in '{tokenstore}' for future use.")
    try:
      # Ask for credentials if not set as environment variables
      if not email or not password:
        email, password = get_credentials()

      garmin = Garmin(email, password)
      garmin.login()
      # Save Oauth1 and Oauth2 token files to directory for next login
      garmin.garth.dump(tokenstore)
      print(f"Oauth tokens stored in '{tokenstore}' directory for future use. (first method)")
      # Encode Oauth1 and Oauth2 tokens to base64 string and safe to file for next login (alternative way)
      token_base64 = garmin.garth.dumps()
      dir_path = os.path.expanduser(tokenstore_base64)
      with open(dir_path, "w") as token_file:
        token_file.write(token_base64)
      print(f"Oauth tokens encoded as base64 string and saved to '{dir_path}' file for future use. (second method)")
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError, requests.exceptions.HTTPError) as err:
      logger.error(err)
      return None

  return garmin


def to_json(output):
  return json.dumps(output, indent=2)


def escape_for_csv(input):
  """Prepares the given input for csv output"""
  if isinstance(input, str):
    # escape a double quote (") with additional double quote ("")
    value = input.replace('"', '""')
    value = '"' + value + '"'
    return value
  else:
    return input


def preserve_keys(data, pres):
  """Preserves only the list of keys in 'pres' for given dict 'data'"""
  resp = []
  for d in data:
    resp.append({key: d[key] for key in pres if key in d})
  return resp



email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
tokenstore = os.getenv('GARMINTOKENS') or '~/.garminconnect'
tokenstore_base64 = os.getenv('GARMINTOKENS_BASE64') or '~/.garminconnect_base64'
api = None


today = datetime.date.today()
logs_dir = f'{os.path.abspath(os.curdir)}/logs/' # can be shared with activity-metrics
gen_dir  = f'{os.path.abspath(os.curdir)}/gen/' # can also be shared with activity-metrics
gen_srv  = f'{gen_dir}services/garmin/'



def main():

  if len(sys.argv) == 1:
    return print(man.strip())

  elif sys.argv[1] in ('-v','--version'):
    return print(f'Version: {v}')

  elif sys.argv[1] in ('man','help','-h','--help'):
    return print(man.strip())

  elif sys.argv[1] in ('cpd','copy-dash'):
    gmdash = f'{os.path.dirname(os.path.abspath(os.path.realpath(__file__)))}/gm-dash/public/gm-dash.html'
    cpfile = sys.argv[2] + '/' if len(sys.argv) == 3 else './'
    cpfile = f"{cpfile.strip('/')}/gm-dash.html"
    shutil.copyfile(gmdash, cpfile)
    return print(f'Successfully copied: {gmdash} -> {cpfile}')

  elif sys.argv[1] in ('gencsv','-g'):
    if len(sys.argv) == 3 and sys.argv[2]:
      year = sys.argv[2]
      ydir = f'{logs_dir}{year}/'
      gen_csv_file = f'{gen_srv}{year}-garmin-activities.csv'

      if os.path.exists(ydir) and os.path.isdir(ydir):
        files = os.listdir(ydir)
        garmin_files = sorted([file for file in files if file.startswith(f'garmin-{year}-')])

        if garmin_files:
          print(f'Combining all ({len(garmin_files)}) json files for year {year}.')
          combined_data = []
          for file in garmin_files:
            with open(f'{ydir}{file}', 'r') as data:
              json_data = json.load(data)
              combined_data.append(json_data)

          flattened_data = [item for sublist in combined_data for item in sublist]
          # temp ignore: 'activityType'
          final_data = preserve_keys(flattened_data, ['activityId','activityName','startTimeLocal','distance','duration','averageSpeed','maxSpeed','averageHR','maxHR','description'])
          final_data = sorted(final_data, key=lambda x: datetime.datetime.strptime(x['startTimeLocal'], '%Y-%m-%d %H:%M:%S'), reverse=True)

          print('- Converting JSON to CSV...')

          columns = list(final_data[0].keys())
          csv_string = ','.join(columns) + '\n'
          for row in final_data:
            csv_string += ','.join(str(escape_for_csv(row[column])) for column in columns) + '\n'

          print('- JSON successfully converted to CSV.')

          f = open(gen_csv_file, 'w')
          f.write(csv_string)
          f.close()

          print(f'File {gen_csv_file} successfully saved.')

        else:
          print(f'Sorry, we could not find any json files for the year {year}.')

      else:
        print(f'Sorry, the directory {ydir} could not be found.')

    else:
      return print('Please enter a valid year value.')

  else:

    # retrieve & export activities for month

    input_month = sys.argv[1]

    if input_month in ('now','cur','current','tod','today','month'):
      input_month = today.strftime('%Y-%m')

    if not re.match(r'^\d{4}-\d{2}$', input_month):
      sys.exit(f"Sorry, '{input_month}' is not in the YYYY-MM format. Please correct it.")

    im_split      = input_month.split('-')
    im_year       = im_split[0]
    im_month      = im_split[1]
    im_year_int   = int(im_year)
    im_month_int  = int(im_month)
    
    im_wkd_start, im_last_day = calendar.monthrange(im_year_int, im_month_int)

    input_month_start = datetime.datetime(im_year_int, im_month_int, 1).strftime('%Y-%m-%d')
    input_month_end   = datetime.datetime(im_year_int, im_month_int, im_last_day).strftime('%Y-%m-%d')

    logs_dir_year = f'{logs_dir}{im_year}/'
    log_json_file = f'{logs_dir_year}garmin-{im_year}-{im_month}.json'

    if not os.path.isdir(logs_dir_year):
      sys.exit(f'Sorry, the directory {logs_dir_year} does not exist. Please create it first.')

    api = init_api(email, password)
    acts_this_month = api.get_activities_by_date(input_month_start,input_month_end)

    f = open(log_json_file, 'w')
    f.write(to_json(acts_this_month))
    f.close()

    print(f'Activities ({len(acts_this_month)}) for the month ({input_month}) saved to {log_json_file} successfully.')



if __name__ == '__main__':
  main()
