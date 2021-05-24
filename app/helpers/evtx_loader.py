import os
from helpers import utils
import logging
import datetime
import vars
import jsonlines
import time


class EvtxLoader:
    def __init__(self, file_path):
        self.file_path = file_path

        self.logger = logging.getLogger('evtx-hunter')
        self.logger.setLevel(logging.DEBUG)

    def load_evtx_files(self):
        evtx_filenames = utils.get_recursive_filenames(self.file_path, ".evtx")

        for filename in evtx_filenames:
            total_events = 0

            self.logger.info("processing " + filename)
            basename = os.path.basename(filename)
            output_filename = vars.TMP_DIR + basename + ".json"

            # Convert evtx file to JSON
            os.system(vars.EXTERNAL_DIR + vars.EVTX_DUMP_EXE + " -o jsonl \"" + filename + "\" -f "
                      + "\"" + output_filename + "\"")

            with jsonlines.open(output_filename, "r") as reader:
                for obj in reader:
                    total_events += 1

            self.logger.info("processed " + str(total_events) + " events")