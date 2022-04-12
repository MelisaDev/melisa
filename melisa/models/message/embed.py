# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from typing import List, Union, Optional

from melisa.exceptions import EmbedFieldError
from melisa.utils.api_model import APIModelBase, APINullable
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
class EmbedThumbnail(APIModelBase):
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
class EmbedVideo(APIModelBase):
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
class EmbedImage(APIModelBase):
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
class EmbedProvider(APIModelBase):
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
class EmbedAuthor(APIModelBase):
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
class EmbedFooter(APIModelBase):
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
class EmbedField(APIModelBase):
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
    inline: APINullable[str] = None


@dataclass(repr=False)
class Embed(APIModelBase):
    # ToDo: Add fields set method

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
        Color code of the embed
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
    color: APINullable[int] = None
    footer: APINullable[EmbedFooter] = None
    image: APINullable[EmbedImage] = None
    thumbnail: APINullable[EmbedThumbnail] = None
    video: APINullable[EmbedVideo] = None
    provider: APINullable[EmbedProvider] = None
    author: APINullable[EmbedAuthor] = None
    fields: APINullable[List[EmbedField]] = None

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

    def set_timestamp(self, time: Union[Timestamp, datetime]) -> Embed:
        """Sets timestamp in the supported by discord format.

        Parameters
        ----------
        time: :class:`~melisa.utils.timestamp.Timestamp`
            The datetime to set the timestamp to.

        Returns
        -------
        :class:`~,e;osa.models.message.embed.Embed`
            The new embed object.
        """
        self.timestamp = time.isoformat()

        return self

    def set_author(
        self,
        name: str,
        *,
        url: Optional[str] = None,
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
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

    def set_image(self, url: str, *, proxy_url: Optional[str] = None) -> Embed:
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

    def set_thumbnail(self, url: str, *, proxy_url: Optional[str] = None) -> Embed:
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
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
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
