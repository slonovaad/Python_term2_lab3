import os
from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).resolve().parents[2]
LOG_FILE = os.path.join(PROJECT_DIRECTORY, "py_log.log")
SOURCE_FOLDER = os.path.join(PROJECT_DIRECTORY, "source_files")

PAYLOAD_VARIATIONS = [{'deadline': '2027-01-01', 'priority': '1'},
                      {'deadline': '2027-02-01', 'priority': '2'},
                      {'deadline': '2028-05-03', 'priority': '5'},
                      {'deadline': '2032-01-01', 'priority': '3'},
                      {'deadline': '2028-03-02', 'priority': '1'},
                      {'deadline': '2029-01-01', 'priority': '1'},
                      {'deadline': '2027-05-01', 'priority': '2'}]
