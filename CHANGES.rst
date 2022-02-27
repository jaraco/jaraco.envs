v2.3.0
======

* #4: Added some tests capturing expectations around
  object types for input (use ``path.Path`` object for
  ``root`` property for maximum compatibility).
* Require Python 3.7 or later.

v2.2.0
======

* VirtualEnv now allows a ``create_opts`` attribute to
  affect the creation (passed to `virtualenv`).

v2.1.1
======

Rely on PEP 420 for namespace packages.

v2.1.0
======

* #1: Rely on pure tox without tox-venv.

v2.0.0
======

* Require Python 3.6 or later.
* Moved release CI to Azure Pipelines.

v1.0.1
======

* Refreshed package metadata.

v1.0.0
======

* Present ``jaraco.envs`` module from adopted from
  ``jaraco.services.envs`` in jaraco.services 2.0.
