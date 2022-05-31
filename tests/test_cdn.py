from melisa import CDNBuilder

cdn = CDNBuilder("png")


class TestCDN:
    def test_avatar_url(self):
        assert (
            cdn.avatar_url("585766846268047370", "52320b1f9ddb1d7546da7b973bc23d6d")
            == "https://cdn.discordapp.com/avatars/585766846268047370/52320b1f9ddb1d7546da7b973bc23d6d.png?size=1024"
        )

    def test_default_avatar_url(self):
        assert (
            cdn.default_avatar_url("0575")
            == "https://cdn.discordapp.com/embed/avatars/0.png"
        )

    def test_guild_icon_url(self):
        assert (
            cdn.guild_icon_url(
                "951867868188934216",
                "5ef33b1f6c4b35f19b605c51c5a64469",
                image_format="webp",
            )
            == "https://cdn.discordapp.com/icons/951867868188934216/5ef33b1f6c4b35f19b605c51c5a64469.webp?size=1024"
        )
