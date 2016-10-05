#!/usr/bin/env python3

from monk.monk import MonkWorker
from monk.log import logger
from handlers import MonkRegister


def main():
    logger.info("Start main worker")
    worker = MonkWorker(MonkRegister())
    worker.run()

if __name__ == "__main__":
    main()
