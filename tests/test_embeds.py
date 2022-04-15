import datetime

from melisa import Embed, Timestamp, Color

dict_embed = {
    'title': 'my title',
    'description': 'simple description',
    'color': 252307,
    'timestamp': datetime.datetime.utcfromtimestamp(1649748784).isoformat(),
    'footer': {
        'text': 'cool footer text'
    },
    'author': {
        'name': 'best author'
    },
}

EMBED = Embed(title="my title", description="simple description")
EMBED.set_author(name="best author")
EMBED.set_footer(text="cool footer text")
EMBED.set_color(Color.from_hex_code("#03d993"))
EMBED.set_timestamp(Timestamp.parse(1649748784))


def has_key_vals(actual, required):
    return all(actual.get(key) == val for key, val in required.items())


class TestEmbed:
    def test_total_length_when_embed_is_empty(self):
        embed = Embed()
        assert embed.total_length() == 0

    def test_total_length_when_title_is_none(self):
        embed = Embed(title=None)
        assert embed.total_length() == 0

    def test_total_length_title(self):
        embed = Embed(title="my title")
        assert embed.total_length() == 8

    def test_total_length_when_description_is_none(self):
        embed = Embed(description=None)
        assert embed.total_length() == 0

    def test_total_length_description(self):
        embed = Embed(description="simple description")
        assert embed.total_length() == 18

    def test_total_length_author_name(self):
        embed = Embed().set_author(name="best author")
        assert embed.total_length() == 11

    def test_total_length_footer_text(self):
        embed = Embed().set_footer(text="cool footer text")
        assert embed.total_length() == 16

    def test_total_length_field_value(self):
        embed = Embed().add_field(name="", value="best field value")
        assert embed.total_length() == 16

    def test_total_length_all(self):
        embed = Embed(title="my title", description="simple description")
        embed.set_author(name="best author")
        embed.set_footer(text="cool footer text")
        assert embed.total_length() == 53

    def test_embed_to_dict(self):
        """
        Tests whether or not the dispatch class its string conversion
        is correct.
        """
        assert has_key_vals(EMBED.to_dict(), dict_embed)

    def test_embed_from_dict(self):
        assert has_key_vals(
            Embed.from_dict(dict_embed).to_dict(),
            dict_embed
        )
