from City import *
from EthnicGroup import EthnicGroup
import pandas as pd

TIME_STR = 'Time'

SEGREGATION_STR = 'Segregation'

VALUE_STR = 'Value'

PARAMETER_STR = 'Parameter'

CITY_SIZE = (30, 30)

DEFAULT_Y_NAME = "yellow"
DEFAULT_Y_VALUE = 1
DEFAULT_B_NAME = "blue"
DEFAULT_B_VALUE = 2
DEFAULT_GROUP_SIZE = 250
DEFAULT_BIAS = 0.25
DEFAULT_DIVERSITY = 0


def average(lst):
    """
    calculates the average of the list
    :param lst: the list
    :return: the average
    """
    return sum(lst) / len(lst)


def run_in_loop(the_city):
    """
    runs every experiment 100 times to get not-poisoned perspective
    :param the_city:
    :return:
    """
    time_res = []
    seg_res = []
    for i in range(100):
        segregation, time_taken = the_city.apply_schelling()
        time_res.append(time_taken)
        seg_res.append(segregation)
    return average(seg_res), average(time_res)


def run_diversity():
    """
    runs the experiment with diversity as variable
    :return: nothing
    """
    data_frame = pd.DataFrame()

    parameters = []
    values = []
    segregations = []
    times = []

    diversity = 0
    while diversity < DEFAULT_BIAS:
        yellow = EthnicGroup(DEFAULT_Y_NAME, DEFAULT_Y_VALUE, DEFAULT_GROUP_SIZE, DEFAULT_BIAS + 0.125, diversity)
        blue = EthnicGroup(DEFAULT_B_NAME, DEFAULT_B_VALUE, DEFAULT_GROUP_SIZE, DEFAULT_BIAS + 0.125, diversity)
        the_city = City(city_size=CITY_SIZE, population={1: yellow, 2: blue})
        segregation, time_taken = run_in_loop(the_city)

        parameters.append("Diversity")
        values.append(diversity)
        segregations.append(segregation)
        times.append(time_taken)

        diversity += 0.125

    data_frame[PARAMETER_STR] = parameters
    data_frame[VALUE_STR] = values
    data_frame[SEGREGATION_STR] = segregations
    data_frame[TIME_STR] = times

    return data_frame


def run_bias():
    """
    runs the experiment with bias as variable
    :return: nothing
    """
    data_frame = pd.DataFrame()

    parameters = []
    values = []
    segregations = []
    times = []

    bias = DEFAULT_BIAS

    while bias <= 1:
        yellow = EthnicGroup(DEFAULT_Y_NAME, DEFAULT_Y_VALUE, DEFAULT_GROUP_SIZE, bias, DEFAULT_DIVERSITY)
        blue = EthnicGroup(DEFAULT_B_NAME, DEFAULT_B_VALUE, DEFAULT_GROUP_SIZE, bias, DEFAULT_DIVERSITY)
        the_city = City(city_size=CITY_SIZE, population={1: yellow, 2: blue})
        segregation, time_taken = run_in_loop(the_city)

        parameters.append("Bias")
        values.append(bias)
        segregations.append(segregation)
        times.append(time_taken)

        bias += 0.125

    data_frame[PARAMETER_STR] = parameters
    data_frame[VALUE_STR] = values
    data_frame[SEGREGATION_STR] = segregations
    data_frame[TIME_STR] = times
    return data_frame


def run_ratio():
    """
    runs the experiment with diversity as variable
    :return: nothing
    """
    data_frame = pd.DataFrame()

    parameters = []
    values = []
    segregations = []
    times = []

    yellow_size = 0
    blue_size = 500
    while blue_size >= yellow_size:
        yellow = EthnicGroup(DEFAULT_Y_NAME, DEFAULT_Y_VALUE, yellow_size, DEFAULT_BIAS, DEFAULT_DIVERSITY)
        blue = EthnicGroup(DEFAULT_B_NAME, DEFAULT_B_VALUE, blue_size, DEFAULT_BIAS, DEFAULT_DIVERSITY)
        the_city = City(city_size=CITY_SIZE, population={1: yellow, 2: blue})
        segregation, time_taken = run_in_loop(the_city)

        parameters.append("Ratio")
        values.append((yellow_size / blue_size))
        segregations.append(segregation)
        times.append(time_taken)

        yellow_size += 50
        blue_size -= 50

    data_frame[PARAMETER_STR] = parameters
    data_frame[VALUE_STR] = values
    data_frame[SEGREGATION_STR] = segregations
    data_frame[TIME_STR] = times
    return data_frame


def run_occupation():
    """
    runs the experiment with diversity as variable
    :return: nothing
    """
    data_frame = pd.DataFrame()

    parameters = []
    values = []
    segregations = []
    times = []

    yellow_size = 0
    blue_size = 0
    total_size = CITY_SIZE[0] * CITY_SIZE[1]
    while blue_size + yellow_size <= total_size:
        yellow = EthnicGroup(DEFAULT_Y_NAME, DEFAULT_Y_VALUE, yellow_size, DEFAULT_BIAS, DEFAULT_DIVERSITY)
        blue = EthnicGroup(DEFAULT_B_NAME, DEFAULT_B_VALUE, blue_size, DEFAULT_BIAS, DEFAULT_DIVERSITY)
        the_city = City(city_size=CITY_SIZE, population={1: yellow, 2: blue})
        segregation, time_taken = run_in_loop(the_city)
        parameters.append("Occupation")
        values.append((yellow_size + blue_size) / total_size)
        segregations.append(segregation)
        times.append(time_taken)
        yellow_size += 50
        blue_size += 50

    data_frame[PARAMETER_STR] = parameters
    data_frame[VALUE_STR] = values
    data_frame[SEGREGATION_STR] = segregations
    data_frame[TIME_STR] = times
    return data_frame


def run_mobility():
    data_frame = pd.DataFrame()

    values = []
    segregations = []
    times = []

    mobility = 0
    while mobility <= 1:
        yellow = EthnicGroup(DEFAULT_Y_NAME,
                             DEFAULT_Y_VALUE,
                             DEFAULT_GROUP_SIZE,
                             DEFAULT_BIAS,
                             DEFAULT_DIVERSITY,
                             mobility)
        blue = EthnicGroup(DEFAULT_B_NAME,
                           DEFAULT_B_VALUE,
                           DEFAULT_GROUP_SIZE,
                           DEFAULT_BIAS,
                           DEFAULT_DIVERSITY,
                           mobility)
        the_city = City(city_size=CITY_SIZE, population={1: yellow, 2: blue})
        segregation, time_taken = run_in_loop(the_city)
        values.append(mobility)
        segregations.append(segregation)
        times.append(time_taken)
        mobility += 0.1

    # append empty columns to an empty DataFrame
    data_frame[VALUE_STR] = values
    data_frame[SEGREGATION_STR] = segregations
    data_frame[TIME_STR] = times

    return data_frame


def run_series():
    """
    this function runs all the experiment in a row, one after the other, and creates a proper csv
    :return:
    """

    df1 = run_bias()
    df2 = run_diversity()
    df3 = run_ratio()
    df4 = run_occupation()

    df = pd.concat([df1, df2, df3, df4], ignore_index=True)
    df.to_csv("experiment_result.csv")


def run_mobility_exp():
    """
    this function runs all the experiment in a row, one after the other, and creates a proper csv
    :return:
    """

    df = run_mobility()
    with open("experiment_result.csv", "w") as f:
        df.to_csv(f)


