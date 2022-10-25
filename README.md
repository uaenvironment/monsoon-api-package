# monsoon-api-package
## <ins>Overview</ins>
This package serves as a wrapper to simplify REST API calls to the UArizona Environment monsoon dataset. This is the same dataset that is visually represented in our monsoon plotter found at [monsoon.environment.arizona.edu](monsoon.environment.arizona.edu). The plotter allows a limited export of the data dependent on the date range and sensor network being plotted. This package allows you to incorporate our monsoon dataset into a local codebase for processing. The dataset consist of the following remote sensing precipitation networks along with their programmatic names:

- Pima County FCD - pima_fcd
- Maricopa County FCD - maricopa_fcd
- [RainLog.org](rainlog.org) - rainlog
- MesoWest - mesowest
- Mohave County FCD - mohave_fcd (data beginning 2021)

Data from the networks above are updated at different frequencies and in some cases multiple times per day or hour. This is variable across networks based on their configuration and if precipitation sensors are experiencing rainfall.

Data collection from additional networks is currently being tested and will be added to the list above when available. The network(s) currently being tested include:

- New networks coming soon

<br />

## <ins>Getting Started</ins>

### Requesting access
Our data is accessible via an API key request which can be sent to <monsoon-api@list.arizona.edu>

### Installing
Clone this repository and install the required dependencies using the included
`requirements.txt` file. This can be done using the command
`pip install -r  requirements.txt`. Next, install the monsoon package by
running `pip install .` from the root of the repository.

We intend to make the package available via PyPI in the near future.

### Command line usage
Following installation, the `monsoon-cli` command will be available. Use the
`moonsoon-cli --help` command for further instructions.

<br>

### Creating an instance of monsoon.py

The sample code below is the process to create an instance of the monsoon.py class.

````python
import monsoon

# pass your issued username and key as parameters to the monsoon.py class constructor
monsoon_object = monsoon.MonsoonAPI(username, key)
````
If incorrect credentials are supplied the class will return the following.

```
Could not authenticate
```

</br>

## <ins>Requesting Data</ins>

</br>

#### **precip_totals**(start_date, end_date, networks)
This function returns the sum of rainfall totals across each sensor in a given network(s) for a provided date range.

Parameters:
````
start_date (required): (string) - Range start date in "YYYY-MM-DD" format.
end_date (required):   (string) - Range end date in "YYYY-MM-DD" format.
network(s) (required): (string) - The network(s) to be queried. Multiple networks must be separated by a hyphen (-). ex. "pima_fcd-rainlog"
````

Example: 
````python
# single network query (return shown below)
monsoon_object.precip_totals("2021-08-01", "2021-08-02", "rainlog")

# multiple network query
monsoon_object.precip_totals("2021-08-01", "2021-08-02", "pima_fcd-rainlog")
````

Return:
````json
    ...
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
sensor:                (string) - Specific sensor to retrieve data for. If not provided, all sensor reading will be returned.
````

Example:
````python
monsoon_object.sensor_readings("pima_fcd", "2021-08-02", "2021-08-10", 1030)
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
This function returns data for a given network for an entire monsoon season within a given year(s). Seasons begin June 15th and end September 30th. If an end_year is provided it is treated as inclusive in the data return. Data can also be returned for an entire network or a specific sensor within the network being queried. If you use the raw parameter, which is by default False, the data will be run through the delta calculations. If you set the raw parameter to True the data won't be run through the delta calculation and you will be given the datetime. 

Parameters:
````
network (required):    (string) - Sensor network to gather data from.
start_year (required): (string) - Starting year in "YYYY" format.
end_year:              (string) - End year (inclusive) of monsoon data date range in "YYYY" format.
sensor:                (string) - Specific sensor name monsoon data is being requested for.
raw:                   (bool)   - Default is False. If True the data will run through our delta 
                                  calculation to return totals for all sensors during the
                                  monsoon period. Setting raw as True will also provide 
                                  datetime. 
