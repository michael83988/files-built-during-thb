#!/usr/bin/env python
# coding: utf-8

# # 自行開發模組(module)
# 
# 
# 一個模組(module)就是一個python檔案。建立module的目的:
# - 將關聯性較高的程式碼統一放在一個地方，便於維護。需要使用的時候，可以用`from ... import...`來達成。
# - 或是直接`import <module name>`來使用。
# 
# 
# module中，可以包含`function`以及`class`。在import後面接上要使用的function或是class名稱即可。
# 
# 

# <font color="chocolate">另一個概念為`套件(package)`，就是一個資料夾，裡面可以放很多個module，且擁有`__init__.py`檔案，其中可以撰寫package初始化的程式碼。</br>
# package的出現是為了當相似的module很多時，作為組織module用。
# 使用package的方法也是`from ... import...`或`import ...`。</br>
# `...`可以是module名稱，或是`<module name>.<function or class>`。
# </font>

# 使用jupyter notebook開發出來的python檔，並非單純的python檔，而是json格式。

# In[4]:


def for_test(*args):
    print('成功引用Apriori module囉!')
    print('args: ', args)


# ## 需要將.ipynb轉成.py才能夠被其他python檔給import做使用!!

# In[3]:



# In[32]:


#global variable定義
support = 0.6
confidence = 0.6
size = 2
itemset_dict = {}  #用來存放frequent itemset的dict。每個itemset用tuple來存放; 存size = 1 開始
#temp_dict = {}  #用來存放itemset()回傳的list，若為空list，則得到的frequent itemset list 為 itemset_list
frequent_itemset_list = []


# # 建立Apriori Algorithm

# In[50]:


import pandas as pd






#support的計算 -> bug!
def supp(item, df):
    result = {}
    item = tuple(item)
    total_row = len(df.index)
    for i in range(total_row):
        temp_row = df.iloc[i]
        #print(temp_row)
        
        if(all(k in temp_row.values for k in item) and (tuple(item) not in list(result.keys()))):
            result[tuple(item)] = 1
            #print('有建立')
        elif(all(k in temp_row.values for k in item) and (tuple(item) in list(result.keys()))):
            result[tuple(item)] = result[tuple(item)] + 1
            #print('加1')
        else:
            #print('不符合')
            #print([k for k in key])
            continue
    
    #print('內部統計結果dict: ',inner_temp_dict)
    #print('supp中的result: ', result)
    return result[tuple(item)] / total_row if item in list(result.keys()) else 0

#confidence計算
def conf(x, item, df):
    #print('x: ', x)
    #print('item: ', item)
    return supp(list(item), df) / supp(list(x), df) 



#lift計算
def lift(x, y, item, df):
    #print('lift的item: ', item)
    #print('supp(item, df): ', supp(list(item), df))
    #print('supp(x, df): ', supp(list(x), df))
    #print('supp(y, df): ', supp(list(y), df))
    return supp(list(item), df) / (supp(list(x), df) * supp(list(y), df))



#增加itemset size並且做篩選
def itemset(inner_size, items, df):
    #print('成功呼叫itemset() function')
    #print('傳入的itemset: ',items)
    
    """
    #將小於support值的itemset給濾掉
    print('itemset內的support: ', support)
    filtered_item_dict = filter(lambda x:(x[1] / len(df.index) >= support), items.items())
    filtered_item_dict = dict(filtered_item_dict)
    #print('過濾後: ',filtered_item_dict)
    """
    
    #建立size+1 的itemset_dict
    keys = list(items.keys())
    #print('keys: ', keys)
    
    temp_keys_list = []
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            combined_key_list = list(keys[i]) + list(keys[j])
            #print('組合的key: ',combined_key_list)
            
            combination_key_list = tuple(set(combined_key_list))
            temp_keys_list.append(combination_key_list)
    #print('排列組合後的keys: ', temp_keys_list)
    
    #排除size != size的組合，且把重複的組合留下唯一一組
    filtered_keys_list = list(set([key for key in temp_keys_list if len(key) == inner_size]))
    #print('itemset符合size的keys: ',filtered_keys_list)
    
    #與原dataframe比較，針對每個key(tuple構成的)去做統計(計數)
    inner_temp_dict = {}
    total_row = len(df.index)
    for i in range(total_row):
        temp_row = df.iloc[i]
        #print(temp_row)
        for key in filtered_keys_list:
            if(all(k in temp_row.values for k in key) and (key not in list(inner_temp_dict.keys()))):
                inner_temp_dict[key] = 1
                #print('有建立')
            elif(all(k in temp_row.values for k in key) and (key in list(inner_temp_dict.keys()))):
                inner_temp_dict[key] = inner_temp_dict[key] + 1
                #print('加1')
            else:
                #print('不符合')
                #print([k for k in key])
                continue
    
    #print('itemset內部統計結果dict: ',inner_temp_dict)
    
    #過濾掉<support的部分
    filtered_item_dict = filter(lambda x:(x[1] / len(df.index) >= support), inner_temp_dict.items())
    inner_temp_dict = dict(filtered_item_dict)
    #print('itemset內部過濾後的dict: ', inner_temp_dict)
    
    #回傳True or False決定是否要繼續計算
    if(inner_temp_dict != {}):
        global itemset_dict
        itemset_dict = inner_temp_dict.copy()
        
        global size
        size = inner_size + 1
        return True
    else:
        print('Frequent itemset建立完成 ...')
        return False

    
