#!/usr/bin/env python3
import sys
import time

from es_agent_client.util.logger import logger
from es_agent_client.client import VersionInfo, V2Options
from es_agent_client.reader import new_v2_from_reader

FAKE = "fake"


def main(args=None):
    try:
        logger.info("Hello, this is the Fake Component - Py")
        run()
    except Exception as e:
        logger.exception(e)
        return 1
    return 0


def run():
    ver = VersionInfo(
        name=FAKE,
        meta={
            "input": FAKE
        }
    )
    opts = V2Options()
    c = new_v2_from_reader(sys.stdin.buffer, ver, opts)
    logger.info("Don't. Stop me. Nowwwww. Cause we're...")
    while True:
        logger.info("... having a good time")
        time.sleep(10)

    # TODO


if __name__ == "__main__":
    sys.exit(main())
