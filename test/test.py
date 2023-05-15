import shioaji as sj

# 永豐測試環境已經關閉無法使用, 需使用正式環境, 因此sj.Shioaji()不加入simulation=True參數 , 因此下單需要小心
api = sj.Shioaji()

api.login(
    api_key = "9dvjsXe1Bec9zsEayMAS2McgPCDShYDQL8Hw9QWCvPHt",
    secret_key = "GhX5JpY1GMj9dPjpaQsDqeCpkjbjnRicmhNQszeRiFix",
    contracts_cb=lambda security_type: print(f"{repr(security_type)} fetch done.")
)
# https://sinotrade.github.io/zh_TW/tutor/market_data/streaming/stocks/
print(api.Contracts.Stocks['2330'])