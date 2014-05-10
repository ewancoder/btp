Development Lab
***************

.. contents::
   :depth: 2

.. todo::

   * Write on this page (dev.rst) something about pygame (I can read more about pygame here)
   * I can read here more on software that I use for coding - arch linux + vim + jedi plugin (I've not described all the plugins and other stuff) [from about.rst, line 58]

Branching
---------

This is main `github repo <https://github.com/ewancoder/btp>`_ of the game. You can clone it for your sake. As you can see, it has multiple branches.

* `master <https://github.com/ewancoder/btp/tree/master>`_ - main branch for **stable releases**. There will go versions like *0.1*, *0.2*, *1.0* - official stable releases.
* `dev <https://github.com/ewancoder/btp/tree/dev>`_ - **development** branch. All development goes here, but separate big features being developed on separate branches created just for these features. Here goes versions *0.0.7*, *0.0.7.4*, *0.1.1* and etc.
* `docs <https://github.com/ewancoder/btp/tree/docs>`_ - separate branch for **docs**. It is made for good and clean commits history and splitting documentation & code development, but because this documentation uses :py:mod:`sphinx autodoc extension <sphinx.ext.autodoc>`, it's essential to merge **dev** branch to **docs** branch each time before creating docs for new features.

When the big feature being developed, it's useful to create separate branch just for it. And if it's big enough and consists from separate parts or features, new separate branches could be created from this branch. For example - `req branch <https://github.com/ewancoder/btp/tree/req>`_ was created for solving issue with virtualenv not building my req.txt, pygame and other stuff. Now it's perfectly working with readthedocs.

Modules
-------

.. toctree::
   :maxdepth: 2

   game
   screens
