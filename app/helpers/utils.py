import os
import glob
import logging
import jsonlines
import vars
import json
import pandas as pd


def retrieve_all_events():
    for file_info in json.load(open(vars.TMP_DIR + "files.json", 'r'))["files"]:
        with jsonlines.open(file_info["json_dump_filename"]) as reader:
            for item in reader:
                yield item


def get_description_for_event_id(event_id):
    event_id = int(event_id)
    description_loc = vars.EVENT_ID_MAPPING[vars.EVENT_ID_MAPPING['event_id'] == event_id]
    return description_loc["description"]


def get_event_id_mappings():
    df = pd.read_csv(vars.EXTERNAL_DIR + "event_id_mapping.csv", delimiter=";")

    # using dictionary to convert specific columns
    convert_dict = {'event_id': int}
    df = df.astype(convert_dict)
    vars.EVENT_ID_MAPPING = df


def get_all_event_channels():
    event_channels = set()
    for file_info in json.load(open(vars.TMP_DIR + "files.json", 'r'))["files"]:
        event_channels.update(list(file_info["event_channel_counts"].keys()))

    return list(event_channels)


def get_recursive_filenames(path, file_suffix):
    filenames = list()

    for subdir, dirs, files in os.walk(path):
        for file in files:
            filename = os.path.join(subdir, file)
            if filename.endswith(file_suffix):
                filenames.append(filename)

    return filenames


def remove_all_tmp_json_files():
    files = glob.glob(vars.TMP_DIR + "/evtx_dump/*.json")
    for f in files:
        os.remove(f)


def setup_logger():
    logger = logging.getLogger('evtx-hunter')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


def sort_dict(_dict, reverse=False):
    event_summary_list = sorted(_dict.items(), key=lambda x: x[1], reverse=reverse)
    return dict(event_summary_list)
