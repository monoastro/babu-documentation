import nepali_datetime

bs_date = nepali_datetime.date(2080, 2, 3)
ad_date = bs_date.to_datetime_date()

print(f"BS: {bs_date} -> AD: {ad_date}")
