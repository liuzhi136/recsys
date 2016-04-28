'''
 the ratio range is 1 up to 5
 if a user have 3 or more records, it means that this user prefer like the corresponding merchant 
 if a user have less than 3 records, it means that this user may be dislike the corresponding merchant
'''
import numpy as np
import pickle

# this method used to read data into a list
def formatData(filename):
    lines = [line.strip().split(',') for line in open(filename)]
    lines.pop(0);
#     for i in range(len(lines)):
#         lines[i] = [int(elem) for elem in lines[i]]
    return lines;

# this method used to extract a user's all merchant record
# the format is user:merchant_id,location,date
def extraUser_Merchant(data):
    users = set(data[:,0]);
    print("the number of user: ", len(users))
    user_merchant = dict()
    length = len(data[0])
    for user in users:
        user_merchant[user] = data[data[:,0] == user][:,1:length]
    return user_merchant

# this method used to extract merchants in a specific location
def extraLocation_merchant(data):
    locate_merchant = dict();
    for line in data:
        locate = line[-1]
        if ':' in locate:
            locate = locate.split(':')
            for l in locate:
                if not l in locate_merchant:
                    locate_merchant[l] = set()
                locate_merchant[l].add(line[0])
        else: 
            if not locate in locate_merchant:
                locate_merchant[locate] = set()
            locate_merchant[locate].add(line[0])
    return locate_merchant

# this method used to define the user rate from implicit feedback, the format is user:{merchant:number of consumption}
# ignore the location information
def extraUserRecord(user_merchant):
    user_rate = dict();
    for key,value in user_merchant.items():
        merchants = set(value[:,0].tolist())
        print(merchants)
        user_rate[key] = {};
        for merchant in merchants:
            user_rate[key][merchant] = sum(value[:,0] == merchant)
        print(key, ":", user_rate[key])
    return user_rate

def computeUserRates(user_record):
    user_rate = dict();
    for key,value in user_record.items():
        user_rate[key] = {};
        for subkey,subval in value.items():
            if subval >= 3: 
                user_rate[key][subkey] = 3 + (subval - 3)//3
                if user_rate[key][subkey] > 5: user_rate[key][subkey] = 5
            else: 
                user_rate[key][subkey] = subval;
        print(key, user_rate[key])
    return user_rate;

# this method used to compute the number of consumption for each merchant in a specific location
def calculateRateInLocation(location_merchants, originalData):
    location_mers_rate = dict();
#     for k,v in location_merchants.items():
#         location_mers_rate[k] = dict()
#         for merchant in v:
#             location_mers_rate[k][merchant] = 0
    for record in originalData:
        if not record[2] in location_mers_rate:
            location_mers_rate[record[2]] = dict()
        if not record[1] in location_mers_rate[record[2]]:
            location_mers_rate[record[2]][record[1]] = 0
        location_mers_rate[record[2]][record[1]] += 1
    return location_mers_rate

# this method used to store data which its' format is key:{subkey:value}
def storeData(data, toFile2):
    print('Begin to store!')
    with open(toFile2, 'wt') as handle:
        for key,val in data.items():
            line = str(key) + ":";
            for subkey,subval in val.items():
                line = line + str(subkey) + "-" + str(subval) + ","
            line = line[:-1]
            print(line)
            handle.write(line + '\n')
            
def store_dictData(data, toFile):
    with open(toFile, 'wt') as dicthandle:
        for k,v in data.items():
            line = k + ':'
            for val in v:
                line = line + val + '-'
            line = line[:-1]
            dicthandle.write(line + "\n");
            
if __name__ == '__main__':
    data = formatData('data/ijcai2016_koubei_train')
    location_merchant = pickle.load(open('data/location_merchant', 'rb'))
    location_merchant_rate = calculateRateInLocation(location_merchant, data)
    storeData(location_merchant_rate, 'data/location_merchant_rate_text')
    pickle.dump(location_merchant_rate, open('data/location_merchant_rate', 'wb'))
#     with open('data/merchantIds','rb') as merchantshandle:
#         merchants = pickle.load(merchantshandle)
#     merchants = [int(merchant) for merchant in merchants]
#     with open('data/user_merchant_py', 'rb') as user_merhandle:
#         user_merchants = pickle.load(user_merhandle)
#     print(sum(user_merchants[756066][:,0] == 2606))
#     user_rate = extraUserRecord(user_merchants)
#     print('Begin to store data!')
#     with open('data/rate', 'wb') as ratehandle:
#         pickle.dump(user_rate, ratehandle)
#     with open('data/user_records', 'rb') as user_merhandle:
#         user_records = pickle.load(user_merhandle)
#     user_rate = computeUserRates(user_records)
#     with open('data/user_rate', 'wb') as ratehandle:
#         pickle.dump(user_rate, ratehandle)
#     storeData(user_rate, 'data/user_rate_text')
#     data = np.array(data);
#     user_merchant = extraUser_Merchant(data)
#     storeData(user_merchant, 'data/user_merchant_diy', 'data/user_merchant_py')
    
