import Evtx.Evtx as Evtx
import os
import logging


def get_events(input_file, parse_xml=False):
    with Evtx.Evtx(input_file) as event_log:
        for record in event_log.records():
            yield record.lxml()


def filter_events_json(event_data, event_ids, fields=None):
    for evt in event_data:
        system_tag = evt.find("System", evt.nsmap)
        event_id = system_tag.find("EventID", evt.nsmap)
        if event_id.text in event_ids:
            event_data = evt.find("EventData", evt.nsmap)
            json_data = {}
            for data in event_data.getchildren():
                if not fields or data.attrib["Name"] in fields:
                    # If we don't have a specified field filter list, print all
                    # Otherwise filter for only those fields within the list
                    json_data[data.attrib["Name"]] = data.text

            yield json_data


def get_recursive_filenames(path, file_suffix):
    filenames = list()

    for subdir, dirs, files in os.walk(path):
        for file in files:
            filename = os.path.join(subdir, file)
            if filename.endswith(file_suffix):
                filenames.append(filename)

    return filenames


def convert_xml_event_to_json(xml_event):
    json_data = {}

    system_tag = xml_event.find("System", xml_event.nsmap)
    event_id = system_tag.find("EventID", xml_event.nsmap)
    event_data = xml_event.find("EventData", xml_event.nsmap)

    if event_id is not None:
        json_data['ID'] = event_id.text

    if event_data is not None:
        for data in event_data.getchildren():
            # If we don't have a specified field filter list, print all
            # Otherwise filter for only those fields within the list
            if "Name" in data.attrib.keys():
                json_data[data.attrib["Name"]] = data.text

    return json_data


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

