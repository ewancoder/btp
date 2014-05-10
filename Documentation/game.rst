BTP main module - game.py
=========================

.. contents::
   :depth: 2

About
-----

This is main game executable file which contains main logics of the game and manipulates with other classes and modules (basically, :mod:`screens` module).

.. automodule:: game

Imports
-------

+----------------+-----------------------------------------------------------+
| :mod:`screens` | For wrapping screens around (see :doc:`screens`)          |
+----------------+-----------------------------------------------------------+
| :mod:`os`      | Determine whether file exists or not                      |
+----------------+-----------------------------------------------------------+
| :mod:`pickle`  | For saving/loading Pers() object (savegame)               |
+----------------+-----------------------------------------------------------+
| :mod:`random`  | For executing battle only if the chance is right          |
+----------------+-----------------------------------------------------------+
| :mod:`pygame`  | As a core of the whole game it is imported in each module |
+----------------+-----------------------------------------------------------+

Data
----

.. autodata:: CAPTION

.. autodata:: SIZE

Classes
-------

Game
~~~~

This is main game class which loops **while true** through :mod:`screens` based on game logics written here.

.. autoclass:: Game
   :members:

Mob
~~~

.. autoclass:: Mob
   :members:

Pers
~~~~

.. autoclass:: Pers
   :members:

:meth:`game.Pers.save` My cool function

Quest
~~~~~

.. autoclass:: Quest
   :members:
