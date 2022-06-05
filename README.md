<div id="top"></div>

<!-- BADGES -->
![Build](https://github.com/bergsmith/csvcomparer/actions/workflows/CI.yaml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/csvcomparer/badge/?version=latest)](https://csvcomparer.readthedocs.io/en/latest/?badge=latest)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://badgen.net/github/license/Naereen/Strapdown.js)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

<!-- LOGO -->
<br />
<div align="center">
  <a href="https://github.com/bergsmith/csvcomparer">
    <img src="https://raw.githubusercontent.com/bergsmith/csvcomparer/main/images/logo.svg" alt="Logo" width="100" height="100">
  </a>
  <h3 align="center">csvcomparer</h3>
  <p align="center">
    Compare delimited files that share a common key.
    <br />
    <a href="http://csvcomparer.rtfd.io/"><strong>Explore the docs »</strong></a>
    ·
    <a href="https://github.com/bergsmith/csvcomparer/issues">Report Bug</a>
    ·
    <a href="https://github.com/bergsmith/csvcomparer/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#example">Example</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
<br />

<!-- OVERVIEW -->
## Overview
**csvcomparer** is an open-source Python project used for determining differences between two delimited files (referred to here as "left" and "right" files) that share a common key, or index. Specifically, **csvcomparer** determines:

  - Columns exclusive to the left and right files, respectively.
  - Rows exclusive to the left and right files, respectively.
  - Field-level differences for rows/columns in common between files.

<p align="right">(<a href="#top">back to top</a>)</p>

## Basic Usage
As a python module:
```python
from csvcomparer import CsvCompare

diffs = CsvCompare(
  "<path/to/left_file.csv>",
  "<path/to/right_file.csv>",
  "<key>").diffs
```

As a command line utility:
```
> python csvcomparer left_csv_filepath right_csv_filepath key
```
## Examples

Provided the following file data:  
**_menu_l.csv_**
|id |name  |pic|price|score|togo|
|---|------|---|-----|-----|----|
|1A |beer  |🍺 |$6.00|3.9  |N   |
|1B |wine  |🍷 |$7.25|4.5  |N   |
|2A |cheese|🧀 |$4.10|4.0  |Y   |
|3A |bacon |🥓 |$3.33|4.9  |Y   |

**_menu_r.csv_**
|id |name  |pic|price|stars|
|---|------|---|-----|-----|
|1A |beer  |🍻 |$5.25|3.9  |
|1B |wine  |🍷 |$7.25|4.8  |
|2A |cheese|🧀 |$3.95|4.1  |
|4C |taco  |🌮 |$8.33|3.1  |
|5B |pizza |🍕 |$9.99|2.4  |


Usage as a Python module...
```python
>>> from csvcomparer import CsvCompare
>>> CsvCompare("menu_l.csv", "menu_r.csv", "id").diffs
```
... or as a command-line utility:
```sh
> python csvcomparer menu_l.csv menu_r.csv id
```
Returns:
```sh
{'cols_added': ['stars'],
 'cols_removed': ['score', 'togo'],
 'rows_added': {'4C': {'name': 'taco',
                       'pic': '🌮',
                       'price': '$8.33',
                       'stars': 3.1},
                '5B': {'name': 'pizza',
                       'pic': '🍕',
                       'price': '$9.99',
                       'stars': 2.4}},
 'rows_changed': {'1A': [('pic', '🍺', '🍻'), ('price', '$6.00', '$5.25')],
                  '2A': [('price', '$4.10', '$3.95')]},
 'rows_removed': {'3A': {'name': 'bacon',
                         'pic': '🥓',
                         'price': '$3.33',
                         'score': 4.9,
                         'togo': 'Y'}}}

```                     
Multi-column keys are also supported. So for the same file data:
```python
>>> CsvCompare("menu_l.csv", "menu_r.csv", ["id", "name"]).diffs
```
Returns:
```sh
{'cols_added': ['stars'],
 'cols_removed': ['score', 'togo'],
 'rows_added': {('4C', 'taco'): {'pic': '🌮', 'price': '$8.33', 'stars': 3.1},
                ('5B', 'pizza'): {'pic': '🍕', 'price': '$9.99', 'stars': 2.4}},
 'rows_changed': {('1A', 'beer'): [('pic', '🍺', '🍻'),
                                   ('price', '$6.00', '$5.25')],
                  ('2A', 'cheese'): [('price', '$4.10', '$3.95')]},
 'rows_removed': {('3A', 'bacon'): {'pic': '🥓',
                                    'price': '$3.33',
                                    'score': 4.9,
                                    'togo': 'Y'}}}
```

See the docs for detailed usage and examples.



<p align="right">(<a href="#top">back to top</a>)</p>

<!-- INSTALLATION -->
## Installation
### Prerequisites
  - [Python](https://www.python.org/) v3.6 or greater
  - [Poetry](https://python-poetry.org/)

Then simply run:
```sh
poetry install csvcomparer
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap
**csvcomparer** is in its infancy, and there are high hopes for this project!

The ultimate goal is being able to compare any two data sets that can be consumed as a "dataframe", regardless of size, efficiently as possible. This comes with a great deal of challenges, but I'm confident it will get there. 

See the [open issues](https://github.com/bergsmith/csvcomparer/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing
Any contributions are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License
Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
Ryan Bergsmith - [LinkedIn](https://www.linkedin.com/in/bergsmith/) - ryguydev@gmail.com  
Project Link: [Github](https://github.com/bergsmith/csvcomparer)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
  - [Robin Zaubeerer](https://github.com/Zaubeerer) for being a great [PDM](https://pybit.es/catalogue/the-pdm-program/) coach and providing roadmap inspiration.

<p align="right">(<a href="#top">back to top</a>)</p>