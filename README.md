# monsoon-api-package
## Overview
This package serves as a wrapper to simplify REST API calls to the UArizona Environment monsoon dataset. This is the same dataset that is visually represented in our monsoon plotter found at [monsoon.environment.arizona.edu](monsoon.environment.arizona.edu). The plotter allows a limited export of the data dependent on the date range and sensor network being plotted. This package allows you to incorporate our monsoon dataset into a local codebase for processing. The dataset consist of the following remote sensing precipitation networks along with their programmatic names:

- Pima County FCD - pima_fcd
- Maricopa County FCD - maricopa_fcd
- [RainLog.org](rainlog.org) - rainlog
- MesoWest - mesowest

Data from the networks above are updated at different frequencies and in some cases multiple times per day or hour. This is variable across networks based on their configuration and if precipitation sensors are experiencing rainfall.

Data collection from additional networks is currently being tested and will be added to the list above when available. The network(s) currently being tested include:

- Mohave County FCD

<br />

## Getting Started
This package contains 2 files named mon_conf.py which serves as a configuration file and monsoon.py which is the collection of functions used to query the API for data. 

### mon_conf.py
Serves as the main configuration file used for user/organization API authentication. It contains the base URL variable used to build the API query string, and the USERNAME and KEY variables which must be set prior to making an API call. These string values are issued once access has been granted to the dataset.

````python
# API base URL
URL = "https://api.air.arizona.edu"

# Input issued username and key information below
USERNAME = ""
KEY = ""
````

After you have configured mon_conf.py wth your issued USERNAME and KEY, you can then import monsoon into your project file along with the JSON package.

````python
import json
import monsoon

# sample function calls NOTE: missing required parameters
monsoon.precip_totals(parameters)
monsoon.sensor_readings(parameters)
monsoon.monsoon_data(parameters)
monsoon.sensor_metadata(parameters)

# example of storing API data in python variable
data = monsoon.sensor_metadata("pima_fcd", 1030)

# TODO: describe the python datatype of the above data variable

# TODO: show how to retrieve specific values within the data
````
<br />

## Requesting Data

### monsoon.py

Serves as the main file containing a collection of functions used to make API queries. Below are function descriptions and examples of their use.

<br />

#### **precip_totals**(start_date, end_date, networks)
This function returns the sum of rainfall totals across each sensor in a given network(s) for a provided date range.

Parameters:
````
start_date (required): (string) - Range start date in "YYYY-MM-DD" format.
end_date (required):   (string) - Range end date in "YYYY-MM-DD" format.
network(s) (required): (string) - The network or networks to be queried. Multiple networks must be separated by a hyphen (-). ex. "pima_fcd-rainlog"
````

Example: 
````python
# single network query (return shown below)
precip_totals("2021-08-01", "2021-08-02", "rainlog")

# multiple network query
precip_totals("2021-08-01", "2021-08-02", "pima_fcd-rainlog")
````

Return:
````json
    {
        "total_rainfall": 0,
        "lon": -111.60009,
        "lat": 33.347397,
        "network": "rainlog",
        "sensor_name": "11003"
    },
    {
        "total_rainfall": 0.1,
        "lon": -112.461716,
        "lat": 34.627197,
        "network": "rainlog",
        "sensor_name": "11004"
    },
    {
        "total_rainfall": 0.18,
        "lon": -110.045517,
        "lat": 34.235909,
        "network": "rainlog",
        "sensor_name": "11009"
    },
    ...
````

<br />

#### **sensor_readings**(network, start_date, end_date="", sensor="")
This function returns the raw unprocessed data from a given network or specific network sensor for a given date range.

Parameters:
````
network (required):    (string) - Sensor network to gather data from.
start_date (required): (string) - Specific date or beginning date range to gather data from in "YYYY-MM-DD" format.
end_date:              (string) - End date of a the date range being requested in "YYYY-MM-DD" format.
sensor:                (int)    - Specific sensor to retrieve data for. If not provided, all sensor reading will be returned.
````

