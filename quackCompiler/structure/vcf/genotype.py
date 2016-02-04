from enum import Enum

class RES(Enum):
    '''
    Result of Compare. The result has three situations.
    '''
    notEq = 0       # not matching
    exactEq = 1     # exact matching
    fuzzyEq = 2     # fuzzy matching

class genotype(object):
    '''

    '''

    __name__ = "genotype"

    def __init__(self, alleles):
        alleles.sort()
        self.__alleles = alleles

    def __str__(self):
        ret = "{alleles: " + ('').join(self.__alleles) + "}"
        return ret

    def __getitem__(self, key):
        return self.__alleles[key]

    def __setitem__(self, key, value):
        self.__alleles[key] = value

    @property
    def alleles(self):
        """Get the alleles."""
        return self.__alleles

    def addAllele(self, allele):
        self.__alleles.append(allele)

    def testGenotype(self, gStr, strict=None):
        """

        :param gStr:
        :param strict:
        :return:
        """
        compRes = self.compare(gStr)

        if compRes == RES.notEq:
            return False
        elif compRes  == RES.exactEq:
            if strict == None or strict == 1:
                return True
            else:
                return False
        elif compRes == RES.fuzzyEq:
            if strict == None:
                return True
            else:
                return False
        else:
            print('ERROR!')


    def compare(self,alleles):
        '''
        :param alleles: the input alleles(allele1,allele2)
        :return: RES
        '''
        allArr = alleles.replace(' ','')
        allArr = allArr.split(',')

        allArr.sort()
        self.__alleles.sort()
        if len(allArr) == len(self.__alleles):
            if allArr == self.__alleles:
                return RES.exactEq
            else:
                return RES.notEq
        elif len(allArr) != len(self.__alleles):
            return RES.notEq
        else:
            print('ERROR!')