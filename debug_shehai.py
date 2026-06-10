import sys
from kinliuren import Liuren

class DebugLiuren(Liuren):
    def shehai_debug(self):
        shangke = self.find_sike_relations()[0]
        print("shangke:", shangke)
        print("rel[9]:", self.find_sike_relations()[9])
        print("rel[2].count('尅'):", self.find_sike_relations()[2].count("尅"))
        print("rel[2].count('被尅'):", self.find_sike_relations()[2].count("被尅"))
        print("rel[5]:", self.find_sike_relations()[5])
        print("rel[7][2][0][0]:", self.find_sike_relations()[7][2][0][0])
        print("rel[7][2][1][0]:", self.find_sike_relations()[7][2][1][0])
        print("compare_shehai_number:", self.compare_shehai_number())

lr = DebugLiuren('立秋', '五', '癸亥', '甲寅')
lr.shehai_debug()
