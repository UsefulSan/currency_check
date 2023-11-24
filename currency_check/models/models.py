from sqlalchemy import Column, Date, Float


class CurrencyMixin:
    date = Column(Date, primary_key=True, unique=True)
    price = Column(Float)
