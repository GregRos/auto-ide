#!/usr/bin/env python3.10
import argparse
from loguru import logger

import sys
from os import chdir
from os.path import dirname
from config import manager

root_parser = argparse.ArgumentParser(description='The automatic IDE picker')
root_parser.add_argument("path", type=str)

if __name__ == '__main__':
    args = root_parser.parse_args()
    logger.info("Received request to open {dir}", dir=args.path)
    launcher = manager.get_ide(args.path)
    if not launcher:
        logger.error("A launcher for this project wasn't found!")
    launcher.launch()
    logger.info("Done!")
