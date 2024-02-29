import json
from flask import Response, request
from . import dms_mirror_bp
from ..dms_mirror import DmsMirror
import logging


def get_dms_mirror():
    _dm = DmsMirror()
    _parser = _dm.basic_args()
    _args = _parser.parse_args()

    if hasattr(_args, "log_level"):
        logging.basicConfig(
            format="%(pathname)s: %(asctime)-15s: %(levelname)s: %(funcName)s: %(lineno)d: %(message)s",
            level=_args.log_level)
        logging.info(_dm.__log_msg(f"Logging level is set to {_args.log_level}"))

    _dm.setup_from_args(_args)
    return _dm


_dmsMirror = get_dms_mirror()


def response_json(code, data):
    """
    Return JSON data response
    :param int code: HTTP response code
    :param data: dict or list to send as response content
    """
    if not isinstance(data, str):
        data = json.dumps(data)

    return Response(
        status=code,
        mimetype='application/json',
        response=data)


@dms_mirror_bp.route('/register-component-version-artifact', methods=['POST'])
def register_component_version_artifact():
    """
    Endpoint returning map of client: lang by given list of clients
    """
    logging.info("POST /register-component-version-artifact from [%s]" % request.remote_addr)
    try:
        _component = request.json.get('component')
        _version = request.json.get('version')
        _dmsMirror.process_version(_version, _component)
    except Exception as _e:
        logging.exception(_e)
        return response_json(400, {"result": str(_e)})

    return response_json(200, {"result": "Success"})
