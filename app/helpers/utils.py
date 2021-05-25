import os
import glob
import logging
import jsonlines
import vars
import json


def retrieve_all_events():
    for file_info in json.load(open(vars.TMP_DIR + "files.json", 'r'))["files"]:
        with jsonlines.open(file_info["json_dump_filename"]) as reader:
            for item in reader:
                yield item


def get_all_event_channels():
    event_channels = set()
    for item in retrieve_all_events():
        event_channels.add(item["Event"]["System"]["Channel"])

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