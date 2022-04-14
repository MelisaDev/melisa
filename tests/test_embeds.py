import datetime

from melisa import Embed, Timestamp

dict_embed = {
    'title': 'my title',
    'description': 'simple description',
    'timestamp': datetime.datetime.utcfromtimestamp(1649748784).isoformat(),
    'footer': {
        'text': 'cool footer text'
    },
    'author': {
        'name': 'best author'
    },
}


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

    def test_comparing_embeds(self):
        embed = Embed(title="my title", description="simple description")
        embed.set_author(name="best author")
        embed.set_footer(text="cool footer text")
        embed.set_timestamp(Timestamp.parse(1649748784))
        assert embed.to_dict() == dict_embed
