# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from typing import List, Union, Optional, Dict, Any

from .colors import Color
from melisa.exceptions import EmbedFieldError
from ...utils.conversion import try_enum
from ...utils.api_model import APIModelBase
from ...utils.types import APINullable, UNDEFINED
from melisa.utils.timestamp import Timestamp


class EmbedType(Enum):
    """
    Embed types are "loosely defined" and, for the most part,
    are not used by our clients for rendering.
    Embed attributes power what is rendered.
    Embed types should be considered deprecated and might be removed in a future API version.

    Attributes
    __________
    RICH:
        Generic embed rendered from embed attributes
    IMAGE
        Image embed
    VIDEO
        Video embed
    GIFV
        Animated gif image embed rendered as a video embed
    ARTICLE
        Article embed
    LINK
        Link embed
    """

    RICH = "rich"
    IMAGE = "image"
    VIDEO = "video"
    GIFV = "gifv"
    ARTICLE = "article"
    LINK = "link"


@dataclass(repr=False)
class EmbedThumbnail:
    """Representation of the Embed Thumbnail

    Attributes
    ----------
    url: :class:`str`
        Source url of the thumbnail
    proxy_url: Optional[:class:`str`]
        A proxied url of the thumbnail
    height: Optional[:class:`int`]
        Height of the thumbnail
    width: Optional[:class:`int`]
        Width of the thumbnail
    """

    url: str
    proxy_url: APINullable[str] = None
    height: APINullable[int] = None
    width: APINullable[int] = None


@dataclass(repr=False)
class EmbedVideo:
    """Representation of the Embed Video

    Attributes
    ----------
    url: Optional[:class:`str`]
        Source url of the video
    proxy_url: Optional[:class:`str`]
        A proxied url of the video
    height: Optional[:class:`int`]
        Height of the video
    width: Optional[:class:`int`]
        Width of the video
    """

    url: str
    proxy_url: APINullable[str] = None
    height: APINullable[int] = None
    width: APINullable[int] = None


@dataclass(repr=False)
class EmbedImage:
    """Representation of the Embed Image

    Attributes
    ----------
    url: :class:`str`
        Source url of image (only supports http(s) and attachments)
    proxy_url: Optional[:class:`str`]
        A proxied url of the image
    height: Optional[:class:`int`]
        Height of the image
    width: Optional[:class:`int`]
        Width of the image
    """

    url: str
    proxy_url: APINullable[str] = None
    height: APINullable[int] = None
    width: APINullable[int] = None


@dataclass(repr=False)
class EmbedProvider:
    """Representation of the Embed Provider

    Attributes
    ----------
    name: Optional[:class:`str`]
        Name of provider
    url: Optional[:class:`str`]
        Url of provider
    """

    name: APINullable[str] = None
    url: APINullable[str] = None


@dataclass(repr=False)
class EmbedAuthor:
    """Representation of the Embed Author

    Attributes
    ----------
    name: :class:`str`
        Name of author
    url: Optional[:class:`str`]
        Url of author
    icon_url: Optional[:class:`str`]
        Url of author icon (only supports http(s) and attachments)
    proxy_icon_url: Optional[:class:`str`]
        A proxied url of author icon
    """

    name: str
    url: APINullable[str] = None
    icon_url: APINullable[str] = None
    proxy_icon_url: APINullable[str] = None


@dataclass(repr=False)
class EmbedFooter:
    """Representation of the Embed Footer

    Attributes
    ----------
    text: :class:`str`
        Footer text
    icon_url: Optional[:class:`str`]
        Url of footer icon (only supports http(s) and attachments)
    proxy_icon_url: Optional[:class:`str`]
        A proxied url of footer icon
    """

    text: str
    icon_url: APINullable[str] = None
    proxy_icon_url: APINullable[str] = None


@dataclass(repr=False)
class EmbedField:
    """Representation of the Embed Field

    Attributes
    ----------
    name: :class:`str`
        Name of the field
    value: :class:`str`
        Value of the field
    inline: Optional[:class:`bool`]
        Whether or not this field should display inline
    """

    name: str
    value: str
    inline: Optional[bool] = False


