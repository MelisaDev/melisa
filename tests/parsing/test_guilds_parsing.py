from melisa.models import Guild

guild_data = {
    "id": "197038439483310086",
    "name": "Discord Testers",
    "icon": "f64c482b807da4f539cff778d174971c",
    "description": "The official place to report Discord Bugs!",
    "splash": None,
    "discovery_splash": None,
    "features": [
        "ANIMATED_ICON",
        "VERIFIED",
        "NEWS",
        "VANITY_URL",
        "DISCOVERABLE",
        "MORE_EMOJI",
        "INVITE_SPLASH",
        "BANNER",
        "COMMUNITY"
    ],
    "emojis": [],
    "banner": "9b6439a7de04f1d26af92f84ac9e1e4a",
    "owner_id": "73193882359173120",
    "application_id": None,
    "region": None,
    "afk_channel_id": None,
    "afk_timeout": 300,
    "system_channel_id": None,
    "widget_enabled": None,
    "widget_channel_id": None,
    "verification_level": 3,
    "roles": [],
    "default_message_notifications": 1,
    "mfa_level": 1,
    "explicit_content_filter": 2,
    "max_presences": 40000,
    "max_members": 250000,
    "vanity_url_code": "discord-testers",
    "premium_tier": 3,
    "premium_subscription_count": 33,
    "system_channel_flags": 0,
    "preferred_locale": "en-US",
    "rules_channel_id": "441688182833020939",
    "public_updates_channel_id": "281283303326089216"
}

parsed_model = Guild.from_dict(guild_data)


class TestGuildParsing:
    def test_dict_to_model(self):
        assert int(parsed_model.id) == 197038439483310086
        assert parsed_model.name == "Discord Testers"
        assert parsed_model.features == [
            "ANIMATED_ICON",
            "VERIFIED",
            "NEWS",
            "VANITY_URL",
            "DISCOVERABLE",
            "MORE_EMOJI",
            "INVITE_SPLASH",
            "BANNER",
            "COMMUNITY"
        ]
