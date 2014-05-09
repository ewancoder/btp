User Guide
**********

.. contents::
   :depth: 2

.. _quickstart:

Getting Started
===============

Welcome, brave sir User. I see, you wanna play. Here are quick and simple instructions to start playing:

How to get it
-------------

First, you need to get the game and packages it relies upon. You need 3 things:

#. `Python package <http://www.python.org/downloads>`_. Download whether 2 or 3 version, it's not crucial, yet I am using 3rt and most newest, bleeding edge version.
#. `PyGame package <http://www.pygame.org/download.shtml>`_. Download lastest available version for your OS.
#. The game itself:

  * `Stable version <https://github.com/ewancoder/btp/archive/master.zip>`_
  * `Development version <https://github.com/ewancoder/btp/archive/dev.zip>`_

.. note::

   If you are on \*nix you can install both **python** and **pygame** through your package manager::
   
      apt-get     install  python pygame
      aptitude    install  python pygame
      pacman      -S       python pygame

   Just make sure you're installing version of pygame compatible with the version of python.

How to run it
-------------

All you need it to execute ``game.py`` game file in the root game folder. You can do it via **python**. Run python in the directory with the game and print ``game.py``. Then the game will start. Also you can run it just as executable::

   #Add eXecutable flag to game.py file if it's not executable yet (should be, though)
   chmod +x game.py

   #Run the game
   ./game.py
