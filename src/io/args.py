from typing import Any
import argparse

class Args:
    def __init__(self, configs_filename, report_filepath):
        self.config_path = "data/configs/" + configs_filename
        self.report_path = report_filepath

def parse_args() -> Any:
    parser = argparse.ArgumentParser()
    parser.add_argument('configs_filename', type = str)
    parser.add_argument('report_filepath', type = str)

    args = parser.parse_args()

    config_filename = args.configs_filename
    report_filepath = args.report_filepath

    return Args(config_filename, report_filepath)