코드 설명
=========

샘플로 작업한, 한국 아파트 거래 내역으로 데이터 마이닝을 위한 자료 입니다. 파이썬/판다스/넘파이/싸이파이를 사용 한 환경에서 동작을 테스트 하였습니다.

Sample Data mining code with Python/Pandas/NumPy/SciPy/..etc

라이센스
========

MIT License. code is supplied as-is with no warrenty. do, whatever with your own risk.


테스트/작업 환경
================

* Tested Env.
 * Windows 7 x86_64 (xeon, 16GB)
 * python 2.7 x86_64 (Enthought Canopy for Windows 1.4.0/64bit)
 * Pandas 0.14.0 / SciPy 0.14.0 / NumPy 1.8.0 / MatPlotLib 1.3.1


데이터 설명
===========

한국 아파트 거래 데이터 (2006~2014년 1사분기 까지) 입니다.

총 5021360 건.


컬럼 설명
=========

CSV / UTF-8 포맷

* idx - 유니크 ID
* years - 거래 년
* month - 거래 월
* day - 거래 일(1-초순/2-중순/3-하순)
* size - 전용면적 (m^2)
* floor - 층수
* price - 거래 가격(만원)
* built_year - 건축 연도
* state - 광역지역(ex: 서울)
* city - 시군구 (ex: 강남구)
* dong - 동 (ex: 개포동)
* apt_ids - 아파트 ID (unique hashed)

