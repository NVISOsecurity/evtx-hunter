import argparse
import os
import vars
import dash
from helpers.evtx_loader import EvtxLoader
from helpers import utils
from graphing import table
import dash_html_components as html


def main():
    logger = utils.setup_logger()
    logger.info("started evtx-hunter")

    vars.PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    vars.TMP_DIR = vars.PROJECT_ROOT_DIR + "/../tmp/"
    vars.EXTERNAL_DIR = vars.PROJECT_ROOT_DIR + "/../external/"

    parser = argparse.ArgumentParser(description="Dump a binary EVTX file into XML.")
    parser.add_argument("evtx", type=str,
                        help="Path to the Windows EVTX event log file folder")

    args = parser.parse_args()

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    vars.DASH_APP = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    vars.DASH_APP.title = "evtx-hunter"

    utils.remove_all_tmp_json_files()
    evtxloader = EvtxLoader(args.evtx)
    evtxloader.load_evtx_files()

    filename_summary_table = table.create_filename_summary()
    event_channels = utils.get_all_event_channels()

    children = [
        html.H1(children='evtx-hunter'),
        html.H2(children="File summary"),
        filename_summary_table,
        html.H2(children="Event channel summary"),
    ]

    for event_channel in event_channels:
        if event_channel is not None:
            event_summary_table = table.create_event_summary(event_channel)

            children.append(html.H3(children=event_channel))
            children.append(event_summary_table)

    vars.DASH_APP.layout = html.Div(children=children,
                                    style={'width': '80%', 'margin': 'auto'})


if __name__ == "__main__":
    main()
    vars.DASH_APP.run_server(debug=False)
