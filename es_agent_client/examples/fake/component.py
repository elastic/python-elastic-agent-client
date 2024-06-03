#!/usr/bin/env python3
import sys
import logging

from es_agent_client.util.logger import logger

def main(args=None):
    try:
        run()
    except Exception as e:
        logging.exception(e)
        return 1
    return 0


def run():
    pass


if __name__ == "__main__":
    print("Hello, this is the Fake Component - Py")
    sys.exit(main())
