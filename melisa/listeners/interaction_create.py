# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from ..models.interactions.interactions import Interaction
from ..utils.types import Coro


async def interaction_create_listener(self, gateway, payload: dict):
    interaction = Interaction.from_dict(payload)

    await self.dispatch("on_interaction_create", (interaction,))

    return


def export() -> Coro:
    return interaction_create_listener