````
Example:
````python
# request for sensor name 1030 precip data from 2019 and 2020 monsoon seasons
monsoon_object("pima_fcd", "2019", "2020", 1030, True) 
````
Return:
````json
    ...
    {
        "sensor_name": "1030",
        "reading_value": 6.73,
        "lat": 32.532799,
        "lon": -110.756248,
        "date": "2019-09-24 11:49:23",
        "network": "pima_fcd"
    },
    {
        "sensor_name": "1030",
        "reading_value": 6.77,
        "lat": 32.532799,
        "lon": -110.756248,
        "date": "2019-09-24 11:58:17",
        "network": "pima_fcd"
    },
    {
        "sensor_name": "1030",
        "reading_value": 6.81,
        "lat": 32.532799,
        "lon": -110.756248,
        "date": "2019-09-24 12:06:52",
        "network": "pima_fcd"
    },
    {
        "sensor_name": "1030",
        "reading_value": 6.85,
        "lat": 32.532799,
        "lon": -110.756248,
        "date": "2019-09-24 12:14:19",
        "network": "pima_fcd"
    },
    ...
````

Example:
````python
# request for sensor name 1030 precip data from 2019 and 2020 monsoon seasons
monsoon_object.monsoon_data("pima_fcd", "2019", "2020", 1030, False)
````

Return:
````json
    ...
    {
        "sensor_name": "1030",
        "total_rainfall": 6.93,
        "lon": -110.756248,
        "lat": 32.532799,
        "network": "pima_fcd"
    }
    ...
````



Example:
````python
# request for all sensor data from 2019 monsoon season
monsoon_object.monsoon_data("pima_fcd", "2019") 
````
Return:
````json
    ...
    {
        "sensor_name": "4310",
        "total_rainfall": 9.530000000000001,
        "lon": -110.645172,
        "lat": 31.993576,
        "network": "pima_fcd"
    },
    {
        "sensor_name": "4320",
        "total_rainfall": 6.179999999999999,
        "lon": -110.638847,
        "lat": 31.885183,
        "network": "pima_fcd"
    },
    {
        "sensor_name": "4410",
        "total_rainfall": 3.8200000000000003,
        "lon": -110.452812,
        "lat": 31.905499,
        "network": "pima_fcd"
    },
    {
        "sensor_name": "6020",
        "total_rainfall": 2.01,
        "lon": -111.080132,
        "lat": 32.337254,
        "network": "pima_fcd"
    },
    {
        "sensor_name": "6040",
        "total_rainfall": 4.530000000000001,
        "lon": -110.993095,
        "lat": 32.133057,
        "network": "pima_fcd"
    },
    ...
````

<br />

#### **sensor_metadata**(network, sensor="")
This function retrieves specific sensor metadata for a single sensor name or an entire network.

Parameters:
````
network (required): (string) - Network to retrieve sensor information from as string.
sensor:             (string) - Retrieve specific sensor metadata. If not provided all sensors within a network will be returned.
````
Example:
````python
# single sensor request
monsoon_object.sensor_metadata("pima_fcd", 1030)

# entire sensor network request
monsoon_object.sensor_metadata("pima_fcd")

````
Return:
````json
    ...
    {
        "sensor_id": 3,
        "sensor_name": "1030",
        "lat": 32.532799,
        "lon": -110.756248,
        "location_name": "Oracle Ridge",
        "sensor_type": "Precipitation"
    }
    ...
````
</br>

#### **flood_data(network, start_date, end_date="", sensor="")** 
 Flood data route makes an API call for data between the start date and end date 
 and optionally a sensor.

Parameters:

```
:param network (required):     (string) - sensor network only pima and maricopa 
:param start_date (required):  (string) - format "YYYY-MM-DD"
:param end_date:               (string) - format "YYYY-MM-DD"
:param sensor:                 (string) - specific sensor ID 
```

Example:

```python
# entire network request
monsoon_object.flood_data("pima_fcd","2022-02-15")
# single sensor request
monsoon_object.flood_data("maricopa_fcd","2022-01-18", "2022-02-01", "773")
```

Return:
```json
    ...
    {
        "sensor_name": "6383",
        "reading_date": "2022-02-15T22: 20: 56.000Z",
        "feet": 2.4,
        "cfs": 0,
        "anomaly_checksum": "",
        "lat": 31.839169,
        "lon": -111.404335
    }
    ... 
```
