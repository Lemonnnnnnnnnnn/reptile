import pymongo
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib

matplotlib.rc("font", family='FangSong')

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client["lagou"]
mycol = db["lagou_items"]

educationArr = []
cityArr = []
companySizeArr = []
skillLablesArr = []
workYearArr = []
salaryArr = []
for i in mycol.find():
    educationArr.append(i['education'][0])
    cityArr.append(i['city'][0])
    companySizeArr.append(i['companySize'][0])
    skillLablesArr.append(i['skillLables'][0])
    workYearArr.append(i['workYear'][0])
    salaryArr.append(i['salary'][0])

statistics = pd.value_counts(cityArr)
Range = statistics.index.values[:5]
Number = statistics.values[:5]
plt.suptitle('城市')
plt.bar(Range, Number)
plt.savefig('城市.png', bbox_inches='tight')
plt.clf()

statistics = pd.value_counts(companySizeArr)
Range = statistics.index.values[:5]
Number = statistics.values[:5]
plt.suptitle('公司规模')
plt.bar(Range, Number)
plt.savefig('公司规模.png', bbox_inches='tight')
plt.clf()

statistics = pd.value_counts(educationArr)
Range = statistics.index.values[:5]
Number = statistics.values[:5]
plt.suptitle('学历')
plt.bar(Range, Number)
plt.savefig('学历.png', bbox_inches='tight')
plt.clf()

statistics = pd.value_counts(workYearArr)
Range = statistics.index.values[:5]
Number = statistics.values[:5]
plt.suptitle('工作时间')
plt.bar(Range, Number)
plt.savefig('工作时间.png', bbox_inches='tight')
plt.clf()

statistics = pd.value_counts(salaryArr)
Range = statistics.index.values[:5]
Number = statistics.values[:5]
plt.suptitle('薪资')
plt.bar(Range, Number)
plt.savefig('薪资.png', bbox_inches='tight')
plt.clf()
