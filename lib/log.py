import logging
from colored import fg, attr

_log_prefixes = {
    "debug": fg("red") + attr("bold") + "DEBUG" + attr("reset"),
    "info": fg("blue") + attr("bold") + "*" + attr("reset"),
    "success": fg("green") + attr("bold") + "+" + attr("reset"),
    "failure": fg("red") + attr("bold") + "-" + attr("reset"),
    "warning": fg("yellow") + attr("bold") + "!" + attr("reset"),
    "error": fg("red") + "ERROR" + attr("reset"),
    "critical": fg("red") + "CRITICAL" + attr("reset"),
}

_logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(prefix)s] %(message)s")
_logger.setLevel(logging.DEBUG)


def set_level(level):
    _logger.setLevel(level)


def debug(msg):
    _logger.log(
        logging.DEBUG, msg,
        extra={"prefix": _log_prefixes["debug"]}
        )


def info(msg):
    _logger.log(
        logging.INFO, msg,
        extra={"prefix": _log_prefixes["info"]}
        )


def success(msg):
    _logger.log(
        logging.INFO, msg,
        extra={"prefix": _log_prefixes["success"]}
        )


def failure(msg):
    _logger.log(
        logging.INFO, msg,
        extra={"prefix": _log_prefixes["failure"]}
        )


def warning(msg):
    _logger.log(
        logging.WARN, msg,
        extra={"prefix": _log_prefixes["warning"]}
        )


def error(msg):
    _logger.log(
        logging.ERROR, msg,
        extra={"prefix": _log_prefixes["error"]}
        )


def critical(msg):
    _logger.log(
        logging.CRITICAL, msg,
        extra={"prefix": _log_prefixes["critical"]}
        )
