#-*- coding: utf-8 -*-
#
# Sample Data mining code with Python/Pandas/NumPy/SciPy/..etc
#
# - Tested on Windows / Canopy
# - Code by Jioh L. Jung (ziozzang@gmail.com)
#

# 주: 분석 단계는 아래의 코드를 ipython 커맨드라인으로 적절히 copy&paste 로 작업 되었음.
# Tested Env.
# - Windows 7 x86_64 (xeon, 16GB)
# - python 2.7 x86_64 (Enthought Canopy for Windows 1.4.0/64bit)
# - Pandas 0.14.0 / SciPy 0.14.0 / NumPy 1.8.0 / MatPlotLib 1.3.1

############################################################################################
# 사용 라이브러리 임포팅
import pandas as pd
import numpy as np
from scipy.cluster.vq import kmeans,vq
import matplotlib.pyplot as plt

# csv 읽어오기.
apt_trades = pd.read_table("apt_lists.csv", sep=",")

#===============================================
# 데이터 가공 단계
# 거래중 최고 층수
p = apt_trades.groupby(by=["apt_ids"],as_index=False)["floor"].max()
p["floor_max_by_trade"] = p["floor"]
del p["floor"]
apt_lists = apt_lists.merge(p, on=["apt_ids"])

# 해당 아파트의 총 거래 건수
p = apt_trades.groupby(by=["apt_ids"],as_index=False)["price"].count()
p["count_by_trade"] = p["price"]
del p["price"]
apt_trades = apt_trades.merge(p, on=["apt_ids"])

# 해당 아파트의 총 사이즈 갯수
def round_v(x):
  return int(x)
apt_trades["size_int"] = apt_trades["size"].map(round_v)

p = apt_trades.groupby(by=["apt_ids", "size_int"],as_index=False)["price"].count()
p["size_count_by_trade"] = p["price"]
del p["price"]
apt_trades = apt_trades.merge(p, on=["apt_ids", "size_int"])
apt_trades["size_pct"] = apt_trades["size_count_by_trade"] / apt_trades["count_by_trade"]

# 평형 설정
apt_trades["py"] = apt_trades["size"] / 3.3
apt_trades["price_per_size"] = apt_trades["price"] / apt_trades["size"]
apt_trades["price_per_py"] = apt_trades["price"] / apt_trades["py"]

# 거래 당시 연식 설정
apt_trades["aged"] = apt_trades["years"] - apt_trades["built_year"]

# 면적으로 종별 분류하기.
#1 ~ 13평 = 42.975207 
#2 ~ 18평 = 59.504132 
#3 ~ 25.7평 = 85.7 
#4 ~ 30.8평 = 102 
#5 ~ 35평 = 115.702479 
#6 ~ 40평 = 132.231405 
#7 ~ 45평 = 148.760331 
#8 ~ 55평 = 181.818182 
def as_type(x):
  if x <= 42.975207:
    return 1
  if x <= 59.504132:
    return 2
  if x <= 85.7:
    return 3
  if x <= 102:
    return 4
  if x <= 115.702479:
    return 5
  if x <= 132.231405:
    return 6
  if x <= 148.760331:
    return 7
  if x <= 181.818182:
    return 8
  return 9
apt_trades["size_code"] = apt_trades["size"].map(as_type)

# 자료를 Groupby 해서 찾아 보기.

# 구별로 자료 합치기
dd = apt_trades.groupby(by=["years", "month", "day", "state", "city"],as_index=False)["price"].sum()

# 구별로 평당 가격 합치기
py_gu = apt_trades.groupby(by=["years", "month", "day", "state", "city"],as_index=False)["price_per_py"].mean()

# 서울에서 연식에 따른 평당 가격
py_yr_seoul = apt_trades[apt_trades["state"] == "서울"].groupby(by=["years", "month", "day", "state", "city", "aged"],as_index=False)["price_per_py"].mean()
# 다른 동네도 그럴까? - 울산? 부산?
py_yr_ulsan = apt_trades[apt_trades["state"] == "울산"].groupby(by=["years", "month", "day", "state", "city", "aged"],as_index=False)["price_per_py"].mean()
py_yr_busan = apt_trades[apt_trades["state"] == "부산"].groupby(by=["years", "month", "day", "state", "city", "aged"],as_index=False)["price_per_py"].mean()
py_yr_daegu = apt_trades[apt_trades["state"] == "대구"].groupby(by=["years", "month", "day", "state", "city", "aged"],as_index=False)["price_per_py"].mean()
py_yr_inchon = apt_trades[apt_trades["state"] == "인천"].groupby(by=["years", "month", "day", "state", "city", "aged"],as_index=False)["price_per_py"].mean()

