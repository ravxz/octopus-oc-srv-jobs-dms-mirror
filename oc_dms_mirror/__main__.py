if __name__ == "__main__":
    import argparse
    _parser = argparse.ArgumentParser(description="Mirror artifacts from DMS to MVN", conflict_handler='resolve')
    # _parser.add_argument("--app-start", dest="app_start", type=bool, help="Start application", default=False)
    _parser.add_argument("--app-start", dest="app_start", action='store_true', help="Start application")
    _parser.add_argument("--app-bind", dest="app_bind", type=str, help="<host:port> application binding",
                         default='0.0.0.0:5400')
    _parser.add_argument("--app-timeout", dest="app_timeout", type=str, help="Application response timeout", default=300)
    _parser.add_argument("--app-workers", dest="app_workers", type=int, help="Amount of application workers", default=10)
    _parser.set_defaults(feature=True)

    _args = _parser.parse_args()
    if _args.app_start:
        from .application import StandaloneApplication
        _options = {
            "bind": _args.app_bind,
            "timeout": _args.app_timeout,
            "workers": _args.app_workers,
            "worker_class": "uvicorn.workers.UvicornWorker"
        }
        StandaloneApplication("oc_dms_mirror.wsgi:app", _options).run()
    else:
        from .dms_mirror import DmsMirror
        DmsMirror().main()
