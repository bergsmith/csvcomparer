Examples
========
Assume the following .csv file data:

**menu_l.csv** - *the "left" file*

 ===== ========= ====== ======== ======== ======= 
  id    name      pic    price    score    togo   
 ===== ========= ====== ======== ======== ======= 
  1A    beer      🍺     $6.00    3.9      N      
  1B    wine      🍷     $7.25    4.5      N      
  2A    cheese    🧀     $4.10    4.0      Y      
  3A    bacon     🥓     $3.33    4.9      Y      
 ===== ========= ====== ======== ======== ======= 

**menu_r.csv** - *the "right" file*

 ===== ========= ====== ======== ======== 
  id    name      pic    price    stars   
 ===== ========= ====== ======== ======== 
  1A    beer      🍻     $5.25    3.9     
  1B    wine      🍷     $7.25    4.8     
  2A    cheese    🧀     $3.95    4.1     
  4C    taco      🌮     $8.33    3.1     
  5B    pizza     🍕     $9.99    2.4     
 ===== ========= ====== ======== ======== 

.. note::
   Within this project's context, the following changes are said to have occurred between the left and right files (with respect to the ``id``):

      - Two columns (``score`` and ``togo``) have been removed
      - One column (``stars``) has been added
      - Two rows (``id: 4C`` and ``id: 5B``) have been added
      - One row (``id: 3A``) has been removed
      - Two rows have changed:

         - ``id: 1A``

            - ``pic`` changed from ``🍺`` to ``🍻``
            - ``price`` changed from ``$6.00`` to ``$5.25``

         - ``id: 2A``

            - ``price`` changed from ``$4.10`` to ``$3.95``

Get all difference (diff) types
-------------------------------
The CsvCompare object has a ``diffs`` property that leverages a convenience class CsvCompareDiffs, which is essentially an accumulation of the individual difference types, along with some additional functionality for formatting and reference.

In this example, the ``id`` column is being used as the row key, or index, between the two files. Any column that is unique, or group of columns whose respective row values are unique when combined, can be used as the row key.

.. tabs::

   .. group-tab:: Python

      .. code-block::

         >>> from csvcomparer import CsvCompare
         >>> csvx = CsvCompare("menu_l.csv", "menu_r.csv", "id")
         >>> csvx.diffs

         {'cols_added': ['stars'],
          'cols_removed': ['score', 'togo'],
          'row_key': ['id'],
          'rows_added': {'4C': {'name': 'taco',
                                'pic': '🌮',
                                'price': '$8.33',
                                'stars': 3.1},
                         '5B': {'name': 'pizza',
                                'pic': '🍕',
                                'price': '$9.99',
                                'stars': 2.4}},
          'rows_changed': {'1A': [('pic', '🍺', '🍻'), 
                                  ('price', '$6.00', '$5.25')],
                           '2A': [('price', '$4.10', '$3.95')]},
          'rows_removed': {'3A': {'name': 'bacon',
                                  'pic': '🥓',
                                  'price': '$3.33',
                                  'score': 4.9,
                                  'togo': 'Y'}}}

   .. group-tab:: CLI

      .. code-block::

         > python csvcomparer menu_l.csv menu_r.csv id

         {'cols_added': ['stars'],
          'cols_removed': ['score', 'togo'],
          'row_key': ['id'],
          'rows_added': {'4C': {'name': 'taco',
                                'pic': '🌮',
                                'price': '$8.33',
                                'stars': 3.1},
                         '5B': {'name': 'pizza',
                                'pic': '🍕',
                                'price': '$9.99',
                                'stars': 2.4}},
          'rows_changed': {'1A': [('pic', '🍺', '🍻'),
                                  ('price', '$6.00', '$5.25')],
                           '2A': [('price', '$4.10', '$3.95')]},
          'rows_removed': {'3A': {'name': 'bacon',
                                  'pic': '🥓',
                                  'price': '$3.33',
                                  'score': 4.9,
                                  'togo': 'Y'}}}

Per the mention above, here's an example using both ``id`` and ``name`` as the row key (or index):

