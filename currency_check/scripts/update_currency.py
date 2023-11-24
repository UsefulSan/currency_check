import datetime

import requests
import schedule
from sqlalchemy.exc import IntegrityError

from currency_check import db
from currency_check.currency import currencies
from currency_check.models import USD_D1, EUR_D1 # type: ignore

today = (datetime.date.today().strftime("%d.%m.%Y"))


def get_exchange_rate(date: str = today) -> None:
    """
    Получает курс валют на заданную дату с определенного URL и сохраняет его в базе данных.
    :param date: (datetime, необязательно): Дата, для которой необходимо получить курс обмена валют.
    По умолчанию используется сегодняшняя дата.
    :return: None. Если произошла ошибка при получении курса валюты.
    """
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url)

    if response.status_code == 200:
        for currency in currencies.name:
            for timeframe in currencies.timeframes:
                table_name = eval(f'{currency}_{timeframe}')
                xml_text = response.text
                usd_index = xml_text.find(f"<CharCode>{currency}</CharCode>")
                rate_start_index = xml_text.find("<Value>", usd_index) + len("<Value>")
                rate_end_index = xml_text.find("</Value>", rate_start_index)
                rate = xml_text[rate_start_index:rate_end_index].replace(",", ".")
                date_time_obj = datetime.datetime.strptime(date, '%d.%m.%Y')
                try:
                    db.session.add(table_name(date=date_time_obj, price=float(rate)))
                    db.session.commit()
                except IntegrityError:
                    print(f"Данные в таблице {table_name} уже существуют")
                    db.session.rollback()

    else:
        print("Ошибка при получении курса валюты")
        return None


schedule.every().day.at("00:01", "Europe/Moscow").do(get_exchange_rate)

# while True:
#     schedule.run_pending()
#     time.sleep(5)
