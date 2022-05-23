import pytest

from melisa import CacheManager, Snowflake, Guild, TextChannel


class TestCache:
    @pytest.fixture()
    def cache(self, cache_params: dict = None):
        if cache_params is None:
            cache_params = {}

        return CacheManager(**cache_params)

    def test_count(self, cache):
        cache._raw_guilds = {
            Snowflake(123): 123,
            Snowflake(1234): 1111
        }
        cache._raw_users = {
            Snowflake(123): 123,
            Snowflake(1234): 1111
        }
        cache._raw_dm_channels = {
            Snowflake(123): 123,
            Snowflake(1234): 1111
        }
        cache._channel_symlinks = {
            Snowflake(123): 123,
            Snowflake(1234): 1111
        }

        assert cache.guilds_count() == 2
        assert cache.users_count() == 2
        assert cache.guild_channels_count() == 2
        assert cache.total_channels_count() == 4

    def test_set_and_get_guild(self, cache):
        cache.set_guild(
            Guild.from_dict({"id": "123", "name": "test"})
        )

        assert cache.get_guild(123).name == "test"

    def test_set_and_get_guild_channel(self, cache):
        channel = {"id": "456", "name": "test", "type": 0, "guild_id": 123}

        cache.set_guild(
            Guild.from_dict({"id": "123", "name": "test", "channels": [channel]})
        )
        cache.set_guild_channel(
            TextChannel.from_dict(channel)
        )

        assert cache.get_guild_channel(456).name == "test"
