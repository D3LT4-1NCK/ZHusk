import sys
import time
import platform
import subprocess


SO = platform.system()


class ZhuskError(Exception):
    """Base exception for all Zhusk library errors."""
    pass
