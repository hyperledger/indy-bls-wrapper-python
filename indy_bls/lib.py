"""Raw library bindings."""

import json
import os.path
import logging
import sys

from ctypes import CDLL, CFUNCTYPE, byref, c_char_p, c_int32, c_void_p
from ctypes.util import find_library
from enum import IntEnum
from logging import ERROR, WARNING, INFO, DEBUG

from .error import IndyBlsError

LOGGER = logging.getLogger()
TRACE = 5


class ErrorCode(IntEnum):
    """Error code as returned by FFI methods."""

    Success = 0
    Fail = 1


def do_call(name, *args):
    """Perform an FFI method call."""
    # LOGGER.debug("do_call: >>> name: %r, args: %r", name, args)

    lib = _cdll()
    err = getattr(lib, name)(*args)

    if err != ErrorCode.Success:
        LOGGER.debug("do_call: Function %r returned err: %r", name, err)
        err_msg = c_char_p()
        lib.indy_bls_get_current_error(byref(err_msg))
        err_json = err_msg.value.decode("utf-8")
        lib.indy_bls_string_free(err_msg)
        raise IndyBlsError(json.loads(err_json)["message"])


def _cdll():
    if not hasattr(_cdll, "cdll"):
        _cdll.cdll = _load_cdll()
        _set_logger()

    return _cdll.cdll


def _load_cdll() -> CDLL:
    LOGGER.debug("_load_cdll: >>>")

    lib_name = "indy_blssignatures"
    lib_prefix_mapping = {"darwin": "lib", "linux": "lib", "linux2": "lib", "win32": ""}
    lib_suffix_mapping = {
        "darwin": ".dylib",
        "linux": ".so",
        "linux2": ".so",
        "win32": ".dll",
    }

    os_name = sys.platform
    LOGGER.debug("_load_cdll: Detected OS name: %s", os_name)

    try:
        lib_prefix = lib_prefix_mapping[os_name]
        lib_suffix = lib_suffix_mapping[os_name]
    except KeyError:
        LOGGER.error("_load_cdll: OS isn't supported: %s", os_name)
        raise IndyBlsError("OS isn't supported: %s", os_name)

    lib_filename = f"{lib_prefix}{lib_name}{lib_suffix}"
    LOGGER.debug("_load_cdll: Resolved library name is: %s", lib_filename)

    try:
        lib_path = os.path.join(os.path.dirname(__file__), lib_filename)
        res = CDLL(lib_path)
        LOGGER.debug("_load_cdll: <<< res: %s", res)
        return res
    except OSError:
        LOGGER.warning("Library not loaded from python package")

    lib_path = find_library(lib_name)
    if not lib_path:
        raise IndyBlsError(f"Library not found in path: {lib_name}")
    try:
        res = CDLL(lib_path)
    except OSError as e:
        LOGGER.error("_load_cdll: Can't load %s: %s", lib_name, e)
        raise IndyBlsError(f"Error loading library: {lib_path}") from e

    return res


def _set_logger():
    logging.addLevelName(TRACE, "TRACE")

    LOGGER.debug("set_logger: >>>")

    def _log(context, level, target, message, module_path, file, line):
        lib_logger = LOGGER.getChild("native." + target.decode().replace("::", "."))

        level_mapping = {
            1: ERROR,
            2: WARNING,
            3: INFO,
            4: DEBUG,
            5: TRACE,
        }

        lib_logger.log(
            level_mapping[level], "\t%s:%d | %s", file.decode(), line, message.decode()
        )

    _set_logger.callbacks = {
        "log_cb": CFUNCTYPE(
            None, c_void_p, c_int32, c_char_p, c_char_p, c_char_p, c_char_p, c_int32
        )(_log),
        "enabled_cb": c_void_p(),
        "flush_cb": c_void_p(),
    }

    do_call(
        "indy_bls_set_custom_logger",
        c_void_p(),
        _set_logger.callbacks["log_cb"],
        _set_logger.callbacks["enabled_cb"],
        _set_logger.callbacks["flush_cb"],
        c_int32(TRACE),
    )

    LOGGER.debug("set_logger: <<<")
