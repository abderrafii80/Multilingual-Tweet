@echo off
hive -e "LOAD DATA INPATH '/data_mining/google_news_2_en.json' INTO TABLE data_mining.news_en;"
hive -e "LOAD DATA INPATH '/data_mining/google_news_2_fr.json' INTO TABLE data_mining.news_fr;"
hive -e "LOAD DATA INPATH '/data_mining/google_news_2_ar.json' INTO TABLE data_mining.news_ar;"
pause