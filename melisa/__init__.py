# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from .client import Client, Bot
from .models import *
from .exceptions import *
from .rest import RESTApp
from .cache import CacheManager, AutoCacheModels

__package__ = "melisa"
__title__ = "Melisa"
__description__ = "Cache-configurable module to interact with the Discord API."
__author__ = "MelisaDev"
__license__ = "MIT"
__version__ = '0.0.1a0'

