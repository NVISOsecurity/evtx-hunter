from PySide2.QtCore import QThreadPool
from PySide2.QtWidgets import QHeaderView

import helpers
import argparse
from PySide2 import QtWidgets
import sys
from views.main_window import MainWindow
import time
from workers.evtx_loader import  EvtxLoader


def main():
    logger = helpers.setup_logger()

    logger.info("started evtx-hunter")

    parser = argparse.ArgumentParser(
        description="Dump a binary EVTX file into XML.")
    parser.add_argument("evtx", type=str,
                        help="Path to the Windows EVTX event log file folder")

    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    main_window.eventTableModel.addColumn("UtcTime")
    main_window.eventTableModel.addColumn("event_id")
    main_window.eventTableModel.addColumn("Image")

    main_window.window.eventTableView.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

    evtxloader = EvtxLoader(args.evtx, main_window)
    threadpool = QThreadPool()
    print("Multithreading with maximum %d threads" % threadpool.maxThreadCount())

    time.sleep(1)
    threadpool.start(evtxloader)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
