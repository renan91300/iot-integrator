API
===

This part of the documentation lists the full API reference of all classes and functions.

WSGI
----

.. autoclass:: leds_cibele_api.wsgi.ApplicationLoader
   :members:
   :show-inheritance:

Config
------

.. automodule:: leds_cibele_api.config

.. autoclass:: leds_cibele_api.config.application.Application
   :members:
   :show-inheritance:

.. autoclass:: leds_cibele_api.config.redis.Redis
   :members:
   :show-inheritance:

.. automodule:: leds_cibele_api.config.gunicorn

CLI
---

.. automodule:: leds_cibele_api.cli

.. autofunction:: leds_cibele_api.cli.cli.cli

.. autofunction:: leds_cibele_api.cli.utils.validate_directory

.. autofunction:: leds_cibele_api.cli.serve.serve

App
---

.. automodule:: leds_cibele_api.app

.. autofunction:: leds_cibele_api.app.asgi.on_startup

.. autofunction:: leds_cibele_api.app.asgi.on_shutdown

.. autofunction:: leds_cibele_api.app.asgi.get_application

.. automodule:: leds_cibele_api.app.router

Controllers
~~~~~~~~~~~

.. automodule:: leds_cibele_api.app.controllers

.. autofunction:: leds_cibele_api.app.controllers.ready.readiness_check

Models
~~~~~~

.. automodule:: leds_cibele_api.app.models

Views
~~~~~

.. automodule:: leds_cibele_api.app.views

.. autoclass:: leds_cibele_api.app.views.error.ErrorModel
   :members:
   :show-inheritance:

.. autoclass:: leds_cibele_api.app.views.error.ErrorResponse
   :members:
   :show-inheritance:

Exceptions
~~~~~~~~~~

.. automodule:: leds_cibele_api.app.exceptions

.. autoclass:: leds_cibele_api.app.exceptions.http.HTTPException
   :members:
   :show-inheritance:

.. autofunction:: leds_cibele_api.app.exceptions.http.http_exception_handler

Utils
~~~~~

.. automodule:: leds_cibele_api.app.utils

.. autoclass:: leds_cibele_api.app.utils.aiohttp_client.AiohttpClient
   :members:
   :show-inheritance:

.. autoclass:: leds_cibele_api.app.utils.redis.RedisClient
   :members:
   :show-inheritance:
