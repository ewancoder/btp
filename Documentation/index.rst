.. Big Typernatural Project Documentation
   Created by EwanCoder, 2014

.. Links declaration
.. _github: https://github.com/ewancoder/btp
.. _develop: https://github.com/ewancoder/game/tree/develop

Big Typernatural Project's documentation!
*****************************************

This is documentation created by Sphinx about my game project - **Big TyperNatural Project, BTP**. You can see all the **source code** at my `github`_ repo. For the newest updates, you should check `develop`_ branch, although it is not created yet because the game on it's early stage - there's nothing to be stable yet. The source code on this documentation located in **Documentation** directory of BTP source tree.

Contents:

.. toctree::
    :maxdepth: 2

    about
    structure
    features
    resources

.. _whatisit:

What is BTP?
============

BTP is **text-based RPG game** with **typing** battle system.

You can read about it more on :doc:`about`.

How to get it?
==============

You can **download lastest version** using my `github`_ repo::

    curl -O https://raw.githubusercontent.com/ewancoder/btp
    #or wget
    whet https://raw.github.com/ewancoder/btp

And you can try it by executing **game.py** file you've just downloaded. All you need for game to work is **python3 or 2** and **pygame**.

How to use this documentation
=============================

First, read this page and :doc:`about` page for understanding what it is. Then read :doc:`structure` page for technical information about whole application structure, it's files and directories. Then you're free to choose what you want to discover. I'd go with :doc:`main` firstly.
