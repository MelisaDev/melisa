<p align="center">
  <b>
    The easiest way to create your own <strong>optimized</strong> Discord Bot. 
  </b>
</p>

<hr>

<a class="github-badge" href="https://melisa.readthedocs.io/en/latest/?badge=latest" tabindex="-1">
<img src="https://readthedocs.org/projects/melisa/badge/?version=latest" alt="Documentation Status"/>
</a>
<a class="github-badge" href="https://github.com/MelisaDev/melisa" tabindex="-1">
<img src="https://img.shields.io/github/repo-size/MelisaDev/melisa" alt="Repo Size"/>
</a>
<a class="github-badge" href="https://github.com/MelisaDev/melisa" tabindex="-1">
<img src="https://img.shields.io/github/last-commit/MelisaDev/melisa" alt="GitHub last commit"/>
</a>
<a class="github-badge" href="https://github.com/MelisaDev/melisa" tabindex="-1">
<img src="https://img.shields.io/github/commit-activity/m/MelisaDev/melisa?label=commits" alt="GitHub commit activity"/>
</a>
<a class="github-badge" href="https://discord.gg/QX4EG8f7aD" tabindex="-1">
<img src="https://img.shields.io/discord/951867868188934216" alt="Discord"/>
</a>

<hr>

<h2 align="center">
THIS LIBRARY IS CURRENTLY UNDER DEVELOPMENT!
</h2>

<h3 align="center">Every provided example or a feature is not ready or may be changed in the future</h3>

## About
<strong>MelisaPy</strong> is a Discord microframework for Python 3 
for the [Discord API](https://discord.com/developers/docs/intro). 

It supports Discord V10 REST API and Gateway

We are trying to make our library optimized. 
We are going to create really cool cache configuration, so don't worry about the RAM :)

---
## Install MelisaPy

```commandline
pip install melisa
```
Or, alternatively:
```commandline
pip install git+https://github.com/MelisaDev/melisa
```

---

## Events Listening

```python
import melisa

client = melisa.Client("your cool token...")

@client.listen
async def on_message_create(message):
    if message.content.startswith('$greet'):
        await message.channel.send(f'Hello man!')

client.run_autosharded()
```

Also, we should tell you, that logging is enabled automatically (evil laugh).
But do not worry, only some important things will be logged, but it can be disabled or changed.

If you wish to specify some intents, you should do it something like that:

```python
import melisa

client = melisa.Client("your cool token...",
                       intents=[
                           melisa.Intents.GUILD_MEMBERS,
                           melisa.Intents.GUILD_BANS
                       ])
```

Or you can do something like this:

```python
import melisa

intents = melisa.Intents.all() - melisa.Intents.GUILD_PRESENCES

client = melisa.Client("your cool token...",
                       intents=intents)
```

Also sharding is fully supported in Melisa, but it is too long to write about it here,
so feel free to read our docs!

---

## Making your bot more efficient

### Python optimization flags
You can specify some optimization flags in CPython interpreter

1. `python bot.py` - no optimization
2. `python -O bot.py` - features such as internal assertions will be disabled.
3. `python -OO bot.py` - more features (including all docstrings) will be removed from the loaded code at runtime.

### `melisa[speed]`
Also you can speed up some features in Melisa, like json parsing. 
It will install `orjson`.

---

## Want to help us?

Contributing manual is not ready yet, but will be done in some days.
Feel free to us in [our Discord Server](https://discord.gg/QX4EG8f7aD) about contributing to the Melisa.

