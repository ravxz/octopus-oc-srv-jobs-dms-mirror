import json
from flask import Response, request
from . import dms_mirror_bp
from oc_dms_mirror.dms_mirror import DmsMirror
import logging


def get_dms_mirror():
    _dm = DmsMirror()
    _parser = _dm.basic_args()
    _parser.add_argument("--app-bind", dest="app_bind", type=str, help="<host:port> application binding",
                         default='0.0.0.0:5400')
    _parser.add_argument("--app-timeout", dest="app_timeout", type=str, help="Application response timeout", default=300)
    _parser.add_argument("--app-workers", dest="app_workers", type=int, help="Amount of application workers", default=10)
    _args = _parser.parse_args()

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
    Endpoint performing component/version sync with DMS on demand.
    """
    logging.info(f"POST {request.url_rule.rule} from [{request.remote_addr}]")
    try:
        _component = request.json.get('component')
        _version = request.json.get('version')
        _dmsMirror.process_version(_version, _component)
    except Exception as _e:
        logging.exception(_e)
        return response_json(400, {"result": str(_e)})

    return response_json(200, {"result": "Success"})
