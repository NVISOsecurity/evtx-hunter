import os
import glob
import logging
import jsonlines
import vars
import json
import pandas as pd
import platform


def create_log_fields_string(event, log_fields):
    output_strings = list()
    for field in log_fields:
        if field in event["Event"]["EventData"]:
            output_strings.append(field + ":" + event["Event"]["EventData"][field])

    return "\n\n".join(output_strings)


def dict_flatten(in_dict, dict_out=None, parent_key=None, separator="."):
    if dict_out is None:
        dict_out = {}

    for k, v in in_dict.items():
        k = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            dict_flatten(in_dict=v, dict_out=dict_out, parent_key=k)
            continue

        dict_out[k] = v

    return dict_out


def normalize_event(event):
    flattened_dict = dict_flatten(event)

    event_id = event["Event"]["System"]["EventID"]
    if type(event_id) != int:
        event["Event"]["System"]["EventID"] = event_id["#text"]

    if "EventData" not in event["Event"].keys() or event["Event"]["EventData"] is None:
        event["Event"]["EventData"] = dict()

    for k in event["Event"]["System"].keys():
        event["Event"]["EventData"][k] = event["Event"]["System"][k]

    for k in event["Event"].keys():
        if k != "EventData":
            event["Event"]["EventData"][k] = event["Event"][k]

    if "UserData" in event["Event"].keys():
        for k in event["Event"]["UserData"].keys():
            event["Event"]["EventData"][k] = dict()
            for k_ in event["Event"]["UserData"][k].keys():
                event["Event"]["EventData"][k][k_] = event["Event"]["UserData"][k][k_]

    for k, v in flattened_dict.items():
        event["Event"]["EventData"][k.split(".")[-1]] = v

    return event


def retrieve_all_occurence_rules():
    for rule_info in json.load(open(vars.RULE_DIR + "interesting_events.json", 'r'))["rules"]:
        yield rule_info


def retrieve_all_first_occurence_rules():
    for rule_info in json.load(open(vars.RULE_DIR + "first_occurence.json", 'r'))["rules"]:
        yield rule_info


def retrieve_all_events():
    for file_info in json.load(open(vars.TMP_DIR + "files.json", 'r'))["files"]:
        with jsonlines.open(file_info["json_dump_filename"]) as reader:
            for item in reader:
                yield item


def get_description_for_event_id(event_id):
    event_id = int(event_id)
    description_loc = vars.EVENT_ID_MAPPING[vars.EVENT_ID_MAPPING['event_id'] == event_id]
    return ', '.join(description_loc["description"].tolist())


def load_event_id_mappings():
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


def is_cygwin():
    return platform.system().startswith("CYGWIN")


def is_64_bit():
    return os.uname().machine == "x86_64"


def get_cygwin_root():
    return "/cygwin" + ("64/" if is_64_bit() else "/")


def set_cygwin_vars():
    if is_cygwin():
        vars.CYGWIN = True
        vars.CYGWIN_DIR = get_cygwin_root()
        vars.CYGDRIVE_DIR = "/cygdrive/"
    else:
        vars.CYGWIN = False


# Forwards the original path or corrects it for Cygwin
def path_for_exe(path):
    # Path from Cygwin must be corrected before it can be used with .exe
    if vars.CYGWIN:
        # Ensures that the path is absolute 
        path = os.path.abspath(path)
        # Path leads to a place within Windows filesystem
        if path.startswith(vars.CYGDRIVE_DIR):
            # Deletes the cygrdive prefix and the drive letter
            path = path[11:]
        # Path leads to a place within Linux filesystem
        else:
            # Adds the Cygwin prefix so .exe can reach the place
            path = vars.CYGWIN_DIR + path
    return path