@dataclass(repr=False)
class Embed(APIModelBase):
    """Represents an embed sent in with message within Discord.

    Attributes
    ----------

    title: Optional[:class:`str`]
        Title of embed
    type: Optional[:class:`~melisa.models.message.embed.EmbedType`]
        Type of embed (always "rich" for webhook embeds)
    description: Optional[:class:`str`]
        Description of embed
    color: Optional[:class:`int`]
        Color code of the embed.
        If you really want to do something with a color,
        feel free to convert it to the ``Color``: ::

            color = Color(embed.color)

    fields: Optional[List[:class:`~melisa.models.message.embed.EmbedField`]]
        Fields information.
    footer: Optional[:class:`~melisa.models.message.embed.EmbedFooter`]
        Footer information.
    image: Optional[:class:`~melisa.models.message.embed.EmbedImage`]
        Image information.
    provider: Optional[:class:`~melisa.models.message.embed.EmbedProvider`]
        Provider information.
    thumbnail: Optional[:class:`~melisa.models.message.embed.EmbedThumbnail`]
        Thumbnail information.
    timestamp: Optional[:class:`~melisa.utils.timestamp.Timestamp`]
        Timestamp of embed content
    url: Optional[:class:`str`]
        Url of embed
    video: Optional[:class:`~melisa.models.message.embed.EmbedVideo`]
        Video information.
    """

    title: APINullable[str] = None
    type: APINullable[EmbedType] = None
    description: APINullable[str] = None
    url: APINullable[str] = None
    timestamp: APINullable[Timestamp] = None
    color: APINullable[Color] = None
    footer: APINullable[EmbedFooter] = None
    image: APINullable[EmbedImage] = None
    thumbnail: APINullable[EmbedThumbnail] = None
    video: APINullable[EmbedVideo] = None
    provider: APINullable[EmbedProvider] = None
    author: APINullable[EmbedAuthor] = None
    fields: APINullable[List[EmbedField]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Generate a message from the given data.

        Parameters
        ----------
        data: :class:`dict`
            The dictionary to convert into an unknown channel.
        """
        self: Embed = super().__new__(cls)

        self.title = data.get("title")
        self.type = (
            try_enum(EmbedType, data["type"]) if data.get("type") is not None else None
        )
        self.description = data.get("description")
        self.url = data.get("url")
        self.timestamp = (
            Timestamp.parse(data["timestamp"])
            if data.get("timestamp") is not None
            else None
        )
        self.color = Color(data["color"]) if data.get("color") is not None else None

        self.footer = None
        self.image = None
        self.thumbnail = None
        self.video = None
        self.provider = None
        self.author = None
        self.fields = []

        if data.get("footer") is not None:
            self.footer = EmbedFooter(
                text=data["footer"]["text"],
                icon_url=data["footer"].get("icon_url"),
                proxy_icon_url=data["footer"].get("proxy_icon_url"),
            )

        if data.get("image") is not None:
            self.image = EmbedImage(
                url=data["image"]["url"],
                proxy_url=data["image"].get("proxy_url"),
                height=data["image"].get("height"),
                width=data["image"].get("width"),
            )

        if data.get("video") is not None:
            self.video = EmbedVideo(
                url=data["video"]["url"],
                proxy_url=data["video"].get("proxy_url"),
                height=data["video"].get("height"),
                width=data["video"].get("width"),
            )

        if data.get("provider") is not None:
            self.provider = EmbedProvider(
                name=data["provider"].get("name"), url=data["provider"].get("url")
            )

        if data.get("author") is not None:
            self.author = EmbedAuthor(
                name=data["author"]["name"],
                url=data["author"].get("url"),
                icon_url=data["author"].get("icon_url"),
                proxy_icon_url=data["author"].get("proxy_icon_url"),
            )

        if data.get("fields") is not None:
            for field in data["fields"]:
                self.fields.append(
                    EmbedField(
                        name=field["name"],
                        value=field["value"],
                        inline=field["inline"]
                        if field.get("inline") is not None
                        else False,
                    )
                )

        return self

    def __post_init__(self):
        if self.title and len(self.title) > 256:
            raise EmbedFieldError.characters_from_desc(
                "Embed Title",
                len(self.title),
                256,
            )

        if self.description and len(self.description) > 4096:
            raise EmbedFieldError.characters_from_desc(
                "Embed Description", len(self.description), 4096
            )

        if self.fields and len(self.fields) > 25:
            raise EmbedFieldError("""You can't set more than 25 embed fields!""")

    def set_color(self, color: Union[int, Color]) -> Embed:
        """Sets color in the supported by discord format.

        Parameters
        ----------
        color: Union[:class:`~melisa.models.message.color.Color`, :class:`int`]
            The datetime to set the timestamp to.

        Returns
        -------
        :class:`~melisa.models.message.embed.Embed`
            The new embed object.
        """
        if isinstance(color, Color):
            self.color = color.value
        elif isinstance(color, int):
            self.color = Color(value=color).value

        return self

    def set_timestamp(self, time: datetime) -> Embed:
        """Sets timestamp in the supported by discord format.

        Parameters
        ----------
        time: :class:`~melisa.utils.timestamp.Timestamp`
            The datetime to set the timestamp to.

        Returns
        -------
        :class:`~melisa.models.message.embed.Embed`
            The new embed object.
        """
        self.timestamp = time.isoformat()

        return self

    def set_author(
        self,
        name: str,
        *,
        url: Optional[str] = UNDEFINED,
        icon_url: Optional[str] = UNDEFINED,
        proxy_icon_url: Optional[str] = UNDEFINED,
    ) -> Embed:
        """Set the author for the embed.

        Parameters
        ----------
        name: :class:`str`
            Name of author
        url: Optional[:class:`str`]
            Url of author icon (only supports http(s) and attachments)
        icon_url: Optional[:class:`str`]
            Url of author
        proxy_icon_url: Optional[:class:`str`]
            A proxied url of author icon
        Returns
        -------
        :class:`~melisa.models.message.embed.Embed`
            Updated embed.
        """

        self.author = EmbedAuthor(
            name=name,
            url=url,
            icon_url=icon_url,
            proxy_icon_url=proxy_icon_url,
        )

        return self

    def set_image(self, url: str, *, proxy_url: APINullable[str] = UNDEFINED) -> Embed:
        """Set the image for the embed.

        Parameters
        ----------
        url: :class:`str`
            Source url of image (only supports http(s) and attachments)
        proxy_url: Optional[:class:`str`]
            A proxied url of the image
        Returns
        -------
        :class:`~melisa.models.message.embed.Embed`
            Updated embed.
        """

        self.image = EmbedImage(url=url, proxy_url=proxy_url)

        return self

    def set_thumbnail(
        self, url: str, *, proxy_url: APINullable[str] = UNDEFINED
    ) -> Embed:
        """Set the thumbnail for the embed.

        Parameters
        ----------
        url: :class:`str`
            Source url of thumbnail (only supports http(s) and attachments)
        proxy_url: Optional[:class:`str`]
            A proxied url of the thumbnail
        Returns
        -------
        :class:`~melisa.models.message.embed.Embed`
            Updated embed.
        """

        self.thumbnail = EmbedThumbnail(url=url, proxy_url=proxy_url)

        return self

    def set_footer(
        self,
        text: str,
        *,
        icon_url: APINullable[str] = UNDEFINED,
        proxy_icon_url: APINullable[str] = UNDEFINED,
    ) -> Embed:
        """
        Sets the embed footer.

        Parameters
        ----------
        text: :class:`str`
            Footer text
        icon_url: Optional[:class:`str`]
            Url of footer icon (only supports http(s) and attachments)
        proxy_icon_url: Optional[:class:`str`]
            A proxied url of footer icon

        Returns
        -------
        :class:`~melisa.models.message.embed.Embed`
            Updated embed.
        """
        self.footer = EmbedFooter(
            text=text, icon_url=icon_url, proxy_icon_url=proxy_icon_url
        )

        return self

    def add_field(self, name: str, value: str, *, inline: bool = False):
        """
        Adds a field to the embed object.

        This function returns the class instance to allow for fluent-style chaining.

        Parameters
        ----------
        name: :class:`str`
            The name of the field.
        value: :class:`str`
            The value of the field.
        inline: :class:`bool`
            Whether the field should be displayed inline.

        Returns
        -------
        Embed
            This embed.
        """

        if self.fields is None:
            self.fields = []

        self.fields.append(EmbedField(name=name, value=value, inline=inline))

        return self

    def edit_field(
        self,
        index: int,
        *,
        name: APINullable[str] = UNDEFINED,
        value: APINullable[str] = UNDEFINED,
        inline: APINullable[bool] = UNDEFINED,
    ) -> Embed:
        """Edit an existing field on this embed.

        Parameters
        ----------
        index: :class:`int`
            The index of the field to edit.
        name: Optional[:class:`str`]
            The name of the field.
        value: Optional[:class:`str`]
            The value of the field.
        inline: Optional[:class:`bool`]
            Whether the field should be displayed inline.

        Returns
        -------
        Embed
            This embed.

        Raises
        ------
        :class:`IndexError`
            Raised if the index is greater than `len(embed.fields) - 1` or
            less than `-len(embed.fields)`
        """
        if not self.fields:
            raise IndexError(index)

        field = self.fields[index]

        if name is not UNDEFINED:
            field.name = name
        if value is not UNDEFINED:
            field.value = value
        if inline is not UNDEFINED:
            field.is_inline = inline

        return self

    def remove_field(self, index: int) -> Embed:
        """Remove an existing field from this embed.

        Parameters
        ----------
        index: :class:`int`
            The index of the embed field to remove.

        Returns
        -------
        Embed
            This embed.

        Raises
        ------
        :class:`IndexError`
            Raised if the index is greater than `len(embed.fields) - 1` or
            less than `-len(embed.fields)`
        """
        if self.fields:
            del self.fields[index]

        if not self.fields:
            self.fields = UNDEFINED

        return self

    def clear_fields(self) -> Embed:
        """Removes all fields from this embed."""
        self.fields.clear()

        return self

    def total_length(self) -> int:
        """Get the total character count of the embed.

        Returns
        -------
        :class:`int`
            The total character count of this embed, including title, description,
            fields, footer, and author combined.
        """
        total = len(self.title or "") + len(self.description or "")

        if self.fields:
            for field in self.fields:
                total += len(field.name) + len(field.value)

        if self.footer and self.footer.text:
            total += len(self.footer.text)

        if self.author and self.author.name:
            total += len(self.author.name)

        return total
