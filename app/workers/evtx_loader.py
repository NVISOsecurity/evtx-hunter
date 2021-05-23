import os
import helpers
import logging
import datetime
import vars
import json
import jsonlines


class EvtxLoader:
    def __init__(self, file_path):
        self.file_path = file_path

        self.logger = logging.getLogger('evtx-hunter')
        self.logger.setLevel(logging.DEBUG)

    def load_evtx_files(self):
        evtx_filenames = helpers.get_recursive_filenames(self.file_path, ".evtx")
        total_events = 0

        for filename in evtx_filenames:
            self.logger.info("processing " + filename)

            ts = datetime.datetime.now().timestamp()
            output_filename = vars.TMP_DIR + str(ts) + ".json"

            # Convert evtx file to JSON
            os.system(vars.EXTERNAL_DIR + "evtx_dump-v0.7.2.exe -o jsonl \"" + filename + "\" -f "
                      + output_filename)

            with jsonlines.open(output_filename, "r") as reader:
                for obj in reader:
                    print(obj["Event"]["System"]["Computer"])
                    total_events += 1

            self.logger.info("loaded " + str(total_events) + " events")