import os
import plotly.graph_objects as go

import helpers.utils
import vars
import jsonlines
from helpers import utils
import dash_table
import pandas as pd
import hashlib


def create_filename_summary():
    data = {'filename': [], 'events': []}
    for filename in os.listdir(vars.TMP_DIR):
        total_events = 0
        f = os.path.join(vars.TMP_DIR, filename)
        with jsonlines.open(f) as reader:
            for item in reader:
                total_events += 1

        data['filename'].append(filename)
        data['events'].append(total_events)

    df = pd.DataFrame(data, columns=data.keys())
    table = dash_table.DataTable(
        id='filename_summary_table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left'}
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

    sorted_dict = helpers.utils.sort_dict(event_summary_dict, reverse=True)

    data['event_id'] = sorted_dict.keys()
    data['events'] = sorted_dict.values()

    df = pd.DataFrame(data, columns=data.keys())
    table = dash_table.DataTable(
        id='event_summary_table_' + hashlib.md5(event_channel.encode()).hexdigest(),
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left'}
    )

    return table
