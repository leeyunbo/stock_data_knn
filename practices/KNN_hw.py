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

def plot_cities(stock_datas):

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
    plt.axis([-10,10,160000,220000]) # set the axes
    plt.title("Favorite Programming Languages")
    plt.show()




# 각각 161개와 230-161개 = 69 개
if __name__ == "__main__":

    stock_data = pd.read_csv('stock_history.added.csv', encoding="ms949")
    stock_datas=list()
    predicted_ud_3ds=list()
    data1 = stock_data['cv3d_diff_rate']
    data2 = stock_data['ma3_value']
    ud_3d = stock_data['ud_3d']


    for i in range(0,len(ud_3d)):
        stock_datas.append(([float(data1[i]),float(data2[i])],str(ud_3d[i])))

    print(stock_datas)


    # try several different values for k

    for k in [1, 3, 5, 7,9,11,13]:
        num_correct = 0

        for diff_data, ud_3d in stock_datas:
            other_datas = [other_data
                            for other_data in stock_datas
                            if other_data != (diff_data, ud_3d)]

            predicted_ud_3d = knn_classify(k, other_datas, diff_data) ## 투표를 다하면 예측 랭귀지가 나오겠지.


            if predicted_ud_3d == ud_3d: #만약, 예측 랭귀지와 actual_language가 같다면
                num_correct += 1 #correct 증가
            predicted_ud_3ds.append(predicted_ud_3d)


        print(k, "neighbor[s]:", num_correct, "correct out of", len(stock_datas),  (num_correct/len(stock_datas)) * 100,'%')

    # create a scatter series for each language
    plot_cities(stock_datas)


"""
    dimensions = range(1, 101, 5)


    avg_distances = []
    min_distances = []

    random.seed(0)
    for dim in dimensions:
        distances = random_distances(dim, 10000)  # 10,000 random pairs
        avg_distances.append(mean(distances))     # track the average
        min_distances.append(min(distances))      # track the minimum
        print(dim, min(distances), mean(distances), min(distances) / mean(distances))
"""

"""
# 각각 161개와 230-161개 = 69 개
if __name__ == "__main__":

    stock_data = pd.read_csv('stock_history.added.csv', encoding="ms949")
    stock_datas=list()
    predicted_ud_3ds=list()
    data1 = stock_data['cv3d_diff_rate']
    data2 = stock_data['ma3_value']
    data3 = stock_data['diff_value']
    ud_3d = stock_data['ud_3d']


    for i in range(0,len(ud_3d)):
        stock_datas.append(([float(data1[i]),float(data2[i])],str(ud_3d[i])))

    print(stock_datas)


    # try several different values for k

    for k in [1, 3, 5, 7,9,11]:
        num_correct = 0
        other_datas = stock_datas[0:161]
        for diff_data, ud_3d in stock_datas[161:]:
            predicted_ud_3d = knn_classify(k, other_datas, diff_data) ## 투표를 다하면 예측 랭귀지가 나오겠지.

            if predicted_ud_3d == ud_3d: #만약, 예측 랭귀지와 actual_language가 같다면
                num_correct += 1 #correct 증가
            predicted_ud_3ds.append(predicted_ud_3d)


        print(k, "neighbor[s]:", num_correct, "correct out of", len(stock_datas[161:]),  (num_correct/len(stock_datas[161:])) * 100,'%')

    # create a scatter series for each language
    plot_cities(stock_datas)
"""