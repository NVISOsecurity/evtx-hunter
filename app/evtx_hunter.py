import helpers
import argparse
import os
import vars
from workers.evtx_loader import EvtxLoader


def main():
    logger = helpers.setup_logger()
    logger.info("started evtx-hunter")

    vars.PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    vars.TMP_DIR = vars.PROJECT_ROOT_DIR + "/../tmp/"
    vars.EXTERNAL_DIR = vars.PROJECT_ROOT_DIR + "/../external/"

    parser = argparse.ArgumentParser(description="Dump a binary EVTX file into XML.")
    parser.add_argument("evtx", type=str,
                        help="Path to the Windows EVTX event log file folder")

    args = parser.parse_args()

    helpers.remove_all_tmp_json_files()
    evtxloader = EvtxLoader(args.evtx)
    evtxloader.load_evtx_files()


if __name__ == "__main__":
    main()
