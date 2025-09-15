import logging
from typing import Optional, Dict


class ErpAdapterLogger:

    def __init__(self, name: str = 'ErpAdapter', level: int = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def _log(self, level: int, data: str, json_response: Optional[Dict]):
        extra_data = {'json_response': json_response}
        self.logger.log(level, data, extra=extra_data)

    def info(self, data: str, json_response: Optional[Dict] = None):
        self._log(logging.INFO, data, json_response)

    def error(self, data: str, json_response: Optional[Dict] = None):
        self._log(logging.ERROR, data, json_response)


    def exception(self, data: str, json_response: Optional[Dict] = None):
        extra_data = {'json_response': json_response}
        self.logger.exception(data, extra=extra_data)

    def warning(self, data: str, json_response: Optional[Dict] = None):
        """Logs a warning message with an optional JSON payload."""
        self.logger.warning(data, extra={'json_response': json_response})

