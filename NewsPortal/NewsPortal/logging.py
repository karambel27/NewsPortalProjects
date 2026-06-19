import logging
from django.utils.log import AdminEmailHandler


class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


class MinLevelFilter(logging.Filter):
    def __init__(self, min_level):
        self.min_level = min_level

    def filter(self, record):
        return record.levelno >= self.min_level


class NoTracebackAdminEmailHandler(AdminEmailHandler):
    def emit(self, record):
        record.exc_info = None
        record.exc_text = None
        super().emit(record)