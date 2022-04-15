from melisa import Color


rgb_right_example = (3, 217, 147)


class TestColor:
    def test_from_rgb_converting(self):
        assert Color.from_rgb(3, 217, 147).to_rgb() == rgb_right_example

    def test_from_hex_code_converting(self):
        assert Color.from_hex_code("#03d993").to_rgb() == rgb_right_example

    def test_from_decimal_converting(self):
        assert Color(252307).to_rgb() == rgb_right_example
