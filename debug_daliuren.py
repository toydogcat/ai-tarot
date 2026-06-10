import sys
from kinliuren import Liuren

jieqi = "驚蟄"
cmonth = "五"
day_gz = "甲戌"
hour_gz = "庚子"

lr = Liuren(jieqi, cmonth, day_gz, hour_gz)
print("Sike:", lr.all_sike())
rel = lr.find_sike_relations()
print("Relations[0]:", rel[0])
print("Relations[2]:", rel[2])
print("Relations[7]:", rel[7])

print("zeike:", lr.zeike())
print("biyung:", lr.biyung())

res = lr.result(0)
print("Result Pattern:", res['格局'])
