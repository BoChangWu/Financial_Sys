# Financial_Sys


一個監看金融市場完整資訊的系統

## Description
----------------

這個Project並不是為了賺錢, 是為了更了解金融市場, 充分了解市場資訊以便進行判斷, 進行交易時常會因為資訊不足而無法下正確的判斷, 對公司內部營運、外資走向等資訊, 抑或是對未來不確定也好, 只要有一項資訊不足就可能讓人失去判斷能力, 因此得到的訊息越多, 越能做出最有利的決定

本project 的主軸在如何獲得完整的市場資訊, 其中包含:
1. 股票資訊(報價、歷史資訊等)
2. 公司營運資訊(市值、財報等)
3. 公司消息(新聞、展望)


當資訊蒐集齊全後, 接下來就可以做很多的處理, 例如簡單的根據數據進行 *API下單*, 或是將獲得的資料統計進行 *股票分析(資料分析)*, 也可以經過處理後將資料丟到 機器學習模型中進行 *模型訓練*

## Introduction

----------------
### Preprocessing

### Issue
1. 圖表不管用backtrader 或 pyfolio 都可能跑不出圖... 先忽略此問題嘗試使用別的方法作圖
### Data Source
[Yahoo Finance US](https://finance.yahoo.com/)
[Backtrader](https://www.backtrader.com/)
[Backtrader tutorial](https://www.youtube.com/watch?v=pt4auu_ZPm4)