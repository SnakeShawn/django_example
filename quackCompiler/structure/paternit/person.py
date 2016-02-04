
class person:

    __name__ = "Person"

    def __init__(self, sample, marker, allele1 = None, allele2 = None):
        self.__sample = sample
        self.__marker = marker
        self.__allele1 = allele1
        self.__allele2 = allele2

    @property
    def __gender__(self):
        return 'Male'
