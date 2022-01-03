class sRNAcons_sRNA2Species():
    def __init__(self, name, percentages, frequency, inspecies, notinspecies):
        self.name = name
        self.percentage = percentages
        self.frequency = frequency

    def __str__(self):
        return "\t".join([self.name,self.percentage,self.frequency])
    def get_sorted_attr(self):
        return ["name","percentage","frequency"]

class sRNAcons_species2sRNA():
    def __init__(self, specie, Percentage, Frequency, srna, srnanotmapped):
        self.species = specie.split(";")[0]
        self.percentage = Percentage
        self.frequency = Frequency

    def __str__(self):
        return "\t".join([self.species,self.percentage,self.frequency])
    def get_sorted_attr(self):
        return ["species","percentage","frequency"]

