from __future__ import annotations

from ..utils.types import Coro
from ..models.user import User


async def on_ready_listener(self, gateway, payload: dict):
    gateway.session_id = payload.get("session_id")

    guilds = payload.get("guilds")

    self.guilds = dict(map(lambda i: (i["id"], None), guilds))
    self.user = User.from_dict(payload.get("user"))

    custom_listener = self._events.get("on_ready")

    if custom_listener is not None:
        await custom_listener()

    return


def export() -> Coro:
    return on_ready_listener
