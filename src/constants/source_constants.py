import os
from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).resolve().parents[2]
LOG_FILE = os.path.join(PROJECT_DIRECTORY, "py_log.log")
SOURCE_FOLDER = os.path.join(PROJECT_DIRECTORY, "source_files")

PAYLOAD_VARIATIONS = [{'deadline': '01.01.2027'},
                      {'deadline': '01.02.2027'},
                      {'deadline': '05.03.2028'},
                      {'deadline': '01.01.2032'},
                      {'deadline': '03.02.2028'},
                      {'deadline': '01.01.2029'},
                      {'deadline': '05.01.2027'}]
