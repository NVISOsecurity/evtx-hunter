import vars
from helpers import utils
import dash_table
import pandas as pd
import hashlib
import logging
import json
from datetime import datetime


def create_filename_summary_table():
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
        style_cell={'textAlign': 'left', 'whiteSpace': 'pre-line'},
        page_size=20
    )

    return table


def create_interesting_events_table(rule_dict):
    graph_data_dict = dict({"timestamp": []})

    if "log_fields" in rule_dict.keys():
        graph_data_dict.update({"log_fields": []})

    if rule_dict["log_full_event"]:
        graph_data_dict.update({"full_event": []})

    for event in utils.retrieve_all_events():
        item_event_channel = event["Event"]["System"]["Channel"]
        if item_event_channel != rule_dict["event_channel"]:
            continue

        event = utils.normalize_event(event)
        event_matches_filter = False

        for filter_field in rule_dict["event_filter"].keys():
            if filter_field not in event["Event"]["EventData"].keys():
                event_matches_filter = False
                break
            elif str(event["Event"]["EventData"][filter_field]) != str(rule_dict["event_filter"][filter_field]):
                event_matches_filter = False
                break
            else:
                event_matches_filter = True

        if event_matches_filter:
            # If we reach here, then we have filtered out all non-matching events
            time_string = event["Event"]["System"]["TimeCreated"]["#attributes"]["SystemTime"]
            event_date = datetime.fromisoformat(time_string.replace('Z', '+00:00'))

            graph_data_dict["timestamp"].append(event_date)

            if rule_dict["log_full_event"]:
                graph_data_dict["full_event"].append(json.dumps(event["Event"], indent=4, sort_keys=True))

            if "log_fields" in rule_dict.keys():
                log_string = utils.create_log_fields_string(event, rule_dict["log_fields"])
                graph_data_dict["log_fields"].append(log_string)

    df = pd.DataFrame(graph_data_dict, columns=graph_data_dict.keys())

    if len(df) > 0:
        df.sort_values(by=['timestamp'], inplace=True, ascending=False)
        df['timestamp'] = df['timestamp'].dt.strftime('%m/%d/%Y %H:%M:%S')

    table = dash_table.DataTable(
        id='event_summary_table_' + hashlib.md5(rule_dict["rule_name"].encode()).hexdigest(),
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left', 'whiteSpace': 'pre-line'},
        page_size=20
    )

    return table


def create_first_occurence_table(rule_dict):
    graph_data_dict = dict({"first_occurence": []})
    
    if "log_fields" in rule_dict.keys():
        graph_data_dict.update({"log_fields": []})

    if "monitored_field" in rule_dict.keys():
        graph_data_dict.update({rule_dict["monitored_field"]: []})

    if rule_dict["log_full_event"]:
        graph_data_dict.update({"full_event": []})

    for event in utils.retrieve_all_events():
        item_event_channel = event["Event"]["System"]["Channel"]
        if item_event_channel != rule_dict["event_channel"]:
            continue

        event = utils.normalize_event(event)
        event_matches_filter = False

        for filter_field in rule_dict["event_filter"].keys():
            if filter_field not in event["Event"]["EventData"].keys():
                event_matches_filter = False
                break
            elif str(event["Event"]["EventData"][filter_field]) != str(rule_dict["event_filter"][filter_field]):
                event_matches_filter = False
                break
            else:
                event_matches_filter = True

        if event_matches_filter:
            # If we reach here, then we have filtered out all non-matching events
            time_string = event["Event"]["System"]["TimeCreated"]["#attributes"]["SystemTime"]
            event_date = datetime.fromisoformat(time_string.replace('Z', '+00:00'))

            if rule_dict["monitored_field"] in event["Event"]["EventData"].keys():
                if event["Event"]["EventData"][rule_dict["monitored_field"]] \
                        not in graph_data_dict[rule_dict["monitored_field"]]:
                    graph_data_dict[rule_dict["monitored_field"]].append(
                        event["Event"]["EventData"][rule_dict["monitored_field"]])
                    graph_data_dict["first_occurence"].append(event_date)

                    if rule_dict["log_full_event"]:
                        graph_data_dict["full_event"].append(json.dumps(event["Event"], indent=4, sort_keys=True))

                    if "log_fields" in rule_dict.keys():
                        log_string = utils.create_log_fields_string(event, rule_dict["log_fields"])
                        graph_data_dict["log_fields"].append(log_string)
                else:
                    first_occurence_index = graph_data_dict[rule_dict["monitored_field"]].index(
                        event["Event"]["EventData"][rule_dict["monitored_field"]])
                    earlier_seen_date = graph_data_dict["first_occurence"][first_occurence_index]

                    if event_date < earlier_seen_date:
                        graph_data_dict[rule_dict["monitored_field"]][first_occurence_index] = \
                            event["Event"]["EventData"][rule_dict["monitored_field"]]
                        graph_data_dict["first_occurence"][first_occurence_index] = event_date

                        if rule_dict["log_full_event"]:
                            graph_data_dict["full_event"][first_occurence_index] = json.dumps(event["Event"], indent=4, sort_keys=True)

                        if "log_fields" in rule_dict.keys():
                            log_string = utils.create_log_fields_string(event, rule_dict["log_fields"])
                            graph_data_dict["log_fields"][first_occurence_index] = log_string

    df = pd.DataFrame(graph_data_dict, columns=graph_data_dict.keys())

    if len(df) > 0:
        df.sort_values(by=['first_occurence'], inplace=True, ascending=False)
        df['first_occurence'] = df['first_occurence'].dt.strftime('%m/%d/%Y %H:%M:%S')

    table = dash_table.DataTable(
        id='event_summary_table_' + hashlib.md5(rule_dict["rule_name"].encode()).hexdigest(),
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'left', 'whiteSpace': 'pre-line'},
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
