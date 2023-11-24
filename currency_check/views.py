from datetime import date as day
from datetime import datetime
from typing import Any

from flask import render_template, request

from currency_check import app, db
from currency_check.currency import currencies
from currency_check.scripts.update_currency import get_exchange_rate
from currency_check.models import USD_D1, EUR_D1 # type: ignore


@app.route('/', methods=('GET', 'POST')) # type: ignore
def home() -> Any:
    """
      Эта функция служит обработчиком домашнего маршрута ('/') приложения.
      Она поддерживает методы GET и POST.
      :param: None
      :return:
          объект: Отрисованный шаблон 'home.html' со следующими переменными:
          - rate: список текущих курсов валют
          - historic_rate: список исторических курсов обмена валют
          - selected_date: выбранная дата из формы POST-запроса
      :raises: None
      """
    current_rates = []
    history_rates = []
    selected_date = None

    for currency in currencies.name:
        for timeframe in currencies.timeframes:
            table_name = eval(f'{currency}_{timeframe}')
            current_rate = db.session.query(table_name).where(table_name.date == day.today()).first()
            if current_rate is None:
                get_exchange_rate()
                return home()
            current_rates.append(current_rate.price)
            if request.method == 'POST':
                try:
                    selected_date = request.form['date']
                    if selected_date and selected_date <= day.today().strftime('%Y-%m-%d'):
                        current_rate = db.session.query(table_name).where(table_name.date == selected_date).first()
                        if current_rate is None:
                            date_time = datetime.strptime(selected_date, '%Y-%m-%d')
                            date_time_obj = date_time.strftime('%d.%m.%Y')
                            get_exchange_rate(date_time_obj)
                            return home()
                        history_rates.append(current_rate.price)
                except KeyError:
                    pass

    return render_template('home.html', rate=current_rates, historic_rate=history_rates,
                           selected_date=selected_date)
