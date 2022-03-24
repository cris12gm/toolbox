class sRNAcons_sRNA2Species():
    def __init__(self, name, percentages, frequency, inspecies, notinspecies):
        self.name = name
        self.percentage = percentages
        self.frequency = frequency
<<<<<<< HEAD
        self.species = inspecies.replace(",","\n")


    def __str__(self):
        return "\t".join([self.name,self.percentage,self.frequency,self.species])
    def get_sorted_attr(self):
        return ["name","percentage","frequency","species"]

class sRNAcons_species2sRNA():
    def __init__(self, specie, Percentage, Frequency, srna, srnanotmapped):
        self.species = specie.split(";")[0]
=======

    def __str__(self):
        return "\t".join([self.name,self.percentage,self.frequency])
    def get_sorted_attr(self):
        return ["name","percentage","frequency"]

class sRNAcons_species2sRNA():
    def __init__(self, specie, Percentage, Frequency, srna, srnanotmapped):
        self.specie = specie.split(";")[0]
>>>>>>> upstream/develop
        self.percentage = Percentage
        self.frequency = Frequency

    def __str__(self):
<<<<<<< HEAD
        return "\t".join([self.species,self.percentage,self.frequency])
    def get_sorted_attr(self):
        return ["species","percentage","frequency"]
=======
        return "\t".join([self.specie,self.percentage,self.frequency])
    def get_sorted_attr(self):
        return ["specie","percentage","frequency"]
>>>>>>> upstream/develop

