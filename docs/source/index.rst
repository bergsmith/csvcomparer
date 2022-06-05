Welcome to csvcomparer's documentation!
=======================================

.. raw:: html

   <!-- LOGO -->
   <div align="center">
   <a href="https://github.com/bergsmith/csvcomparer">
      <img src="https://raw.githubusercontent.com/bergsmith/csvcomparer/main/images/logo.svg" alt="Logo" width="100" height="100">
   </a>
   <h3 align="center">csvcomparer</h3>
   <p align="center">
      Compare delimited files that share a common key.
      <br />
      <a href="https://github.com/bergsmith/csvcomparer/issues">Report Bug</a>
      ·
      <a href="https://github.com/bergsmith/csvcomparer/issues">Request Feature</a>
   </p>
   </div>

Overview
--------
**csvcomparer** is an open-source Python project used for determining differences between two delimited files (referred to here as "left" and "right" files) that share a common key, or index. Specifically, **csvcomparer** determines:

- Columns exclusive to the left and right files, respectively.
- Rows exclusive to the left and right files, respectively.
- Field-level differences for rows/columns in common between files.


.. toctree::
   :maxdepth: 2
   :caption: Quick Start
   :hidden:

   installation
   examples


.. toctree::
   :maxdepth: 2
   :caption: Class Reference
   :hidden:

   csvcompare
   csvcompare_diffs


.. toctree::
   :maxdepth: 2
   :caption: About The Project
   :hidden:

   roadmap
   contributing