# DataFrame의 내용 데이터를 가공
apt_trades["py"] = apt_trades["size"] / 3.3
apt_trades["price_per_size"] = apt_trades["price"] / apt_trades["size"]
apt_trades["price_per_py"] = apt_trades["price"] / apt_trades["py"]


# 간단한 통계 - 값의 카운트를 얻어오기 (Groupby -> count(*))
# - Series 로 출력됨
a = apt_lists["built_year"].value_counts()

# Series 데이터를 DataFrame으로 조인 하기
a.index.name = "built_year"
a.name = "count"
b = apt_lists.join(a, on="built_year", how="left")


# 소팅하기
b.sort_index(by=["built_year"], ascending=False)[:10]

# 골라 내서 슬라이스 하기
apt_lists[apt_lists["built_year"] > 2000][apt_lists["apt_ids"] > 1000][:10]

# 피벗테이블 작성
p = apt_trades.pivot_table("price", rows="apt_ids", cols="size", aggfunc="mean")


# 가격을 기간별로 써메이션 - 피봇 테이블
total_count = apt_trades.pivot_table(["price"], rows=["years", "month"], aggfunc=sum)
total_count.plot(title="price sum by timeline")

############################################################################################
# 차트 그리기


# 서울의 연식별 거래건수
apt_trades[apt_trades["state"] == "서울"].groupby(by=["aged"], as_index=False)["price"].count().plot( "aged","price", kind="bar")

# 서울의 연식별 평당 가격
apt_trades[apt_trades["state"] == "서울"].groupby(by=["aged"], as_index=False)["price_per_py"].mean().plot( "aged","price_per_py", kind="barh")

# 연식들의 동네별
apt_trades[apt_trades["state"] == "서울"][apt_trades["aged"] >=25][apt_trades["aged"] <=37].groupby(by=["city"], as_index=False)["price_per_py"].mean().plot( "city","price_per_py", kind="bar")



#apt_trades[apt_trades["state"] == "서울"][apt_trades["aged"] >=25][apt_trades["aged"] <=37].groupby(by=["city"], as_index=False)["price_per_py"].mean()
# 결국, 강남, 서초, 송파, 용산, 강동이 핵심.

# 클러스터링 해보기
q = apt_trades[apt_trades["state"] == "서울"][apt_trades["aged"] >=25][apt_trades["aged"] <=37].groupby(by=["city", "aged"], as_index=False)["price_per_py"].mean()

data = np.vstack(q.as_matrix(columns=[ "aged", "price_per_py"]))
centroids,_ = kmeans(data,2)

idx,_ = vq(data,centroids)

plot(data[idx==0,0],data[idx==0,1],'ob',
     data[idx==1,0],data[idx==1,1],'or')
plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
show()

#q[q.price_per_py < 2000] 과 q[q.price_per_py >= 2000]
#경향으로 나뉨


# 예를들어 중랑구는(아랫쪽 클러스터..)
apt_trades[apt_trades["state"] == "서울"][apt_trades["city"]== "중랑구"].groupby(by=["aged"], as_index=False)["price_per_py"].mean().plot( "aged","price_per_py", kind="barh")
# 에서 보듯이 재개발관련 가격 차이가 크게 나지 않음 - 즉 재개발은 서울 안에서도 특정지역 편중 이슈임



# 아파트 입주시기별 단지 크기
apt_navers[apt_navers.house_count > 100 ][apt_navers.enter != "-" ][["enter", "house_count"]].pivot_table(["house_count",], rows=["enter"]).plot(title="Apt. Size by years")

# 파라미터별 산포도
pd.scatter_matrix(n)

############################################################################################
# 데이터 마이닝 돌리기
# kmeans extract using SciPy
data = np.vstack(apt_trades.as_matrix(columns=["floor", "price_per_py"]))
centroids,_ = kmeans(data,2)

idx,_ = vq(data,centroids)

plot(data[idx==0,0],data[idx==0,1],'ob',
     data[idx==1,0],data[idx==1,1],'or')
plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
show()


############################################################################################
# 데이터 샘플링
a = np.random.permutation(apt_trades.as_matrix(columns=["dong_id", "floor"]))
sampled_90pct = a[:len(a) * 0.9]
others_10pct   = a[-len(a) * 0.1 :]