.. tabs::

   .. group-tab:: Python

      .. code-block::

         >>> from csvcomparer import CsvCompare
         >>> csvx = CsvCompare("menu_l.csv", "menu_r.csv", ["id", "name"])
         >>> csvx.diffs

         {'cols_added': ['stars'],
          'cols_removed': ['score', 'togo'],
          'row_key': ["id", "name"],
          'rows_added': {('4C', 'taco'): {'pic': '🌮', 
                                          'price': '$8.33',
                                          'stars': 3.1},
                         ('5B', 'pizza'): {'pic': '🍕', 
                                           'price': '$9.99',  
                                           'stars': 2.4}},
          'rows_changed': {('1A', 'beer'): [('pic', '🍺', '🍻'),
                                            ('price', '$6.00', '$5.25')],
                           ('2A', 'cheese'): [('price', '$4.10', '$3.95')]},
          'rows_removed': {('3A', 'bacon'): {'pic': '🥓',
                                             'price': '$3.33',
                                             'score': 4.9,
                                             'togo': 'Y'}}}

   .. group-tab:: CLI

      .. code-block::

         > python csvcomparer menu_l.csv menu_r.csv id name

         {'cols_added': ['stars'],
          'cols_removed': ['score', 'togo'],
          'row_key': ["id", "name"],
          'rows_added': {('4C', 'taco'): {'pic': '🌮', 
                                          'price': '$8.33',
                                          'stars': 3.1},
                         ('5B', 'pizza'): {'pic': '🍕', 
                                           'price': '$9.99',  
                                           'stars': 2.4}},
          'rows_changed': {('1A', 'beer'): [('pic', '🍺', '🍻'),
                                            ('price', '$6.00', '$5.25')],
                           ('2A', 'cheese'): [('price', '$4.10', '$3.95')]},
          'rows_removed': {('3A', 'bacon'): {'pic': '🥓',
                                             'price': '$3.33',
                                             'score': 4.9,
                                             'togo': 'Y'}}}

Get individual diff types
-------------------------
Each of the diff types from a CsvCompare object are also available properties.

.. important::
   The input files are "lazily loaded" in that the first to call to a CsvCompare diff property triggers the ingestion.

   So in the example below, ``csvx.cols_added`` triggers the input file ingestion. Subsequent calls to diff properties (ex. ``csvx.rows_added`` added) will not attempt to reload the input files.

.. tabs::

   .. group-tab:: Python

      >>> from csvcomparer import CsvCompare
      >>> csvx = CsvCompare("menu_l.csv", "menu_r.csv", "id")
      >>> csvx.cols_added
      ['stars']
      >>> csvx.cols_removed
      ['score', 'togo']
      >>> csvx.rows_added
      {'4C': {'name': 'taco',
              'pic': '🌮',
              'price': '$8.33',
              'stars': 3.1},
       '5B': {'name': 'pizza',
              'pic': '🍕',
              'price': '$9.99',
              'stars': 2.4}}
      >>> csvx.rows_changed
      {'1A': [('pic', '🍺', '🍻'), 
              ('price', '$6.00', '$5.25')],
       '2A': [('price', '$4.10', '$3.95')]}
      >>> csvx.rows_removed
      {'3A': {'name': 'bacon',
              'pic': '🥓',
              'price': '$3.33',
              'score': 4.9,
              'togo': 'Y'}}

   .. group-tab:: CLI

      .. note:: Not currently supported for CLI. See Get all differences.

Convert diffs to json
---------------------
The ``CsvCompareDiff`` object has a ``to_json()`` method that can be used for converting the output.

.. note::
   JSON keys must be strings; therefore, multi-column row keys are converted to comma-delimited strings.

.. tabs::

   .. group-tab:: Python

      .. code-block::

         >>> from csvcomparer import CsvCompare
         >>> csvx = CsvCompare("menu_l.csv", "menu_r.csv", ["id", "name"])
         >>> csvx.diffs.to_json()

         {"row_key": ["id", "name"], 
          "rows_added": {"4C, taco": {"pic": "\ud83c\udf2e", 
                                      "price": "$8.33", 
                                      "stars": 3.1}, 
                         "5B, pizza": {"pic": "\ud83c\udf55", 
                                       "price": "$9.99", 
                                       "stars": 2.4}}, 
          "rows_removed": {"3A, bacon": {"pic": "\ud83e\udd53", 
                                         "price": "$3.33", 
                                         "score": 4.9, 
                                         "togo": "Y"}}, 
          "rows_changed": {"1A, beer": [["pic", "\ud83c\udf7a", "\ud83c\udf7b"], 
                                        ["price", "$6.00", "$5.25"]], 
                           "2A, cheese": [["price", "$4.10", "$3.95"]]}, 
          "cols_added": ["stars"], 
          "cols_removed": ["score", "togo"]}

   .. group-tab:: CLI

      .. code-block:: sh

         > python csvcomparer menu_l.csv menu_r.csv id name --json

         {"row_key": ["id", "name"], 
          "rows_added": {"4C, taco": {"pic": "\ud83c\udf2e", 
                                      "price": "$8.33", 
                                      "stars": 3.1}, 
                         "5B, pizza": {"pic": "\ud83c\udf55", 
                                       "price": "$9.99", 
                                       "stars": 2.4}}, 
          "rows_removed": {"3A, bacon": {"pic": "\ud83e\udd53", 
                                         "price": "$3.33", 
                                         "score": 4.9, 
                                         "togo": "Y"}}, 
          "rows_changed": {"1A, beer": [["pic", "\ud83c\udf7a", "\ud83c\udf7b"], 
                                        ["price", "$6.00", "$5.25"]], 
                           "2A, cheese": [["price", "$4.10", "$3.95"]]}, 
          "cols_added": ["stars"], 
          "cols_removed": ["score", "togo"]}