Example:
````python
sensor_readings("pima_fcd", "2021-08-02", "2021-08-10", 1030)
````
Return:
````json
    {
        "sensor_name": "1030",
        "reading_value": 13.5,
        "datetime": "2021-08-02 11:59:56"
    },
    {
        "sensor_name": "1030",
        "reading_value": 13.5,
        "datetime": "2021-08-02 23:59:55"
    },
    {
        "sensor_name": "1030",
        "reading_value": 13.5,
        "datetime": "2021-08-03 11:59:53"
    },
    {
        "sensor_name": "1030",
        "reading_value": 13.5,
        "datetime": "2021-08-03 23:59:53"
    },
    ...
````

<br />

#### **monsoon_data**(network, start_year, end_year="", sensor="")
This function returns data for a given network for an entire monsoon season within a given year(s). Seasons begin June 15th and end September 30th. If an end_year is provided it is treated as inclusive in the data return. Data can also be returned for an entire network or a specific sensor within the network being queried.

Parameters:
````
network (required):    (string) - Sensor network to gather data from.
start_year (required): (string) - Starting year in "YYYY" format.
end_year:              (string) - End year (inclusive) of monsoon data date range in "YYYY" format.
sensor:                (int)    - Specific sensor name monsoon data is being requested for.
````
Example:
````python
# request for sensor name 1030 precip data from 2019 and 2020 monsoon seasons
monsoon_data("pima_fcd", "2019", "2020", 1030)

# request for all sensor data from 2019 monsoon season
monsoon_data("pima_fcd", "2019")
````
Return:
````json
    {
        "sensor_name": "1030",
        "reading_value": 6.89,
        "datetime": "2019-09-24 12:21:39"
    },
    {
        "sensor_name": "1030",
        "reading_value": 6.89,
        "datetime": "2019-09-24 22:19:57"
    },
    {
        "sensor_name": "1030",
        "reading_value": 6.93,
        "datetime": "2019-09-25 04:43:28"
    },
    {
        "sensor_name": "1030",
        "reading_value": 6.97,
        "datetime": "2019-09-25 04:54:22"
    },
    {
        "sensor_name": "1030",
        "reading_value": 7.01,
        "datetime": "2019-09-25 05:15:08"
    },
    ...
````

<br />

#### **sensor_metadata**(network, sensor="")
This function retrieves specific sensor metadata for a single sensor name or an entire network.

Parameters:
````
network (required): (string) - Network to retrieve sensor information from as string.
sensor:             (int)    - Retrieve specific sensor metadata. If not provided all sensors within a network will be returned.
````
Example:
````python
# single sensor request
sensor_metadata("pima_fcd", 1030)

# entire sensor network request
sensor_metadata("pima_fcd")

````
Return:
````json
[
    {
        "sensor_id": 3,
        "sensor_name": "1030",
        "lat": 32.532799,
        "lon": -110.756248,
        "location_name": "Oracle Ridge",
        "sensor_type": "Precipitation"
    }
]
````



#### **flood_data(network, start_date, end_date="",sensor="")** 
 Flood data route makes an API call for data between the start date and end date 
 and optionally a sensor.

Parameters:

```
:param network (required):     (string) - sensor network only pima and maricopa 
:param start_date (required):  (string) - format "YYYY-MM-DD"
:param end_date (optional):    (string) - format "YYYY-MM-DD"
:param sensor (optional):      (string) - specific sensor ID 
```

Example:

```
# entire network request
flood_data("pima_fcd","2022-02-15")
# single sensor request
flood_data("maricopa_fcd","2022-01-18", "2022-02-01", "773")
```

Return:
``` 
 [
      {
        'sensor_name': '6383',
        'reading_date': '2022-02-15T22: 20: 56.000Z',
        'feet': 2.4,
        'cfs': 0,
        'anomaly_checksum': '',
        'lat': 31.839169,
        'lon': -111.404335
    } 
]