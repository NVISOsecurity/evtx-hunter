import argparse
import os
import vars
import dash
from helpers.evtx_loader import EvtxLoader
from helpers import utils
from graphing import table, histogram
import dash_html_components as html
import dash_core_components as dcc
from datetime import date, datetime


def main():
    logger = utils.setup_logger()
    logger.info("started evtx-hunter")

    vars.PROJECT_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    vars.TMP_DIR = vars.PROJECT_ROOT_DIR + "/../tmp/"
    vars.EXTERNAL_DIR = vars.PROJECT_ROOT_DIR + "/../external/"
    vars.RULE_DIR = vars.PROJECT_ROOT_DIR + "/../rules/"

    parser = argparse.ArgumentParser(description="Dump a binary EVTX file into XML.")
    parser.add_argument("evtx_folder", type=str,
                        help="Path to the Windows EVTX event log file folder")

    args = parser.parse_args()

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    vars.DASH_APP = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    vars.DASH_APP.title = "evtx-hunter"

    utils.remove_all_tmp_json_files()
    utils.load_event_id_mappings()

    evtxloader = EvtxLoader(args.evtx_folder)
    evtxloader.load_evtx_files()

    logger.info("generating graphs and building models, this can take a while")

    event_histogram = histogram.create_histogram()
    filename_summary_table = table.create_filename_summary_table()
    event_channels = utils.get_all_event_channels()

    report_date = str("report date: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    # =====================
    # Build the report page
    # =====================
    children = [
        html.Hr(),
        html.H1(children='evtx-hunter'),
        html.H4(children=report_date),
        html.Hr(),
        html.H2(children="Event histogram"),
        dcc.Graph(figure=event_histogram),
        html.H2(children="File summary"),
        filename_summary_table
    ]

    # event channel summary
    children.append(html.Hr())
    children.append(html.H2(children="Event channel summary"))
    children.append(html.Hr())

    for event_channel in event_channels:
        if event_channel is not None:
            event_summary_table = table.create_event_channel_summary(event_channel)

            children.append(html.H3(children=event_channel))
            children.append(event_summary_table)

    # interesting event rules
    children.append(html.Hr())
    children.append(html.H2(children="Interesting event rules"))
    children.append(html.Hr())

    for rule in utils.retrieve_all_occurence_rules():
        occurence_table = table.create_interesting_events_table(rule)

        children.append(html.H3(children=rule["rule_name"]))
        children.append(occurence_table)

    # first occurence rules
    children.append(html.Hr())
    children.append(html.H2(children="First occurence rules"))
    children.append(html.Hr())

    for rule in utils.retrieve_all_first_occurence_rules():
        first_occurence_table = table.create_first_occurence_table(rule)

        children.append(html.H3(children=rule["rule_name"]))
        children.append(first_occurence_table)

    # layout the entire page
    vars.DASH_APP.layout = html.Div(children=children,
                                    style={'width': '80%', 'margin': 'auto'})


if __name__ == "__main__":
    main()
    vars.DASH_APP.run_server(debug=False)
