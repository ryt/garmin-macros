#!/usr/bin/env python3

import os
import sys
import json
import datetime

from garth.exc import GarthHTTPError

sys.path.append('lib/python-garminconnect')

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

def init_api(email, password):
  """Initialize Garmin API with your credentials."""

  try:
    # Using Oauth1 and OAuth2 token files from directory
    print(
      f"Trying to login to Garmin Connect using token data from directory '{tokenstore}'...\n"
    )

    # Using Oauth1 and Oauth2 tokens from base64 encoded string
    # print(
    #   f"Trying to login to Garmin Connect using token data from file '{tokenstore_base64}'...\n"
    # )
    # dir_path = os.path.expanduser(tokenstore_base64)
    # with open(dir_path, "r") as token_file:
    #   tokenstore = token_file.read()

    garmin = Garmin()
    garmin.login(tokenstore)

  except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
    # Session is expired. You'll need to log in again
    print(
      "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
      f"They will be stored in '{tokenstore}' for future use.\n"
    )
    try:
      # Ask for credentials if not set as environment variables
      if not email or not password:
        email, password = get_credentials()

      garmin = Garmin(email, password)
      garmin.login()
      # Save Oauth1 and Oauth2 token files to directory for next login
      garmin.garth.dump(tokenstore)
      print(
        f"Oauth tokens stored in '{tokenstore}' directory for future use. (first method)\n"
      )
      # Encode Oauth1 and Oauth2 tokens to base64 string and safe to file for next login (alternative way)
      token_base64 = garmin.garth.dumps()
      dir_path = os.path.expanduser(tokenstore_base64)
      with open(dir_path, "w") as token_file:
        token_file.write(token_base64)
      print(
        f"Oauth tokens encoded as base64 string and saved to '{dir_path}' file for future use. (second method)\n"
      )
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError, requests.exceptions.HTTPError) as err:
      logger.error(err)
      return None

  return garmin



# Load environment variables if defined

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
tokenstore_base64 = os.getenv("GARMINTOKENS_BASE64") or "~/.garminconnect_base64"
api = None



# Example selections and settings

today = datetime.date.today()
startdate = today - datetime.timedelta(days=7)  # Select past week
start = 0
limit = 100
start_badge = 1  # Badge related calls calls start counting at 1
activitytype = ''  # Possible values are: cycling, running, swimming, multi_sport, fitness_equipment, hiking, walking, other
activityfile = 'activity.fit'  # Supported file types are: .fit .gpx .tcx
weight = 89.6
weightunit = 'kg'

def to_json(output):
  return json.dumps(output, indent=2)


def main():

  # Init API

  api = init_api(email, password)

  #print(api.get_activities_fordate(today.isoformat()))

  # get this month

  act_this_month = to_json(api.get_activities_by_date('2024-03-01',today))

  f = open('/Users/ray/Desktop/march.json', 'w')
  f.write(act_this_month)
  f.close()

  print(act_this_month)



if __name__ == '__main__':
  main()