#定義組合的function -> 用於產生所有的S組合
#lt: 輸入進來的list; n: 組合的元素有n個
def combine(lt, n):
    #print('呼叫combine')
    answers = []
    tmp_item = [0] * n
    def next_it(lt_lbound, ni):
        if(ni == n):
            answers.append(tmp_item.copy())
            return
        for li in range(lt_lbound, len(lt)):
            tmp_item[ni] = lt[li]
            next_it(li + 1, ni + 1)
    next_it(0, 0)
    return answers


    
#從itemset(I)中計算 S -> I-S 的機率是否 >= confidence。留下符合的並return
def compare_with_confidence(freq_list, df):
    print('過濾掉小於confidence值的組合 ...')
    
    #result_df = pd.DataFrame()
    
    #test = combine(freq_list, 2)
        
    
    #找出每個frequent itemset的S
    combination = {}        
    #print('combination: ', combination)
    for item in freq_list:
        combination[item] = list()
        for n in range(1, len(item)):
            #print('item: ', combination[item])
            combination[item].extend(combine(item, n).copy())
    #print('組合結果: ', combination)   
    
    
    #根據S找出I-S，然後計算confidence
    pass_confidence = {}
    for k, v in combination.items():
        pass_confidence[k] = {}
        for s in v:
            I_S = tuple(filter(lambda x:x not in s, k))
            #print(I_S)
            #initialize
            pass_confidence[k][tuple(s)] = [I_S, conf(s, k, df)]
    
    #print('計算confidence之後: ', pass_confidence)
    
    #濾掉 < confidence 最小值的資料
    prepare_to_remove = []
    for k, v in pass_confidence.items():
        for s, vi in v.items():
            if(vi[1] < confidence):
                prepare_to_remove.append([k, s])
                #pass_confidence[k].pop(s)
                
                
    #pass_confidence[ks[0]].pop(ks[1]) for ks in prepare_to_remove
    for ks in prepare_to_remove:
        pass_confidence[ks[0]].pop(ks[1])
        
        
    #print('過濾掉confidence太小之後: ', pass_confidence)
    #返回dataframe形式的result
    # frequent itemset / support / antecedent / consequent / confidence
    columns = ['frequent itemset', 'support', 'antecedent', 'consequent', 'confidence', 'lift']
    data = []
    for k, v in pass_confidence.items():
        for s, vi in v.items():
            #I_S = tuple(filter(lambda x:x not in s, k))
            tmp_row = [k, supp(k, df), s, vi[0], vi[1], lift(s, vi[0], k, df)]
            data.append(tmp_row)
    
    result_df = pd.DataFrame(data = data, columns = columns)
    print('apriori algorithm執行完成!')
    return result_df
    #pass    



