import pandas as pd

data_len = 230

def get_cv_diff_value(data):
    diff_value = list()
    diff_value.append(None)
    for i in range(1,data_len):
        diff_value.append(data['close_value'][i]-data['close_value'][i-1])
    return pd.DataFrame(diff_value,columns=['diff_value'])

def get_cv_diff_rate(data):
    diff_value_rate = list()
    diff_value_rate.append(None)
    for i in range(1,data_len):
        diff_value_rate.append(round((data['close_value'][i]-data['close_value'][i-1])/data['close_value'][i-1] * 100,4))
    return pd.DataFrame(diff_value_rate,columns=['diff_value_rate'])

def get_cv_maN_value(N,data):
    maN_value = data['close_value'].rolling(window=N).mean()
    return maN_value

def get_cv_maN_rate(N,data):
    maN_value = get_cv_maN_value(N,data)
    maN_rate = list()
    for i in range(0,data_len):
        maN_rate.append(None)
    for i in range(0,data_len):
        if(i<N):
            maN_rate[i] = None
        else:
            maN_rate[i-1] = (((maN_value[i]-maN_value[i-N])/maN_value[i-N]) *100)
    return maN_rate

def get_cvNd_diff_rate(N,data):
    cvNd_diff_rate = list()
    for i in range(0,data_len):
        cvNd_diff_rate.append(None)
    for i in range(0,data_len):
        if(i<N):
            cvNd_diff_rate[i] = None
        else:
            cvNd_diff_rate[i-1] = (((data['close_value'][i] - data['close_value'][i - N]) / data['close_value'][i - N]) *100)
    return pd.DataFrame(cvNd_diff_rate,columns=['cv5d_diff_rate'])

def get_ud_Nd(val):
    ud_val = 0  # 일수에 상관없이 전날 대비 상승하면 1, 하락하면 -1, 같으면 0
    result = 0  # close_value들끼리 뺀 값
    ud_Nd = 3  # 3일 연속 상승하거나 하락해야 ud_Nd - 1일에 값을 저장

    result_list = []  # result값을 넣을 리스트
    ud_val_list = []  # ud_val값을 넣을 리스트
    ud_Nd_list = []  # ud_Nd값을 넣을 리스트
    val = val[['close_value']]
    for i in range(230):
        cost = val.iloc[i, 0]
        if cost == val.iloc[0, 0]:
            result = cost - result
        else:
            result = cost - val.iloc[i - 1, 0]
        if result > 0:
            ud_val = 1
        elif result < 0:
            ud_val = -1
        elif result == 0:
            ud_val = 0

        result_list.append(result)
        ud_val_list.append(ud_val)

    result_list.append(0)

    # result_list에는 값들 정확하게 저장됨
    for index, value in enumerate(result_list):
        print(index, value)

    # ud_val_list에는 n의 값을 3~5가 아닌 1로 했음
    # 변경해야됨

    # for i in ud_val_list:
    #    print(i)

    print("===========================================================")

    numPlus1 = ud_val_list.count(1)
    numMinus1 = ud_val_list.count(-1)

    N = 1  # N의 값

    # print(ud_Nd_list)

    ud_Nd_list.insert(0, 0)

    for N in range(N, 230):

        if ud_val_list[N - 1] == 1 and ud_val_list[N - 2] == 1 and ud_val_list[N - 3] == 1:
            ud_Nd_list.insert(N - 2, 1)

        elif ud_val_list[N - 1] == -1 and ud_val_list[N - 2] == -1 and ud_val_list[N - 3] == -1:
            ud_Nd_list.insert(N - 2, -1)

        else:
            ud_Nd_list.insert(N - 2, 0)

    ud_Nd_list.insert(229, 0)
    ud_Nd_list.insert(230, 0)

    for index, value in enumerate(ud_Nd_list):
        print(index, value)

    numPlus1 = ud_Nd_list.count(1)
    numMinus1 = ud_Nd_list.count(-1)
    numZero = ud_Nd_list.count(0)

    print("ud_Nd값은 1이 ", numPlus1, "번, -1이 ", numMinus1, "번, 0이 ", numZero, "번 count")
    print("======================================================================================================================================================")

    return pd.DataFrame(ud_Nd_list, columns=['ud_Nd'])

def get_vv_diff_value(data):
    vv_diff_value = list()
    vv_diff_value.append(None)
    for i in range(1, data_len):
        vv_diff_value.append(data['volume_value'][i] - data['volume_value'][i - 1])
    return pd.DataFrame(vv_diff_value, columns=['vv_diff_value'])



stock_data = pd.read_csv('stock_history.csv', encoding="ms949")
stock_read_data = stock_data.loc[stock_data['stockname'].isin(["에듀파트너"]), :]
stock_read_data = stock_read_data[["basic_date", "stockname", "close_value","volume_value"]]
stock_read_data.sort_values(by=['basic_date'], axis=0, inplace=True)
stock_read_data = stock_read_data.reset_index(drop=True)

add_stock_read_data = stock_read_data
add_stock_read_data['diff_value'] = get_cv_diff_value(stock_read_data)
add_stock_read_data['diff_value_rate'] = get_cv_diff_rate(stock_read_data)
add_stock_read_data['ma3_value'] = get_cv_maN_value(3,stock_read_data)
add_stock_read_data['ma3_rate'] = get_cv_maN_rate(3,stock_read_data)
add_stock_read_data['cv3d_diff_rate'] = get_cvNd_diff_rate(3,stock_read_data)
add_stock_read_data['vv_diff_value'] = get_vv_diff_value(stock_read_data)
add_stock_read_data['ud_3d'] = get_ud_Nd(stock_read_data)
print(add_stock_read_data)

add_stock_read_data.to_csv("stock_history_added.csv", encoding="ms949")
