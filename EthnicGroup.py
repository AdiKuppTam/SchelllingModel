
class EthnicGroup:
    def __init__(self, name,  value, size, bias, diversity, mobility=1):
        """
        the ethnic group is composed by name, size value and bias and diversity factors
        """
        self.name = name
        self.value = value
        self.size = size
        self.bias = bias
        self.diversity = diversity
        self.mobility = mobility

    def satisfied(self, result):
        """
        return true if the citizen is satisfied
        :param result: the proportion between the groups
        :return:

        """
        return self.diversity <= result <= self.bias
