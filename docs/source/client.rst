.. currentmodule:: melisa

Melisa Module
=============

Client
-------

.. attributetable:: Client

.. autoclass:: Client
    :exclude-members: listen
    :inherited-members:

    .. automethod:: Client.listen()
        :decorator:


RESTApp
-------

.. attributetable:: RESTApp

.. autoclass:: Client
    :inherited-members:


Event Reference
---------------

This section outlines the different types of events.

To register an listener for an event you can use :meth:`Client.event`.

If an your listener raises an exception, :func:`on_error` will be called
to handle it, which defaults to print a traceback and ignoring the exception.

.. warning::

    Listeners functions must be a **coroutine**. If they aren't, then you might get unexpected
    errors. In order to turn a function into a coroutine they must be ``async def``
    functions.

.. function:: on_error(exception)

    Usually when an event raises an uncaught exception, a traceback is
    printed to stderr and the exception is ignored. If you want to
    change this behaviour and handle the exception for whatever reason
    yourself, this event can be overridden. Which, when done, will
    suppress the default action of printing the traceback.

    .. note::
        It will not be received by :meth:`Client.wait_for`.

    :param exception: Exception.
    :type exception: :class:`Exception`

.. function:: on_channel_create(channel)
.. function:: on_channel_delete(channel)

    Called whenever a guild channel is deleted or created.

    :param channel: The guild channel that got created or deleted.
    :type channel: :class:`models.guild.channel.Channel`

.. function:: on_channel_update(before, after)

    Called whenever a guild channel is updated. e.g. changed name, topic, permissions.

    :param before: The updated guild channel's old info.
    :type before: :class:`models.guild.channel.Channel`
    :param after: The updated guild channel's new info.
    :type after: :class:`models.guild.channel.Channel`

.. function:: on_guild_create(guild)

    Called when a :class:`models.guild.guild.Guild` is either created by the :class:`Client` or when the
    :class:`Client` joins a guild.

    :param guild: The guild that was joined or created.
    :type guild: :class:`models.guild.guild.Guild`

.. function:: on_guild_remove(guild)

    Called when a :class:`models.guild.guild.Guild` is removed from the :class:`Client`.

    This happens through, but not limited to, these circumstances:

    - The client got banned.
    - The client got kicked.
    - The client left the guild.
    - The client or the guild owner deleted the guild.

    In order for this event to be invoked then the :class:`Client` must have
    been part of the guild to begin with.

    :param guild: The guild that got removed.
    :type guild: :class:`models.guild.guild.Guild`

.. function:: on_guild_update(before, after)

    Called when a :class:`models.guild.guild.Guild` updates, for example:

    - Changed name
    - Changed AFK channel
    - Changed AFK timeout
    - etc

    :param before: The guild prior to being updated.
    :type before: :class:`models.guild.guild.Guild`
    :param after: The guild after being updated.
    :type after: :class:`models.guild.guild.Guild`

.. function:: on_message_create(message)

    Called when a :class:`models.message.message.Message` is created and sent.

    .. note::

        Not all messages will have ``content``. This is a Discord limitation.
        See the docs of :attr:`Intents.MESSAGE_CONTENT` for more information.

    :param message: The current message.
    :type message: :class:`models.message.message.Message`

.. function:: on_shard_ready(shard_id)

    Called when particular shard becomes ready.

    :param shard_id: The shard ID that is ready.
    :type shard_id: :class:`int`

