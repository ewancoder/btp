Big Typernatural Project Documentation
**************************************

**Big TyperNatural Project, BTP** is a **game** written in **Python**, powered by **PyGame** and based on **keyboard typing**. This game doesn't even have mouse support. And this is not a trouble at all - it's a feature. And another feature of this game is that alongside with gaining experience, new levels, clothes and having a good time you actually will be gaining **real life experience** in fast keyboard typing, because... *wait for it*... battle system is **typo-like** (touchtyping guys will be able to handle some bosses at start). Just imagine it: you are typing commands to go somewhere, you're typing as fast as you can to kill those stupid monsters and you are such a fast typer so you can kill anyone who dare to throw you a glove. Fascinating, isn't it? All you need to do is to buy a good expensive mechanical keyboard (not necessarily), download game and start typing challenge! But for starters - wait until I'll create any **stable version** of the game :) Although, you can try **dev**.

This wiki is powered by **Sphinx** and intended to help both **users** to start playing and any **developers** (including me, hehe) to understand actual code and maintain it easily with comprehension of each and single line. Thus, this wiki has both "user" side and ``"developer"`` side, which are actually pretty entwined close together (but you can be whether advanced user or crappy programmer). So sometimes users could see something like "this function calling class header procedure holy shit returning value", and developer guys could see something like "press this big red button with your Enter key (which is a big key right to the right)".

Contents:
=========

.. toctree::
    :maxdepth: 10

    about
    use
    dev
    features

How to get it?
==============

First of all, to run it you will need `python <http://www.python.org>`_ and `pygame <http://www.pygame.org>`_. Download them for your OS, or just install it by your package manager::

    apt-get     install     python pygame
    aptitude    install     python pygame
    pacman      -S          python pygame

Now, you can browse my `github repo <https://github.com/ewancoder/btp>`_ and download game as archive. Soon I'll finally make release v0.1, which will contain browse-walking system ready-made (yet without quests, battles, etc). Right after than I'll add `development (dev) branch <https://github.com/ewancoder/btp/tree/dev>`_ **dev** branch and all newest changes will go there, when **master** branch will contain all most **stable** versions like 0.1.1 or 0.1.2, and **releases** will contain most stable and biggest versions like 0.2, 0.3 and 1.0 (someday).

To download lastest (stable) version from git, either click `this link (ZIP) <https://github.com/ewancoder/btp/archive/master.zip>`_ or run::

    curl -O https://github.com/ewancoder/btp/archive/master.zip
    #or wget
    wget https://github.com/ewancoder/btp/archive/master.zip

To download development version, simply change 'master' to 'dev' in the link or `click here (ZIP) <https://github.com/ewancoder/btp/archive/dev.zip>`_.

Then you can just execute **game.py** file by cd in the downloaded directory and executing game like this::

    ./game.py

Also you may need to change permissions of the file so it can be executed::

    chmod +x game.py
    ./game.py

And maybe you don't want to make this file executable, then you can just run it via python like this::

    python game.py

.. note::
   You can use python2 or python3 whichever you like, the game is cross-versioned.

.. warning::
   Don't forget to install both **python** and **pygame**.
