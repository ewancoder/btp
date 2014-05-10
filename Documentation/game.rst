BTP main module - game.py
*************************

.. contents::
   :depth: 2

About
=====

This is main game executable file which contains main logics of the game and manipulates other modules and classes (basically, :mod:`screens` module).

.. automodule:: game

At first, we set :const:`game.CAPTION` and :const:`game.SIZE` constants, which is responsible for main window title and size respectively.

.. literalinclude:: ../game.py
   :start-after: CONSTANTS
   :end-before: CLASSES

.. note::
   Size of the window must be smaller or at least the same as any image used as background, otherwise the image won't cover all screen and there will be black areas.

Then we create new pygame window using those constants.

.. literalinclude:: ../game.py
   :start-after: MAIN PROGRAM

Last two lines are basically creation of main game class :class:`game.Game` and a proper pygame quit. The :class:`game.Game` class is looping through whole lots of game logics **while True**, so it's okay that we're quiting our game right after :class:`game.Game` creation.

.. note::
   The ``__name__ == '__main__'`` thing is basically checking whether we're running our game standalone way (form console, as executable, etc.) or we're importing it. Even though I'm not intended to import it and you're should not too, it's proper way to protect your project from undesired execution.

Imports
=======

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

Classes
=======

Game
----

This is the main logics class which rules the game **while true** through :mod:`screens` module.

.. autoclass:: Game
   :members:

We have only one method here and nothing else - :meth:`game.Game.loop`. So, basically, we don't need a class - we can easily make it a function or even write all the code within ``__name__ == '__main__'`` condition, but I like OOP concepts and I like extensibility of classes and object. So for now it will stand a class, but when the stable *1.0* version is out - we'll see.

.. todo::
   Make something about attr -> param linking support

Our :meth:`game.Game.loop` method have only one attribute - :attr:`game.Game.loop.surface` which is the screen area for drawing all the stuff.

At first, we set some variables:

.. literalinclude:: ../game.py
   :start-after: VARIABLES
   :end-before: MAIN

* :data:`game.Game.loop.pers` - our :class:`game.Pers` object to work with. All the data about your character is stored within it. Your hitpoints, your current location and etc.
* :data:`game.Game.loop.started` - boolean which tells us whether game is already loaded or is it should yet be loaded/created.

Then goes main cycle which loops **while True**.

.. literalinclude:: ../game.py
   :start-after: MAIN LOOP
   :end-before: MAIN PROGRAM

Here we create menu using class :class:`screens.Menu` and it's method :meth:`screens.Menu.main`. When 'New game / load game' option is selected, menu returns something (not important what) into the local ``login`` variable which, if not empty, will load :meth:`screens.Login.main` method from :class:`screens.Login`.

Well, the login screen will return a name when it is entered to login screen and Enter is pressed. The name will be stored in :data:`game.Pers.name` variable and then whole cycle will stop working. Because :data:`game.Pers.name` won't be empty anymore.

The next step is to save game and start intro or to load game if user entered the name which already exists in Saves folder. Here we're using :mod:`os` module to check whether savegame exists or not.

If it exists, we use :meth:`game.Pers.load` method which loads whole object data by means of :mod:`pickle`. If it isn't, firstly we're saving whole object data to the file and then we're executing :meth:`screens.World.main` method form :class:`screens.World` class, which is intended to tell user some pre-history of game world and give hime base knowledge of what he'll be waiting within the game.

After that, the variable :data:`game.Game.loop.started` sets to True and this part of code never repeats too.

Next step is finally the world loading. Class :class:`screens.World` is showing world until any action was performed. When an action was performed, :class:`screens.World` returns next place to :data:`game.Pers.place` and mobs record for new place to local variable ``mobs``.

There's our :mod:`random` module comes in handy: we're using it to calculate chances that we're in trouble and monsters are attacking.

Then we're saving a game (after successful battle) and all begins again

.. note::
   There will be lots more logics added to calculate, it's early development stage of the game. In the future, you'll be able to 'cleanse' locations so that mobs you've killed won't attack you again or even will respawn after some time. Now, however, if you'll kill any monsters (hah, battle is not yet ready) and you'll try to load the game - they can attack you again.

Mob
---

There's not much done yet about this class. It's here just for an example of what will be done soon.

.. autoclass:: Mob
   :members:

Source code:

.. literalinclude:: ../game.py
   :start-after: Creates new monster
   :end-before: class Quest

Pers
----

Handles all Player data.

.. autoclass:: Pers
   :members:

Source code:

.. literalinclude:: ../game.py
   :start-after: class Pers
   :end-before: class Game

Quest
-----

This class will contain lots of tasks, jounral, other things to handle all the quests system and other logic. Yet it is far not done.

.. autoclass:: Quest
   :members:

Source code:

.. literalinclude:: ../game.py
   :start-after: class Quest
   :end-before: class Pers