#進行apriori algorithm
def apriori(df):
    #df: pandas的dataframe
    #為了避免重複執行apriori function時出現
    #'ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()'的錯誤，
    #需要把global variables
    clear_param()
      
    
    #先判斷輸入的資料是否為pandas的dataframe，是的話才繼續下去
    if(str(type(df)) == "<class 'pandas.core.frame.DataFrame'>"):
        #print('符合資料格式，可以繼續做計算。')
        #print(df.columns)
        
        #從dataframe中取得初始條件
        #1.資料總筆數
        total_row = len(df.index) 
        
        #2.Create size=1的itemset
        for i in range(total_row):
            temp_row = df.iloc[i]
            #print(type(temp_row))
            
            for j in range(len(temp_row.index)):
                #print(type(temp_row[j]))
                #temp_idx = map(tuple, temp_row[j])  'numpy.int64' object is not iterable
                
                global itemset_dict
                if(temp_row[j] not in list(itemset_dict.keys())):
                    #idx = temp_row[j]
                    #temp_tuple = tuple([10])
                    #print(type(idx))
                    itemset_dict[tuple([temp_row[j]])] = 1
                else:
                    itemset_dict[tuple([temp_row[j]])] = itemset_dict[tuple([temp_row[j]])] + 1
            
        #print('輸入的data初始狀態: ', itemset_dict)    
        print('開始執行apriori algorithm ...')
        
        #初步過濾掉<support的值
        filtered_item_dict = filter(lambda x:(x[1] / len(df.index) >= support), itemset_dict.items())
        itemset_dict = dict(filtered_item_dict)
        #print('初始且符合support的itemset: ',itemset_dict)
        
        
        #執行apriori algorithm
        while True:
            if(itemset(size, itemset_dict, df)):
                pass
                #print('size+1')
                #print(itemset_dict, size)
            else:
                break
            """
            temp_dict = itemset(size, itemset_dict, df).copy()
            if(temp_dict != {}):
                size = size + 1
                itemset_dict = temp_dict.copy()
                
            else:
                #itemset_dict = temp_dict.copy()
                #size = size + 1
                break
            """
        #print('最後的itemset結果: ', itemset_dict)
        global frequent_itemset_list
        #print(itemset_dict.items())
        frequent_itemset_list = [k for k, v in itemset_dict.items() if (v / len(df.index)) >= support]
        #frequent_itemset_list = ['hahaha']
        #print('final的frequent itemsets: ', frequent_itemset_list)
        
        
        
        #得到frequent itemsets之後，再來考慮 (S -> I-S) 是否有 >= confidence值
        result = compare_with_confidence(frequent_itemset_list, df)
        
        return result
    else:
        print('非pandas的dataframe，退回')
        print('資料格式為: ', type(df))
        return None
    
    


# In[53]:


#for test
"""
df = pd.read_excel('lottery.xlsx', sheet_name= 'big_lottery')

#print(df.iloc[[0,1]])  #取得特定row的資料

#print(df)
#去掉不要的columns
exclude_list = ['period','date']  #columns to exclude
want_column = [column for column in df.columns.tolist() if column not in exclude_list]
#print(want_column)
df_pure = df[want_column]
result = apriori(df_pure)
result
#print(result)
"""


# In[47]:


#顯示當前參數
def show_param(*args):
    print('support: ', support)
    print('confidence: ', confidence)
    print('size: ', size)
    print('itemset_dict: ', itemset_dict)
    print('frequent_itemset_list: ', frequent_itemset_list)

    
#清空參數
def clear_param(*args):
    
    #set_param()
    
    """
    global support 
    support = 0.6
    global cofidence
    cofidence = 0.6
    """
    
    global size
    size = 2
    global itemset_dict
    itemset_dict = {}  #用來存放frequent itemset的dict。每個itemset用tuple來存放; 存size = 1 開始
    #temp_dict = {}  #用來存放itemset()回傳的list，若為空list，則得到的frequent itemset list 為 itemset_list
    global frequent_itemset_list
    frequent_itemset_list = []
    
def set_param(sup = 0.6, con = 0.6):
    global support
    support = sup
    
    global confidence
    confidence = con
    
    print('參數設定完成。support = {}, confidence = {}'.format(support, confidence))
    
    


# In[49]:


#show_param()


# In[52]:


#clear_param()
#set_param(sup=0.2)


# In[19]:


"""
#測試combine
my_list = [1,2,3,4,5]
n = 2
print(combine(my_list, n))
"""


# In[ ]:




