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

def get_un_Nd(N,data):
    ud_Nd_list = list()
    value = 0
    com_value = 0
    data = data['close_value']
    for i in range(0,data_len):
        ud_Nd_list.append(0)

    for i in range(0,data_len-N):
        pl_cnt = 0
        mi_cnt = 0
        for j in range(0,N):
            if(data[i+j] < data[i+j+1]):
                pl_cnt = pl_cnt + 1
            elif(data[i+j] > data[i+j+1]):
                mi_cnt = mi_cnt + 1


        if(pl_cnt == N):
            ud_Nd_list[i+N-1] = 1
        elif(mi_cnt == N):
            ud_Nd_list[i+N-1] = -1
        else:
            ud_Nd_list[i+N-1] = 0

    return pd.DataFrame(ud_Nd_list,columns=['ud_Nd'])

def get_vv_diff_value(data):
    vv_diff_value = list()
    vv_diff_value.append(None)
    for i in range(1, data_len):
        vv_diff_value.append(data['volume_value'][i] - data['volume_value'][i - 1])
    return pd.DataFrame(vv_diff_value, columns=['vv_diff_value'])

def get_vv_maN_value(N,data):
    vv_maN_value = data['volume_value'].rolling(window=N).mean()
    return vv_maN_value

def get_vv_maN_rate(N,data):
    vv_maN_value = get_vv_maN_value(N,data)
    vv_maN_rate = list()
    for i in range(0,data_len):
        vv_maN_rate.append(None)
    for i in range(0,data_len):
        if(i<N):
            vv_maN_rate[i] = None
        else:
            vv_maN_rate[i-1] = (((vv_maN_value[i]-vv_maN_value[i-N])/vv_maN_value[i-N]) *100)
    return vv_maN_rate



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
add_stock_read_data['vv_ma3_value'] = get_vv_maN_value(3,stock_read_data)
add_stock_read_data['vv_ma3_rate'] = get_vv_maN_rate(3,stock_read_data)
add_stock_read_data['ud_3d'] = get_un_Nd(3,stock_read_data)
print(add_stock_read_data)

add_stock_read_data.to_csv("stock_history.added.csv", encoding="ms949")
