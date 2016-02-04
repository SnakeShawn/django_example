
from structure.paternit.person import person


class Paternit:
    __name__ = "Paternit"

    def __init__(self, filename):
        self.__filename = filename
        self.__reader = open(filename, 'rt')
        line = self.__reader.readline()      # Get rid of the first line

        self.set = []
        while line:
            line = self.__reader.readline()
            dat = line.strip().split('\t')
            if len(dat) > 1:        # Avoid the empty line
                if len(dat) == 5:
                    u = person(dat[0],dat[1],dat[2],dat[3])
                elif len(dat) == 4:
                    u = person(dat[0],dat[1],dat[2],dat[2])
                self.set.append(u)
        self.__reader.close()

    @property
    def filename(self):
        """Get the alleles."""
        return self.__filename

