import sys
import requests
import json
import mon_conf
import datetime

"""
Collection of wrapper functions for monsoon API route requests.
"""


def precip_totals(start_date, end_date, networks):
    """
    precip_totals() returns the sum of rainfall totals across each sensor in a given network(s) 
    for a provided date range.

    :param start_date (required): (string) - Range start date in "YYYY-MM-DD" format.
    :param end_date (required):   (string) - Range end date in "YYYY-MM-DD" format.
    :param network(s) (required): (string) - The network or networks to be queried. Multiple networks must be separated by a hyphen (-). ex. "pima_fcd-rainlog"
    :return JSON:                          - Returns total rainfall value totals for sensors in the provided network(s).
    """

    # validate date input
    validate_date_input(start_date, end_date)

    # after input validation, construct API request
    query_string = mon_conf.URL + \
        "?startDate={}&endDate={}&network={}".format(
            start_date, end_date, networks)

    # send request
    return get_data(query_string)


def sensor_readings(network, start_date, end_date="", sensor=""):
    """
    Retrieves raw unprocessed sensor reading data from a given network or network sensor for a
    specific date or date range.
    
    :param network (required):    (string) - Sensor network to gather data from.
    :param start_date (required): (string) - Specific date or beginning date range to gather data from in "YYYY-MM-DD" format.
    :param end_date:              (string) - End date of a the date range being requested in "YYYY-MM-DD" format.
    :param sensor:                (string) - Specific sensor to retrieve data for. If not provided, all sensor reading will be returned.
    :return JSON:                          - Returns unprocessed data for a network or network sensor for a given date(s).
    """

    # validate date input
    validate_date_input(start_date, end_date)

    # construct API request
    query_string = mon_conf.URL + \
        "/readings?network={}&startDate={}&endDate{}&sensor={}".format(
            network, start_date, end_date, sensor)

    # send request
    return get_data(query_string)

def flood_data(network, start_date, end_date="", sensor=""):
    """
    Flood data route makes an API call for data between the start date and end date 
    and optionally a sensor.
    :param network (required):     (string) - sensor network only pima and maricopa 
    :param start_date (required):  (string) - format "YYYY-MM-DD"
    :param end_date (optional):    (string) - format "YYYY-MM-DD"
    :param sensor (optional):      (string) - specific sensor ID 
    """
    validate_date_input(start_date, end_date)

    query_string = mon_conf.URL + \
        "/flood?network={}&startDate={}&endDate{}&sensor={}".format(
            network, start_date, end_date, sensor)

    return get_data(query_string)


def monsoon_data(network, start_year, end_year="", sensor="", raw=""): 
    """
    Monsoon data route which makes an API call for data between June 15th to
    September 30th for a given year or set of years (inclusive). Also allows the
    ability to gather data from a specific network sensor for a given monsoon year(s).

    :param network (required):    (string) - Sensor network to gather data from.
    :param start_year (required): (string) - Starting year in "YYYY" format.
    :param end_year:              (string) - End year (inclusive) of monsoon data date range in "YYYY" format.
    :param sensor:                (string) - Specific sensor id monsoon data is being requested.
    :param raw:                   (bool)   - Default is False. If True the data will run through our delta calculation to return
                                             totals for all sensors during the monsoon period. When used raw 
                                             adds datetime to return.
    :return JSON:                          - Returns monsoon data for given year(s).
    """

    # validate year input
    validate_year_input(start_year, end_year)

   # construct API request
    query_string = mon_conf.URL + \
        "/monsoon?network={}&startYear={}&endYear{}&sensor={}&raw={}".format(
            network, start_year, end_year, sensor, raw)
    # send request
    return get_data(query_string)


def sensor_metadata(network, sensor=""):
    """
    Retrieves sensor metadata such as name, location, and sensor type for a specific sensor id or entire network.

    :param network (required): (string) - Network to retrieve sensor information from as string.
    :param sensor:             (string) - Retrieve specific sensor. If not provided all sensors within a network will be returned.
    :return JSON:                       - Returns metadata for given sensor or all sensors in a network.
    """

    # construct API request
    query_string = mon_conf.URL + \
        "/sensors?network={}&sensor={}".format(network, sensor)

    # send request
    return get_data(query_string)


"""
Helper functions
"""


def login():
    """
    login() makes a post request to /login to get your API session token.

    :return: (string) - Session token.
    """
    r = requests.post("https://api.air.arizona.edu/login", {
        "username": mon_conf.USERNAME,
        "key": mon_conf.KEY
    })

    # check for status code >= 400 indicating authentication error
    if (r.status_code >= 400):
        sys.exit("Could not authenticate")

    # else, load auth token
    token = json.loads(r.text)

    # return access key
    return token['accessToken']


def get_data(url):
    """
    Common set of instructions used to perform requests for all API functions/routes.

    :param url (required): (string) - Composed URL string for specific data API routes.
    :return JSON:                   - Requested data.
    """

    # set headers
    headers = {"Authorization": "Bearer {}".format(login())}

    # make request
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)

    # return formatted data
    return data


def validate_date_input(start_date, end_date=""):
    """
    Date validation helper function to check for start_date and end_date
    order and proper date format of YYYY-MM-DD.

    :param start_date (required): (string) - Start date of provided range.
    :param end_date:              (string) - End date of provided range.
    :return sys.exit():                    - Return sys error string and exit if exception raised.
    """

    # error message string
    err_message = ""

    # validate start_date format
    try:
        datetime.datetime.strptime(start_date, "%Y-%m-%d")
    except:
        err_message += "start_date format '" + start_date + "' not correct\n"

    # if end_date parameter is provided validate format and date order
    if end_date:
        try:
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except:
            err_message += "end_date format '" + end_date + "' not correct\n"

        # make sure dates are provided in correct order
        if datetime.datetime.strptime(end_date, "%Y-%m-%d") < datetime.datetime.strptime(start_date, "%Y-%m-%d"):
            err_message += "end_date must be later that start_date\n"

    # if err_message contains a message, print message and halt
    if err_message:
        print("Exception(s) found:")
        sys.exit(err_message)


def validate_year_input(start_year, end_year=""):
    """
    Year validation helper function to check for start_year and end_year
    order and proper year format "YYYY".

    :param start_year (required): (string) - Start year of provided range in "YYYY" format.
    :param end_year:              (string) - End year of provided range in "YYYY" format.
    :return sys.exit():                    - Return sys error string and exit if exception is raised.
    """

    # error message string
    err_message = ""

    # validate start_year format
    try:
        datetime.datetime.strptime(start_year, "%Y")
    except:
        err_message += "start_year format '" + start_year + "' not correct\n"

    # if end_year parameter is provided validate format and year order
    if end_year:
        try:
            datetime.datetime.strptime(end_year, "%Y")
        except:
            err_message += "end_year format '" + end_year + "' not correct\n"

        # make sure years are provided in correct order
        if end_year < start_year:
            err_message += "end_year must be later that start_year\n"

    # if err_message contains a message, print message and halt
    if err_message:
        print("Exception(s) found:")
        sys.exit(err_message)
