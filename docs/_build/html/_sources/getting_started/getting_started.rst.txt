Getting Started
===============

Installation
------------

Ziptool requires Python >= 3.8.0. Install using :code:`pip`:

::

  pip install ziptool

Obtaining Data
--------------

Ziptool extracts information from ACS data. Data of the following forms can be
used:

1. Downloaded, rectangular CSV that contains your variables of interest. You
   can register at https://usa.ipums.org/ and download the data you would like.
   You must be sure to download rectangular data and include PUMA *and* STATEFIP,
   as variables, as the analysis relies on PUMA and state to convert to ZIP code.

2. Alternatively, you could use `ipumspy <https://ipumspy.readthedocs.io/en/latest/>`_!
   This very convenient package allows you to generate a pd.DataFrame for whatever
   data you would like and queries IPUMS directly using the API. This is the
   preferred method for convenience's sake, although both are equally supported.

Extracting ZIP-level Data
-------------------------

The top-level function used to extract data by ZIP code is :code:`data_by_zip`.
Assuming that you have downloaded your data as a CSV, you might use the following
code to query data, assuming that you are interested in the education and
household income for the zip codes 79901 and 02835.

::

  from ziptool import data_by_zip

  data_by_zip(['02835','79901'], path_to_csv,
      {"HHINCOME": {"null": 9999999, "type":'household'},
           "EDUC": {"null": 0, "type": 'individual'}})

You can provide as many ZIP codes as you would like, and as many variables, too.
You must provide the null value for a variable and its type (household or
individual), both of which are readily available from the IPUMS codebook.

If you performed the following query on the 2019 ACS, it would return the
following dictionary. You can easily pull out the statistics you would like.

::

    {'02835':
        {'HHINCOME':
               {'mean': 119942.69862560992, 'std': 135934.56385165124, 'median': 83000.0},
        'EDUC':
               {'mean': 7.361143491088583, 'std': 3.014875918280958, 'median': 7.0}},
     '79901':
        {'HHINCOME':
               {'mean': 46493.49292927944, 'std': 57214.110770472565, 'median': 29982.499776612964},
         'EDUC':
               {'mean': 5.51115705612258, 'std': 2.90874723027615, 'median': 5.999999955296516}}}

The summary statistics for household income make sense! However, education is a
categorical variable, so the summary statistics might be less useful. In that
case, you might choose to provide no argument for :code:`variables` to simply
return the raw pd.DataFrames that you could analyze as you wish.

::

  from ziptool import data_by_zip

  data_by_zip(['02835','79901'], path_to_csv, None)

Because no variables are specified, no analysis is performed -- the function
simply returns the dataframes for each PUMA within the ZIP code and its ratio
(i.e. if some ZIP code 99999 is 75% within PUMA 1 and 25% within PUMA 2,
the code would return one pd.DataFrame per PUMA along with the ratio.) The above
code would return:

::

    {'02835':
                 YEAR  SAMPLE   SERIAL       CBSERIAL  HHWT        CLUSTER  STATEFIP  ...  GQ  HHINCOME  BEDROOMS  PERNUM  PERWT  EDUC  EDUCD
        2542312  2019  201901  1125822  2019010002705  77.0  2019011258221        44  ...   4   9999999         0       1   77.0    11    115
        2542335  2019  201901  1125845  2019010007698  45.0  2019011258451        44  ...   4   9999999         0       1   45.0     7     71
        ...       ...     ...      ...            ...   ...            ...       ...  ...  ..       ...       ...     ...    ...   ...    ...
        2552708  2019  201901  1130856  2019001405444  44.0  2019011308561        44  ...   1     78910         5       2   35.0    11    115

     '79901':
                 YEAR  SAMPLE   SERIAL       CBSERIAL   HHWT        CLUSTER  STATEFIP  ...  GQ  HHINCOME  BEDROOMS  PERNUM  PERWT  EDUC  EDUCD
        2681259  2019  201901  1189446  2019010001158   39.0  2019011894461        48  ...   3   9999999         0       1   39.0     2     23
        2681291  2019  201901  1189478  2019010001549    7.0  2019011894781        48  ...   3   9999999         0       1    7.0     6     63
        ...       ...     ...      ...            ...    ...            ...       ...  ...  ..       ...       ...     ...    ...   ...    ...
        2952760  2019  201901  1302906  2019001405840  105.0  2019013029061        48  ...   1     11000         4       1  105.0     6     63

02835 and 79901 both exist exclusively inside one PUMA, so no ratios are provided
(since they are one). The pd.DataFrame for each ZIP code can easily be queried
from the return dictionary and used as any other pd.DataFrame for analysis of
your choice.
