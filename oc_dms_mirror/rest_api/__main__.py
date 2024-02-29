if __name__ == "__main__":
    import argparse
    import logging
    from ..dms_mirror import DmsMirror
    from .application import StandaloneApplication

    _parser = argparse.ArgumentParser(description="Mirror artifacts from DMS to MVN", conflict_handler='resolve')
    DmsMirror().basic_args(_parser)
    _parser.add_argument("--app-bind", dest="app_bind", type=str, help="<host:port> application binding",
                         default='0.0.0.0:5400')
    _parser.add_argument("--app-timeout", dest="app_timeout", type=str, help="Application response timeout", default=300)
    _parser.add_argument("--app-workers", dest="app_workers", type=int, help="Amount of application workers", default=10)
    _args = _parser.parse_args()

    if hasattr(_args, "log_level"):
        logging.basicConfig(
            format="%(pathname)s: %(asctime)-15s: %(levelname)s: %(funcName)s: %(lineno)d: %(message)s",
            level=_args.log_level)
        logging.info(f"Logging level is set to {_args.log_level}")

    _options = {
        "bind": _args.app_bind,
        "timeout": _args.app_timeout,
        "workers": _args.app_workers,
        # "worker_class": "uvicorn.workers.UvicornWorker"
    }
    StandaloneApplication("app", _options, _args).run()
