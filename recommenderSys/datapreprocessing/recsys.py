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
    interlen = len(intersection)
    # this express is significance strategy
    pc_u_v = (interlen/(interlen + 100)) * pc_u_v
    return pc_u_v

def computeNearestNei(u, user_rate, k):
    nearestNeis = {}
    user = user_rate[u]
    for v in user_rate.keys():
        if u == v: continue
        nearestNeis[v] = computeSim(user, user_rate[v])
    #sort this dict by each value of key:val pair, then get the top k element
    nearestNeisReverse = sorted(nearestNeis.items(), key=lambda d:d[1], reverse=True)
    nearestNeisReverse = dict(nearestNeisReverse[:k])
    return nearestNeisReverse
    
# Retrieve all merchants 
def unionMerchants(users, user_rate):
    merchants = set([merchant for user in users for merchant in user_rate[user].keys()])
    return merchants

def mostPopularMerchant(location, topN):
    location_merchant_rate = pickle.load(open('data/location_merchant_rate', 'rb'))
    merchant_local = copy.deepcopy(location_merchant_rate[location])
    rec_test = ''
    if len(merchant_local) <= 10:
        rec_test = ':'.join(list(merchant_local.keys()))
    else:
        result = []
        for i in range(1,11):
            merchant = max_ith(merchant_local, i)
            result.append(merchant)
        rec_test = ':'.join(result)
    return rec_test

def calculateRec(neighbors=5,*, testdata, user_rate, submitFile):
    with open(submitFile, 'wt') as submithandle:
        for test in testdata:
            rec_test = test[0] + ',' + test[1] + ','
            if not test[0] in user_rate:
                print('user have no record!')
                rec_test = rec_test + mostPopularMerchant(test[1], 10)
            else:
                print('user have some records!')
                # the following part is to compute the predicted result merchant
                nearestNeisReverse = computeNearestNei(test[0], user_rate, neighbors)
                merchants = unionMerchants(list(nearestNeisReverse.keys()), user_rate)
                prediction_merchantRate = dict();
                for merchant in merchants:
                    mer_rate = 0
                    for user in nearestNeisReverse.keys():
                        if merchant in user_rate[user].keys(): 
                            mer_rate = mer_rate + nearestNeisReverse[user] * user_rate[user][merchant]
                    prediction_merchantRate[merchant] = mer_rate
                #this meaning of this part is retrieve the top 10 merchant if predictedNum greater than 10 and
                # Use all element in result dict and retrieve the rest number of the top merchant if the predictedNum less than 10 and greater than 0 and
                # Retrieve top 10 popular merchants if  predictedNum equals 0
                predictedNum = len(prediction_merchantRate)
                if predictedNum > 10:
                    resultMer = [record[0] for record in sorted(prediction_merchantRate, key=lambda d:d[1], reverse=True)[0:11]]
                    rec_test = rec_test + ':'.join(resultMer)
                elif predictedNum < 10 and predictedNum > 0:
                    resultMer = [record[0] for record in sorted(prediction_merchantRate, key=lambda d:d[1], reverse=True)]
                    rec_test = rec_test + mostPopularMerchant(test[1], 10 - predictedNum)
                    rec_test = rec_test + ':'.join(resultMer)
                else:
                    rec_test = rec_test + mostPopularMerchant(test[1], 10)
            print(rec_test)
            submithandle.write(rec_test + '\n')
# this method used to find the ith largest element in a dict
def max_ith(data, i):
    sortedData = sorted(data.items(), key=lambda d:d[1], reverse=True)
    i_max_merchant = sortedData[i-1][0]
#     for k,v in data.items():
#         if i_max_rate < v: i_max_rate = v; i_max_merchant = k
#     data.pop(i_max_merchant)
    return i_max_merchant;

if __name__ == '__main__':
    user_rates = pickle.load(open('data/user_rate', 'rb'))
    testusers = [line.strip().split(',') for line in open('data/ijcai2016_koubei_test')]
    testusers.pop(0)
    calculateRec(testdata=testusers, user_rate=user_rates, submitFile='prediction/submission.csv')