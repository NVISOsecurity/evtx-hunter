from PySide2.QtCore import QRunnable, Slot
from PySide2.QtGui import QStandardItem
import helpers


class EvtxLoader(QRunnable):
    def __init__(self, file_path, window):
        super().__init__()
        self.window = window
        self.file_path = file_path

    @Slot()  # QtCore.Slot
    def run(self):
        evtx_filenames = helpers.get_recursive_filenames(self.file_path, ".evtx")
        total_events = 0

        for filename in evtx_filenames:
            for xml_event in helpers.get_events(filename):
                json_event = helpers.convert_xml_event_to_json(xml_event)
                total_events += 1

                row_content = dict()

                for k in json_event.keys():

                    if not self.window.fieldListModel.findItems(k):
                        item = QStandardItem(k)
                        item.setCheckable(True)
                        self.window.fieldListModel.appendRow(item)

                if "UtcTime" in json_event.keys():
                    row_content["UtcTime"] = json_event["UtcTime"]
                else:
                    row_content["UtcTime"] = "N/A"

                if "ID" in json_event.keys():
                    row_content["event_id"] = json_event["ID"]
                else:
                    row_content["event_id"] = "N/A"

                if "Image" in json_event.keys():
                    row_content["Image"] = json_event["Image"]
                else:
                    row_content["Image"] = "N/A"

                if "UtcTime" in json_event.keys():
                    self.window.eventTableModel.insertRows(self.window.eventTableModel.rowCount())

                    self.window.eventTableModel.setData(self.window.eventTableModel.index(self.window.eventTableModel.rowCount() - 1, self.window.eventTableModel.column_names.index("event_id")), row_content["event_id"])
                    self.window.eventTableModel.setData(self.window.eventTableModel.index(self.window.eventTableModel.rowCount() - 1, self.window.eventTableModel.column_names.index("UtcTime")), row_content["UtcTime"])
                    self.window.eventTableModel.setData(self.window.eventTableModel.index(self.window.eventTableModel.rowCount() - 1, self.window.eventTableModel.column_names.index("Image")), row_content["Image"])
