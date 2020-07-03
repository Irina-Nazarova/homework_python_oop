import datetime as dt

data_format = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def __str__(self):
        return f'limit: {self.limit}, records: {str(self.records)}'

    def remainder(self):
        return self.limit - self.get_today_stats()

    """сохраняет новую запись о расходах."""
    def add_record(self, record):
        self.records.append(record)

    """считает сколько денег потрачено сегодня."""
    def get_today_stats(self):
        return (sum([record.amount for record in self.records
                    if record.date == dt.datetime.now().date()]))

    """считает сколько денег потрачено за последние 7 дней."""
    def get_week_stats(self):
        week_ago = dt.datetime.now().date() - dt.timedelta(days=7)
        return (sum([record.amount for record in self.records
                    if week_ago <= record.date <= dt.datetime.now().date()]))


class CaloriesCalculator(Calculator):

    """определяет, сколько ещё калорий можно/нужно получить сегодня"""
    def get_calories_remained(self):
        if self.remainder() > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с '
                    f'общей калорийностью не более {self.remainder()} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 70.00
    EURO_RATE = 80.00

    """определяет, сколько ещё денег можно потратить сегодня в руб., долларах или евро"""
    def get_today_cash_remained(self, currency):
        conversion_currency = {
                'eur': ('Euro', self.EURO_RATE),
                'usd': ('USD', self.USD_RATE),
                'rub': ('руб', self.RUB_RATE)}
        balance = self.remainder()
        if balance == 0:
            return f'Денег нет, держись'
        conversion_key, conversion_value = conversion_currency[currency]
        conversion_round = (round(balance / conversion_value, 2))
        if balance > 0:
            return f'На сегодня осталось {conversion_round} {conversion_key}'
        return (f'Денег нет, держись: твой долг -'
                f' {abs(conversion_round)} {conversion_key}')


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, data_format).date()

    def __str__(self):
        return f'{str(self.amount)} {self.comment} {str(self.date)}'


if __name__ == '__main__':
    """создан объект CashCalculator с лимитом 1000"""
    cash_calculator = CashCalculator(1000)

    """создан объект CaloriesCalculator с лимитом 2000"""
    calories_calculator = CaloriesCalculator(2000)

    cash_calculator.add_record(Record(600,"Безудержный шопинг"))
    cash_calculator.add_record(Record(1568, "Наполнение потребительской корзины", "27.06.2020"))
    cash_calculator.add_record(Record(300, "Катание на такси", "28.06.2020"))

    calories_calculator.add_record(Record(1000, "Кусок тортика. И ещё один.", "24.06.2020"))
    calories_calculator.add_record(Record(184, "Йогурт.", "23.06.2020"))
    calories_calculator.add_record(Record(1400, "Баночка чипсов."))

    print(calories_calculator.get_today_stats())
    print(calories_calculator.get_week_stats())
    print(calories_calculator.get_calories_remained())

    print(cash_calculator.get_today_cash_remained('rub'))
    print(cash_calculator.get_today_cash_remained('usd'))
    print(cash_calculator.get_today_cash_remained('eur'))
