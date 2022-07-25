import sys
import requests
import json
import datetime

"""
Collection of wrapper functions for monsoon API route requests.
"""

class MonsoonAPI: 
    API_BASE_URL = "https://api.air.arizona.edu"

    def __init__(self, username, api_key):
        self.__username = username 
        self.__api_key = api_key 
        self.__headers = None
        #this method sets headers
        self.__login() 

    def precip_totals(self, start_date, end_date, networks):
        """
        precip_totals() returns the sum of rainfall totals across each sensor in a given network(s) 
        for a provided date range.

        :param start_date (required): (string) - Range start date in "YYYY-MM-DD" format.
        :param end_date (required):   (string) - Range end date in "YYYY-MM-DD" format.
        :param network(s) (required): (string) - The network or networks to be queried. Multiple networks must be separated by a hyphen (-). ex. "pima_fcd-rainlog"
        :return JSON:                          - Returns total rainfall value totals for sensors in the provided network(s).
        """

        # validate date input
        self.__validate_date_input(start_date, end_date)

        # construct API request
        # base monsoon url returns precipitation totals
        url_string = ""
        payload = {'startDate':start_date, 'endDate':end_date, 'network':networks}

        # send request and return result
        return self.__get_data(url_string, payload) 
       
       
    def sensor_readings(self, network, start_date, end_date=None, sensor=None):
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
        self.__validate_date_input(start_date, end_date)

        # construct API request
        url_string = "/readings"
        payload = {'network':network, 'startDate':start_date, 'endDate':end_date, 'sensor':sensor}
        
        # send request and return result
        return self.__get_data(url_string, payload)


    def flood_data(self, network, start_date, end_date=None, sensor=None):
        """
        Flood data route makes an API call for data between the start date and end date 
        and optionally a sensor.
        :param network    (required): (string) - sensor network only pima and maricopa 
        :param start_date (required): (string) - format "YYYY-MM-DD"
        :param end_date:              (string) - format "YYYY-MM-DD"
        :param sensor:                (string) - specific sensor ID 
        """

        # validate date input
        self.__validate_date_input(start_date, end_date)

        # construct API request
        url_string = "/flood"
        payload = {'network':network, 'startDate':start_date, 'endDate':end_date, 'sensor':sensor}

        # send request and return result
        return self.__get_data(url_string, payload)


    def monsoon_data(self, network, start_year, end_year=None, sensor=None, raw=None): 
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
        self.__validate_year_input(start_year, end_year)

        # construct API request
        url_string = "/monsoon"
        payload = {'network':network, 'startYear':start_year, 'endYear':end_year, 'sensor':sensor, 'raw':raw}

        # send request and return result
        return self.__get_data(url_string, payload)


    def sensor_metadata(self, network, sensor=None):
        """
        Retrieves sensor metadata such as name, location, and sensor type for a specific sensor id or entire network.

        :param network (required): (string) - Network to retrieve sensor information from as string.
        :param sensor:             (string) - Retrieve specific sensor. If not provided all sensors within a network will be returned.
        :return JSON:                       - Returns metadata for given sensor or all sensors in a network.
        """

        # construct API request
        url_string = "/sensors"
        payload = {'network':network, 'sensor':sensor}

        # send request and return result
        return self.__get_data(url_string, payload)


    """
    Helper functions
    """

    def __login(self):
        """
        login() makes a post request to /login to get your API session token.

        :return: (string) - Session token.
        """
        req = requests.post(MonsoonAPI.API_BASE_URL+"/login", {
            "username": self.__username,
            "key": self.__api_key
        })

        # check for status code >= 400 indicating authentication error
        if (req.status_code >= 400):
            sys.exit("Could not authenticate")

        # else, load auth token
        token = json.loads(req.text)
        headers = {
            "Authorization": "Bearer {}".format(token['accessToken'])
        }
        # setting headers 
        self.__headers = headers 


    def __get_data(self, url_string, payload):
        """
        Common set of instructions used to perform requests for all API methods/routes.

        :param url_string (required): (string)     - String used for specific data API routes.
        :param payload    (required): (dictionary) - Dictionary of parameters.
        :return JSON:                              - Requested data.
        """

        # build and make request
        req = requests.get(MonsoonAPI.API_BASE_URL+url_string, payload, headers=self.__headers)
        
        # return formatted data
        return json.loads(req.text)


    def __validate_date_input(self, start_date, end_date=None):
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
        if end_date is not None:
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


    def __validate_year_input(self, start_year, end_year=None):
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
        if end_year is not None:
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
