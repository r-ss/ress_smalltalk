#!/usr/bin/env python
# import asyncio

import multiprocessing

from typing import Dict

# Copyright 2021 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""

Google Analytics Data API (GA4)
https://github.com/googleapis/python-analytics-data

Google Analytics Data API sample quickstart application.
This application demonstrates the usage of the Analytics Data API using
service account credentials.
Before you start the application, please review the comments starting with
"TODO(developer)" and update the code to use correct values.
Usage:
  pip3 install --upgrade google-analytics-data
  python3 quickstart.py
"""
# [START analyticsdata_quickstart]
from cgitb import reset
from urllib import response
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest

KEY_FILE_LOCATION = 'google_analytics_api_credentials.json'

# GOOGLE_APPLICATION_CREDENTIALS = KEY_FILE_LOCATION

# import os
from google.oauth2 import service_account

# client = language.LanguageServiceClient(credentials=credentials)


PROPERTIES = [
        {"name": "foldwrap.com", "property_id": "336517101"},
        {"name": "ress.ws", "property_id": "337630550"}
    ]

def sample_run_report(client, for_property_id):
    """Runs a simple report on a Google Analytics 4 property."""
    # TODO(developer): Uncomment this variable and replace with your
    #  Google Analytics 4 property ID before running the sample.
    # property_id = "YOUR-GA4-PROPERTY-ID"

    # [START analyticsdata_run_report_initialize]
    # Using a default constructor instructs the client to use the credentials
    # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # client = BetaAnalyticsDataClient()
    # print(KEY_FILE_LOCATION)
    # credentials = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION)
    
    # client = BetaAnalyticsDataClient(credentials=credentials)
    # client = BetaAnalyticsDataClient().from_service_account_json(KEY_FILE_LOCATION)
    # [END analyticsdata_run_report_initialize]

    # [START analyticsdata_run_report]
    request = RunReportRequest(
        property=f"properties/{for_property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    )
    response = client.run_report(request)
    # [END analyticsdata_run_report]
    # return response

    # [START analyticsdata_run_report_response]
    # for row in response.rows:
    #     print(row.dimension_values[0].value, row.metric_values[0].value)

    return response
    # [END analyticsdata_run_report_response]


# [END analyticsdata_quickstart]

def get_analytics_for(property: Dict):
    # try:
    credentials = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION)
    ga_client = BetaAnalyticsDataClient(credentials=credentials)



    response = sample_run_report(client=ga_client, for_property_id=property["property_id"])
    
    wv = 0
    for row in response.rows:
        wv += int(row.metric_values[0].value)
        # print(row.dimension_values[0].value, row.metric_values[0].value)

    result = {
        "name": property["name"],
        "weekly_visits": wv
    }

    return result

    # print(property["name"])
    # for row in response.rows:
        # print(row.dimension_values[0].value, row.metric_values[0].value)
    # except:
    #     return "error with Saint-Petersburg weather"
    # return r.strip()


def get_websites_analytics():

    pool = multiprocessing.Pool()
  
    # pool object with number of element
    pool = multiprocessing.Pool(processes=2)
  
    # input list
    inputs = PROPERTIES
  
    # map the function to the list and pass
    # function and input list as arguments
    outputs = pool.map(get_analytics_for, inputs)

    s = ""
    for r in outputs:
        s+=f"{r['name']}: {r['weekly_visits']}\n"  
    return s.strip()
