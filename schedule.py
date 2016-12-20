# coding:utf-8

import Colorer
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from service import ProxyService


def job():
    logging.info("schedual job start.")
    service = ProxyService()
    service.refresh()
    logging.info("schedual job end.")


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%d %b %H:%M:%S')

    job() # first crawl
    sched = BlockingScheduler()
    sched.add_job(job, 'interval', hours=24)
    sched.start()

if __name__ == '__main__':
    main()