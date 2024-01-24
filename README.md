# haver <img src="https://raw.githubusercontent.com/LucaMingarelli/haver/master/haver/res/haver.jpg"  width="80">

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/LucaMingarelli/haver/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/LucaMingarelli/haver/tree/master)
[![version](https://img.shields.io/badge/version-0.1.0-success.svg)](#)
[![PyPI Latest Release](https://img.shields.io/pypi/v/haver.svg)](https://pypi.org/project/haver/)
[![License](https://img.shields.io/pypi/l/bindata.svg)](https://github.com/LucaMingarelli/haver/blob/master/LICENSE.txt)

[//]: # ([![Downloads]&#40;https://static.pepy.tech/personalized-badge/bindata?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads&#41;]&#40;https://pepy.tech/project/bindata&#41;)



## Installation

`pip install haver`

# How to

## Connection and Authentication
```python
from haver import Haver

haver = Haver(private_token='<your-haver-API-token>')
```

The class `Haver` also accepts keyword arguments to be passed to requests, 
which handles the connection to the API under the hood. In this way, 
by passing e.g. `verify` and `proxy` parameters, users can access Haver databases from behind firewalls.
For example:
```python
haver = Haver(private_token='<your-haver-API-token>',
              verify=False, # Or local path to certificates 
              proxies={'http': 'http://proxy-username:proxy-password@proxy-server.com:8080',
                       'https': 'http://proxy-username:proxy-password@proxy-server.com:8080'})
```

Instead of passing the token explicitely each time, 
the user can also set an environmental variable `HAVER_TOKEN` containing the API token. 
In this case connection will be as simple as 
`haver = Haver()`.

#### Obtaining tokens
To obtain your token, follow these steps:

* Log into haverview.com, then create a graph with any series.
* Click the vertical dots next to the Directory and Series tabs, above the search box.
* Select Export & Sharing in that menu. This will replace the left tab with the Export dialog.
* Copy the contents of the URL field. It is a link which contains your token, specified as a query parameter

E.g. from 
```
https://api.haverview.com/some/path/here?token=3f15493a-9e05-4b61-93ff-8ba56cb3a726
```
your token would be `3f15493a-9e05-4b61-93ff-8ba56cb3a726`.


## Exploring available resources

All available databases can easily be listed as

```python
haver.get_databases()
```

which will return a dictionary with keys the database names and values the corresponding database description:
```text
{'UNPOP': 'U.N. Population Statistics',
 'EPFRECA': 'Fund Country Allocations',
 'EUFIN': 'Financial Data',
 ...
 }
```

Further information on each dataset can be obtained via the method `haver.database_info`, 
and series within each database can be listed e.g. as

```python
haver.get_series(database='UNPOP', full_info=True)
```

In addition, a search function is also available to allow the user to search series by their descriptions, 
for example as:

```python
haver.search(query='employment')
```

## Querying data

In order to retrieve data, the user has the option of querying 
one series at a time via the dedicated method

```python
haver.read(database='EUDATA', series='N997CE')
```

which returns data in dictionary format, or querying multiple series
as
```python
haver.read_df(haver_codes=['N997CE@EUDATA','N025CE@EUDATA'])
```
where individual `haver_codes` are created by joining series and database names as `{series}@{database}`.

Finally, a database of available recessions can be obtained as

```python
haver.recessions()
```



# Author
Luca Mingarelli, 2024