import pandas as pd
import numpy as np


from collections import Counter
from linear_algebra import distance
from stats import mean
import math, random
import matplotlib.pyplot as plt
data_len = 230

def mkRefdS(pre, roundN):
    re=[pre.loc[i, j] for i in pre.index for j in pre.columns]
    return(np.round(re, roundN))

def raw_majority_vote(labels):
    votes = Counter(labels)
    winner, _ = votes.most_common(1)[0]
    return winner

def majority_vote(labels):
    """assumes that labels are ordered from nearest to farthest"""
    vote_counts = Counter(labels)       # 가장 가까운 거리에 있는 다양한 포인트들의 집단의 수를 셈
    winner, winner_count = vote_counts.most_common(1)[0] #가장 빈도수가 많은 포인트의 집단을 튜플 형태로 리턴
    num_winners = len([count
                       for count in vote_counts.values()
                       if count == winner_count]) #위너의 수를 넘겨주는거지

    if num_winners == 1: #만약 승리자가 하나라면 그걸 리턴
        return winner                     # unique winner, so return it
    else: #만약 아니라면, 가장 멀리있는 애를 제외하고 다시 투표를 진행한다.
        return majority_vote(labels[:-1]) # try again without the farthest


def knn_classify(k, labeled_points, new_point):
    """each labeled point should be a pair (point, label)"""

    # order the labeled points from nearest to farthest
    by_distance = sorted(labeled_points,
                         key=lambda point_label: distance(point_label[0], new_point)) #새로운 포인트와 원래 존재하는 포인트들의 거리를 구해서 정렬한후 리스트로 반환

    # find the labels for the k closest
    k_nearest_labels = [label for _, label in by_distance[:k]] # 가장 가까운 거리에 있는 포인트들을 리스트형식으로 담아준다.

    # and let them vote
    return majority_vote(k_nearest_labels) # 거리가 동일한 포인트들이 있을 수도 있으니까, 투표를 해야함


def plot_state_borders(plt, color='0.8'):
    pass

def plot_cities(stock_datas,a,b,c,d): # 그래프 관련 함수-------- 이부분에서 범위를 수정해야함

    # key is language, value is pair (longitudes, latitudes)
    plots = { "-1" : ([], []), "0" : ([], []), "1" : ([], []) }

    # we want each language to have a different marker and color
    markers = { "-1" : "o", "0" : "s", "1" : "^" }
    colors  = { "-1" : "r", "0" : "b", "1" : "g" }

    for differ, ud_3d in stock_datas:
        plots[ud_3d][0].append(differ[0])
        plots[ud_3d][1].append(differ[1])


    # create a scatter series for each language
    for ud_3d, (x, y) in plots.items():
        plt.scatter(x, y, color=colors[ud_3d], marker=markers[ud_3d],
                          label=ud_3d, zorder=10)

    plot_state_borders(plt)    # assume we have a function that does this

    plt.legend(loc=0)          # let matplotlib choose the location
    plt.axis([a,b,c,d]) # 변수에 따라서 범위 수정 (x : -12 ~ 9, y : -10 ~ 10)
    plt.title("Favorite Programming Languages")
    plt.show()



#close_value	diff_value	diff_value_rate	ma3_value	ma3_rate	cv3d_diff_rate
# 각각 161개와 230-161개 = 69 개, 학습데이터 161개와 테스트데이터 69개
if __name__ == "__main__":

    stock_data = pd.read_csv('stock_history.added.csv', encoding="ms949")
    stock_datas=list()
    predicted_ud_3ds=list()
    data1 = stock_data['cv3d_diff_rate'] # 변수 변경 혹은 추가 가능,만약 추가하려면 리스트를 추가해야함
    data2 = stock_data['diff_value_rate']
    ud_3d = stock_data['ud_3d']


    for i in range(0,len(ud_3d)):
        stock_datas.append(([float(data1[i]),float(data2[i])],str(ud_3d[i])))

    print(stock_datas)


    # try several different values for k
    predicted_ud_3ds = list()
    for i in range(0,161):
        predicted_ud_3ds.append('Learning Data')

    for k in [9]:
        num_correct = 0
        other_datas = stock_datas[0:161]
        for diff_data, ud_3d in stock_datas[161:]:
            predicted_ud_3d = knn_classify(k, other_datas, diff_data)

            if predicted_ud_3d == ud_3d:
                num_correct += 1
            predicted_ud_3ds.append(predicted_ud_3d) # 예측되어 나온 ud_3d 값들을 가지는 리스트


        print(k, "neighbor[s]:", num_correct, "correct out of", len(stock_datas[161:]),  (num_correct/len(stock_datas[161:])) * 100,'%')
        # k 별로 정확도 계산 후 출력
    # create a scatter series for each language
    stock_data['predicted'] = pd.DataFrame(predicted_ud_3ds,columns=['cv5d_diff_rate'])
    stock_data.to_csv("stock_history.added.predicted.csv", encoding="ms949") # csv파일에 예측되어 나온 ud_3d 추가
    plot_cities(stock_datas[0:161],450,4800,-40,60) # 학습 데이터에 대해서 분포를 보여줌



