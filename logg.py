import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename="C:\\incoWatchDog\\service.log",
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


def logg(msg):
    logging.info(msg)

