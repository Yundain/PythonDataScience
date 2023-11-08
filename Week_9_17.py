# !sudo apt-get install -y fonts-nanum
# !sudo fc-cache -fv
# !rm ~/.cache/matplotlib -rf

# import matplotlib.pyplot as plt
# plt.rc('font', family='NanumBarunGothic')

# 사용 라이브러리 정의
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from google.colab import files

# 엑셀 파일 불러오기
uploaded = files.upload()

# 엑셀 파일 시트별로 불러오기
log_info=pd.read_excel('customer_log_data.xlsx', sheet_name = 'log_info')
review_log_data = pd.read_excel('customer_log_data.xlsx', sheet_name = 'review_data')
purchase_data = pd.read_excel('customer_log_data.xlsx', sheet_name = 'purchase_data')



# ? P1(1) 문제 풀이

# log_info로 지정
df = log_info

# event_type이 live login인 조건을 만족하는 행 추출
log_df = df [(df['event_type']=='live login') ]
log_df



# ====성별 비율====

 # 남자의 개수 행 반환
male = len(log_df.loc[log_df['sex'] == 'male'])
# 여자의 개수 행 반환
female = len(log_df.loc[log_df['sex'] == 'female'])
print(male, female)

# 남자의 비율 계산
male_ratio = (male / (male+female)) * 100
print(male_ratio)
# 여자의 비율 계산
female_ratio = (female / (male+female)) * 100
print(female_ratio)

# x축
sex = ['male', 'female']
# y축
values = [male_ratio, female_ratio]

#막대 그래프 그리기
plt.figure(figsize = (10, 5))
plt.bar(sex, values)
plt.show()


# ====나이대별 고객수====

#age를 나이대로 바꾸는 함수 정의
def test(x):
  if x >= 40:
    return 40
  elif x >= 30:
    return 30
  else:
    return 20

log_df['age'] = df['age'].apply(test)
log_df

# age를 나이대로 바꾸면서 age 컬럼명을 age_generation으로 컬럼명 바꾸기
log_df['age_generation'] = log_df['age'].apply(test)
log_df

# 20대 고객 수 구하기
age_20 = len(log_df.loc[log_df['age'] == 20])
# 30대 고객 수 구하기
age_30 = len(log_df.loc[log_df['age'] == 30])
# 30대 고객 수 구하기
age_40 = len(log_df.loc[log_df['age'] == 40])
print(age_20, age_30, age_40)

# x축
age = ['20', '30', '40']
# y축
values = [age_20, age_30, age_40]

# 막대 그래프 그리기
plt.figure(figsize = (10, 5))
plt.bar(age, values)
plt.show()


# ? P1(2) 문제 풀이

# 'event_type'이 'login'인 로그만 필터링
logins_logs_filter = log_info[log_info['event_type'] == 'login']
print("logins_logs_filter", logins_logs_filter)

# user_id가 중복되는 경우 첫번째만 남기고 제거 (최초 로그인만 남김)
login_logs_filter = logins_logs_filter.drop_duplicates(['user_id'], keep = 'first')
print("login_logs_filter", login_logs_filter)

# 분에 맞춰서 분당 데이터 개수 추출
login_logs_filter['datetime'] = pd.to_datetime(login_logs_filter['datetime'])
login_counts = login_logs_filter.groupby([login_logs_filter['datetime'].dt.minute]).count()
print("login_counts", login_counts)

# y 데이터 개수 x 분(시간) 꺾은선 그래프 그리기
# TODO 컬럼을 하나로 줄이고 login_counts로 이름 바꾸기
plt.plot(login_counts)
plt.show()


# ? P2(1) 문제 풀이

# 상품을 구매 여부 파악하기
purchase_find = purchase_data[purchase_data['event_parameter'] == 'click']

# 각 상품별 구매 갯수 파악하기
sum_purchase = purchase_data['product_id'].value_counts()
print(sum_purchase)

# 상품의 종류 갯수 파악하기
count_product = sum_purchase.count()

# 각 상품 코드 가져오기
product_index = sum_purchase.index

# 그래프 생성
x = np.arange(count_product)

# 그래프 그리기
plt.bar(x, sum_purchase)
plt.xticks(x, product_index)

# 그래프 보여주기
plt.show()


# ? P2(2) 문제 풀이

# user_id를 기준으로 log_info와 purchase_data 합치기
join_df = pd.merge(log_info, purchase_data, on=['user_id'])
join_df[['user_id', 'age', 'product_id', 'type', 'event_parameter']]
print(join_df)

# 구매 데이터만 필터링
purchase_join_df = join_df [(join_df['type']=='구매하러 가기') ] # event_type이 live login인 조건을 만족하는 행 추출

# age를 나이대로 변환
purchase_join_df['age'] = join_df['age'].apply(test)
purchase_join_df

# 나이대, 구매상품 별로 그룹화
join_df_return = purchase_join_df.groupby(['product_id', 'age']).count()
join_df_return

# TODO 묶음 세로 막대 그래프 그리기


# ? P3(1) 문제 풀이

# 'product_id'가 가장 인기있는 제품의 로그만 필터링
# TODO 최대값으로 제품 id구하도록 수정
hottest_logs_filter = review_log_data[review_log_data['product_id'] == 1698]
print("hottest_logs_filter", hottest_logs_filter)

# 각 키워드별 갯수 파악하기
sum_keyword = hottest_logs_filter['keyword'].value_counts()
print("sum_keyword", sum_keyword)


# ? P3(2) 문제 풀이

# 상위 5개 데이터만 추출
high_sum_keyword = sum_keyword.nlargest(5)

# 각 키워드 가져오기
keyword_index = high_sum_keyword.index

# 그래프 생성
x = np.arange(5)

# 그래프 그리기
plt.bar(x, high_sum_keyword)
plt.xticks(x, keyword_index)

# 그래프 보여주기
plt.show()