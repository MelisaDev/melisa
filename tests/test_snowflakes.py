from melisa.utils import Snowflake


class TestSnowflakes:
    def test_assertions(self):
        assert Snowflake(2) == 2
        assert Snowflake("2") == 2

    def test_timestamps(self):
        sflake = Snowflake(175928847299117063)
        assert sflake.timestamp == 41944705796
        assert sflake.unix == 1462015105796
