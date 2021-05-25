import os
import plotly.graph_objects as go

import helpers.utils
import vars
import jsonlines
from helpers import utils
import dash_table
import pandas as pd
import hashlib
import logging
import json


def create_filename_summary():
    logger = logging.getLogger('evtx-hunter')
    logger.setLevel(logging.DEBUG)

    data = {'filename': [], 'events': []}
    for file_info in json.load(open(vars.TMP_DIR + "files.json", 'r'))["files"]:
        data['filename'].append(file_info['original_filename'])
        data['events'].append(file_info['total_events'])

    df = pd.DataFrame(data, columns=data.keys())
    df.sort_values(by=['events'], inplace=True, ascending=False)

    table = dash_table.DataTable(
        id='filename_summary_table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        page_size=20
    )

    return table


def create_event_summary(event_channel):
    data = {'event_id': [], 'events': []}
    event_summary_dict = dict()

    for item in utils.retrieve_all_events():
        item_event_channel = item["Event"]["System"]["Channel"]
        if event_channel != item_event_channel:
            continue

        event_id = item["Event"]["System"]["EventID"]

        if type(event_id) != int:
            event_id = event_id["#text"]

        if event_id not in event_summary_dict.keys():
            event_summary_dict[event_id] = 1
        else:
            event_summary_dict[event_id] += 1

    data['event_id'] = event_summary_dict.keys()
    data['events'] = event_summary_dict.values()

    df = pd.DataFrame(data, columns=data.keys())
    df.sort_values(by=['events'], inplace=True, ascending=False)

    table = dash_table.DataTable(
        id='event_summary_table_' + hashlib.md5(event_channel.encode()).hexdigest(),
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        page_size=20
    )

    return table
