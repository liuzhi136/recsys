'''
Created on 2016年4月26日

@author: leo
'''
import pickle
import numpy as np
import copy

# The format of u and v are user:{merchant-rate, ..., merchant-rate}（使用皮尔森相似度）
def computeSim(u, v):
    merchant_u = set(u.keys())
    merchant_v = set(v.keys())
    print(merchant_u ,' ', merchant_v)
    intersection = merchant_u & merchant_v
    if len(intersection) == 0: return 0;
    umean = np.mean(list(u.values())); vmean = np.mean(list(v.values()))
    numeru = 0; denou = 0; denov = 0;
    for merchant in intersection:
        numeru = numeru + (u[merchant] - umean) * (v[merchant] - vmean)
        denou = denou + (u[merchant] - umean) ** 2
        denov = denov + (v[merchant] - vmean) ** 2
    pc_u_v = numeru / np.sqrt(denou * denov)
    return pc_u_v

def computeNearestNei():

def calculateRec(neighbors=5,*, testdata, user_rate, submitFile):
    location_merchant_rate = pickle('data/location_merchant_rate', 'rb')
    with open(submitFile, 'wt') as submithandle:
        for test in testdata:
            if not test[0] in user_rate:
                merchant_local = copy.deepcopy(location_merchant_rate[test[0]])
                rec_test = test[0] + ',' + test[1] + ','
                if len(merchant_local) <= 10:
                    for merchant in merchant_local.keys():
                        rec_test = rec_test + merchant + ':'
                    rec_test = rec_test[:-1]
                else:
                    for i in range(1,1,11):
                        merchant = max_ith(merchant_local,i)
                        rec_test = rec_test + merchant + ':'
                print(rec_test)
                submithandle.write(rec_test + '\n')
            else:
                testUser = 
    
# this method used to find the ith largest element in a dict
def max_ith(data, i):
    i_max_merchant = ''; i_max_rate = 0
    for k,v in data.items():
        if i_max_rate < v: i_max_rate = v; i_max_merchant = k
    data.pop(i_max_merchant)
    return i_max_merchant,i_max_rate;

if __name__ == '__main__':
    location_merchant_rate = pickle.load(open('data/location_merchant_rate', 'rb'))
    print(location_merchant_rate['352'])
    merchant_rate = copy.deepcopy(location_merchant_rate['352'])
    merchant,rate = max_ith(location_merchant_rate['352'],1)
    print('the number of historical consumption of merchant {0} is {1}'.format(merchant, rate))
    
    