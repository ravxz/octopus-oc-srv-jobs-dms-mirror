import logging

# additional tricks for logging
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=gunicorn_logger.level)
