.. Ziptool documentation master file, created by
   sphinx-quickstart on Mon Mar  7 15:18:48 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ziptool Documentation
===================================
This tool is designed to analyze microdata from the American Community Survey
(ACS) on a ZIP-code level. In an effort to anonymize data, the Census Bureau
(perhaps surprisingly) publishes microdata only down to the PUMA (Public Use
Microdata Area) level, each of which contains 100,000 people.

However, researchers often want community data at the ZIP code level. Using
some geographical tricks, Ziptool allows users to obtain approximate data at
the ZIP code level by querying the PUMA(s) it is inside.

The primary function of interest is *data_by_zip*, which takes a dataset and ZIP
codes of interest and returns either summary statistics or the full data.
However, many subfunctions are also documented and can be used standalone.

**Table of Contents**

.. toctree::
   :maxdepth: 2

    Getting Started <getting_started/getting_started>
    Background <why>
    Modules <modules/modules>
    Examples <examples/examples>

**Indices and tables**

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
