# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from typing import Any

try:
    import orjson
except ModuleNotFoundError:
    import json

    HAS_ORJSON = False
else:
    HAS_ORJSON = True

if HAS_ORJSON:
    def dumps(obj: Any) -> str:
        return orjson.dumps(obj).decode('utf-8')

    loads = orjson.loads
else:
    def dumps(obj: Any) -> str:
        return json.dumps(obj, separators=(',', ':'), ensure_ascii=True)

    loads = json.loads
