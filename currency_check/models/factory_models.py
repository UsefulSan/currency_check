from currency_check import app, db
from currency_check.models.models import CurrencyMixin


class USD_D1(db.Model, CurrencyMixin): # type: ignore
    pass


class EUR_D1(db.Model, CurrencyMixin): # type: ignore
    pass


app.app_context().push()
db.create_all()
