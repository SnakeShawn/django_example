import vcf

from .genotype import genotype


class VCFReader:

    __name__ = "VCFReader"

    def __init__(self, filename):
        self.filename = filename

    def getByPos(self, pos):
        """
        Get a record by a position (chromosome, position).
        :param pos: the input Position (chromosome, position)
        :return: record: _Record in PyVcf.
        """
        vcf_reader = vcf.Reader(filename=self.filename)

        reader = vcf_reader.fetch(str(pos[0]), pos[1]-1, pos[1])
        record = None
        
        for re in reader:
            record = re
            break
        return record

    def getByPoses(self,pos):
        vcf_reader = vcf.Reader(filename=self.filename)

        reader = vcf_reader.fetch(str(pos[0]), pos[1]-1, pos[1])
        record = None
        for re in reader:
            record = re
        return record

    def getAllelesByPos(self, pos):
        '''
        :param pos: a list of position ((chromosome1, position1),(chromosome2, position2),...)
        :return: a list of genotype
        '''
        vcf_reader = vcf.Reader(filename=self.filename)
        
        Record_Result = []
        
        for i in range(len(pos)):               # Store the records
            record = None
            for re in vcf_reader.fetch(str(pos[i][0]), pos[i][1]-1, pos[i][1]):
                record = re
            Record_Result.append(record)
        geno_result = []
        for i in range(len(Record_Result)):     # Split the 'GT',get the array and then match the base
            if Record_Result[i] == None:        # Invalid coordinate
                geno_result.append(None)
                continue

            gt_temp = Record_Result[i].samples[0]['GT']

            gt_arr1 = gt_temp.split('/')
            gt_arr2 = gt_temp.split('|')
            if len(gt_arr1) > len(gt_arr2):
                gt_arr = gt_arr1
            else:
                gt_arr = gt_arr2
        
            alleles = []
            for j in range(len(gt_arr)):
                if gt_arr[j] == '0':
                    alleles.append(Record_Result[i].REF.__str__())
                elif gt_arr[j] == '.':
                    alleles.append('.')
                else:
                    alleles.append(Record_Result[i].ALT[(int(gt_arr[j])-1)].__str__())
            g = genotype(alleles)
            geno_result.append(g)
        
        return geno_result



    def getAllelesByPos_INVALID(self, pos):
        '''
        INVALID

        :param pos:
        :return:
        '''
        vcf_reader = vcf.Reader(filename=self.filename)
        print(self.filename)

        Record_Result = []
        for i in range(len(pos)):       # Store the records
            for record in vcf_reader.fetch(str(pos[i][0]), pos[i][1]-1, pos[i][1]):
                if record.is_snp:       # just the snp alleles.
                    Record_Result.append(record)
                else:
                    print('!WARNING:chrom ('+str(pos[i][0])+') at ('+str(pos[i][1])+') is not snp!')
                    #raise Exception('chrom ('+str(pos[i][0])+') at ('+str(pos[i][1])+') is not snp!')
        result = []
        geno_result = []
        for j in range(len(Record_Result)):     # In fact, '.' would not be match, because it's not snp.
            gt_temp = Record_Result[j].samples[1]['GT']
            alleles = ''
            if gt_temp[0] == '0':
                alleles = Record_Result[j].REF.__str__()
            elif gt_temp[0] == '1':
                alleles = Record_Result[j].ALT[0].__str__()
            elif gt_temp[0] == '2':
                alleles = Record_Result[j].ALT[1].__str__()
            elif gt_temp[0] == '.':
                print('None')
            if gt_temp[-1] == '0':
                alleles += Record_Result[j].REF
            elif gt_temp[-1] == '1':
                alleles += Record_Result[j].ALT[0].__str__()
            elif gt_temp[-1] == '2':
                alleles += Record_Result[j].ALT[1].__str__()
            elif gt_temp[-1] == '.':
                print('None')
            if alleles == '':
                print(Record_Result[j].POS)

            alleles = ''.join((lambda x:(x.sort(),x)[1])(list(alleles)))    # sort the alleles(as a string)
            g = genotype(alleles)
            geno_result.append(g)
            result.append(alleles)
        return geno_result

