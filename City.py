import numpy as np
import copy
import random
import time


class City:

    def __init__(self, city_size, population):

        # here we save all the available space
        self.__available_space = [(a, b) for a in range(city_size[0]) for b in range(city_size[1])]

        # with this dictionary, we can get the color from the value
        self.__population = population

        # the matrix that represents the city
        self.__matrix = np.zeros(shape=([city_size[0], city_size[1]]), dtype=int)

        # this is the list of all the possible locations in the city
        self.__location_list = [(a, b) for a in range(city_size[0]) for b in range(city_size[1])]

        self.__city_size = city_size

        # number of milliseconds until set
        self.__time = 0

        # here we set the initial city span
        self.__generate_matrix()

    def __generate_matrix(self):
        """
        generate the matrix with the initial location of the citizens
        :return:
        """

        for group in self.__population.keys():

            pop_size = self.__population[group].size

            # here we randomly choose locations on the board
            my_loc = random.sample(self.__available_space, pop_size)
            # here we settle the citizens
            for location in my_loc:
                self.__matrix[location[0], location[1]] = self.__population[group].value
                # now we delete the used location from the free locations
                self.__available_space.remove(location)

    def __can_move(self, location):
        """
        simply gets the value according to the location
        :param location: the location of the desired matrix
        :return:
        """
        return self.__population[self.__matrix[location[0], location[1]]].mobility >= random.uniform(0, 1)

    def __get_value(self, location):
        """
        simply gets the value according to the location
        :param location: the location of the desired matrix
        :return:
        """
        return self.__matrix[location[0], location[1]]

    def __check_for_satisfaction(self, location, my_value=None):
        """
        :param location: tuple with the location inspected
        :param my_value - if we check the location for an existing fella, this argument will contain it's value
        :return: True if satisfied at the current location, false else
        """
        if my_value is None:
            my_value = self.__get_value(location)

        # means this location is not occupied
        if my_value == 0:
            return True

        color = self.__population[my_value]

        # here we check the surrounding of the location
        different, like_me = self.__look_around(location, my_value)

        if not different:  # if we have no different neighbours
            if not like_me:  # this is a no-neighbours spot
                return True
            else:  # if we have only neighbours like me
                return color.satisfied(0)
        else:
            return color.satisfied(different / (like_me + different))

    def __get_neighbours_locations(self, location):
        """
        gets a list of the neighbours of an specific location
        :param location: the location
        :return:
        """
        # we also make sure that we don't accidentally overflowing the matrix

        lst = [(a, b) for a in range(max(location[0] - 1, 0), min(location[0] + 2, self.__city_size[0]))
               for b in range(max(location[1] - 1, 0), min(location[1] + 2, self.__city_size[1]))]
        return [x for x in lst if x not in self.__available_space]

    def __look_around(self, location, my_value):
        """
        here we load what kind of neighbours we have
        :param location: the location looked at
        :param my_value: the value to compare to
        :return: number of neighbours of every kind
        """
        like_me = 0
        different = 0

        # iterating over the neighbours.
        neighbours_locations = self.__get_neighbours_locations(location)

        for (i, j) in neighbours_locations:

            # means, the block is empty or it's us
            if self.__matrix[i, j] == 0 or (i, j) == location:
                continue

            # means we have people like me in this block
            elif self.__matrix[i, j] == my_value:
                like_me += 1

            # means we have people like me in this block
            else:
                different += 1
        return different, like_me

    def __move(self, old_location):
        """
        :param old_location: the location we want to move from
        :return: true if successfully moved, false else
        """

        value = self.__get_value(old_location)

        try:
            # iterating over the available space
            new_location = random.choice(self.__available_space)
            # moves the thing around
            self.__matrix[new_location[0], new_location[1]] = copy.copy(value)
            self.__matrix[old_location[0], old_location[1]] = 0

            # adds the available location to the list
            self.__available_space.remove(new_location)
            self.__available_space.append(old_location)

            return new_location
        except IndexError:
            return -1, -1

    def __schelling_loop(self):
        """
        here is the iteration itself
        :return:
        """
        location_list = [x for x in self.__location_list if x not in self.__available_space]
        unhappy = []
        while location_list:
            # here we randomly choose location on the board
            location = random.choice(location_list)

            # if the citizen is happy or this location is empty,
            # we can delete it from the list:
            if self.__check_for_satisfaction(location):
                location_list.remove(location)

            # means the citizen is not satisfied
            else:
                unhappy.append(location)
                location_list.remove(location)

        unhappy = [x for x in unhappy if self.__can_move(x)] # here we remove anyone with lack of mobility
        if unhappy:
            while unhappy:
                citizen = random.choice(unhappy)
                if self.__move(citizen) == (-1, -1):  # means the city is totally full
                    break
                else:
                    unhappy.remove(citizen)
            return True
        return False

    def apply_schelling(self):
        """
        here we apply the module itself.
        :return:
        """
        start_time = time.time()
        # here we crate a copy of the original list
        # location_list = [x for x in self.__location_list if x not in self.__available_space]
        moved = self.__schelling_loop()

        while moved:  # means, if someone has been moved in this iteration
            moved = self.__schelling_loop()

        end_time = time.time()
        print("experiment complete\n")
        return self.__compute_segregation(), (end_time - start_time)

    def __compute_segregation(self):
        """
        here we compute how bad is the segregation after the module operation
        :return: the segregation factor
        """
        total = sum(value.size for value in self.__population.values())  # total number of citizens
        segregate = 0  # number of citizens that are surrounded only by people like them
        for location in self.__location_list:
            value = self.__get_value(location)
            if value:  # means there is someone living in this location
                different, like_me = self.__look_around(location, value)

                if different == 0 and like_me > 0:  # the citizen only surrounded by people like him
                    segregate += 1

        if segregate > 0:  # means the is someone who is not segregated
            return (segregate / total) * 100
        else:
            return 0
