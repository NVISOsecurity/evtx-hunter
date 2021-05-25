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


def create_event_channel_summary(event_channel):
    data = {'event_id': [], 'events': [], 'description': []}
    event_summary_dict = dict()
    event_description_list = list()

    for file_info in json.load(open(vars.TMP_DIR + "files.json", 'r'))["files"]:
        for item_event_channel in file_info["event_channel_counts"]:
            if event_channel != item_event_channel:
                continue
            else:
                for event_id in file_info["event_channel_counts"][item_event_channel].keys():
                    event_count = file_info["event_channel_counts"][item_event_channel][event_id]

                    if event_id not in event_summary_dict.keys():
                        event_summary_dict[event_id] = event_count
                        event_description_list.append(utils.get_description_for_event_id(event_id))
                    else:
                        event_summary_dict[event_id] += event_count

    data['event_id'] = event_summary_dict.keys()
    data['events'] = event_summary_dict.values()
    data['description'] = event_description_list

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
