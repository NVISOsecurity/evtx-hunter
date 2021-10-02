import os
from helpers import utils
import logging
import vars
import jsonlines
import uuid
import json


class EvtxLoader:
    def __init__(self, file_path):
        self.file_path = file_path

        self.logger = logging.getLogger('evtx-hunter')
        self.logger.setLevel(logging.DEBUG)

    def load_evtx_files(self):
        summary_dict = dict({"files": []})
        evtx_filenames = utils.get_recursive_filenames(self.file_path, ".evtx")

        for filename in evtx_filenames:
            total_events = 0

            self.logger.info("processing " + filename)
            tmp_filename = str(uuid.uuid4())
            output_filename = vars.TMP_DIR + "/evtx_dump/" + tmp_filename + ".json"

            # Convert evtx file to JSON
            os.system(vars.EXTERNAL_DIR + vars.EVTX_DUMP_EXE + " -o jsonl \"" + utils.evtx_dump_input(filename) + "\" -f "
                      + "\"" + utils.evtx_dump_output(output_filename) + "\"")

            event_counts = dict()
            try:
                with jsonlines.open(output_filename, "r") as reader:
                    for item in reader:
                        total_events += 1
                        item_event_channel = item["Event"]["System"]["Channel"]
                        event_id = item["Event"]["System"]["EventID"]

                        if type(event_id) != int:
                            event_id = event_id["#text"]

                        if item_event_channel not in event_counts.keys():
                            event_counts[item_event_channel] = dict()

                        if event_id not in event_counts[item_event_channel].keys():
                            event_counts[item_event_channel][event_id] = 1
                        else:
                            event_counts[item_event_channel][event_id] += 1

            except OSError:
                logging.error("Could not load " + filename + ". This could be caused by your Anti-Virus " \
                                                             "detecting it as malicious!")
                continue

            # Add the file to the summary dictionary
            tmp_file_dict = {"original_filename": filename, "json_dump_filename": output_filename,
                             "total_events": total_events, "event_channel_counts": event_counts}
            summary_dict["files"].append(tmp_file_dict)

            self.logger.info("processed " + str(total_events) + " events")

        with open(vars.TMP_DIR + "files.json", "w") as outfile:
            json.dump(summary_dict, outfile, indent=4)
