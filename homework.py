import datetime as dt

today = dt.datetime.now().date()
data_format = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def __str__(self):
        return f'limit: {self.limit}, records: {str(self.records)}'

    # сохраняет новую запись о расходах
    def add_record(self, record):
        self.records.append(record)

    # считает сколько денег потрачено сегодня
    def get_today_stats(self):
        self.sum_today = 0
        for record in self.records:
            if record.date == today:
                self.sum_today += record.amount
        return self.sum_today

    # считает сколько денег потрачено за последние 7 дней
    def get_week_stats(self):
        sum_week = 0
        delta = dt.timedelta(days=7)
        week_ago = today - delta
        for record in self.records:
            if week_ago <= record.date <= today:
                sum_week += record.amount
        return sum_week


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    # определяет, сколько ещё калорий можно/нужно получить сегодня
    def get_calories_remained(self):
        remainder_calories = self.limit - self.get_today_stats()

        if self.get_today_stats() < self.limit:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remainder_calories} кКал"
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = float(70)
    EURO_RATE = float(80)

    def __init__(self, limit):
        super().__init__(limit)

    # определяет, сколько ещё денег можно потратить сегодня в руб., долларах или евро
    def get_today_cash_remained(self, currency):
        remainder_cash = self.limit - self.get_today_stats()
        conversion_usd = round(remainder_cash / CashCalculator.USD_RATE, 2)
        conversion_euro = round(remainder_cash / CashCalculator.EURO_RATE, 2)

        if currency == 'usd':
            balance = f'{str(abs(float(conversion_usd)))} USD'
        elif currency == 'eur':
            balance = f'{str(abs(float(conversion_euro)))} Euro'
        else:
            balance = f'{str(abs(float(remainder_cash)))} руб'

        if remainder_cash > 0:
            return f'На сегодня осталось {balance}'
        elif remainder_cash == 0:
            return f'Денег нет, держись'
        elif remainder_cash < 0:
            return f'Денег нет, держись: твой долг - {balance}'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, data_format).date()

    def __str__(self):
        return f'{str(self.amount)} {self.comment} {str(self.date)}'


if __name__ == '__main__':
    # создан объект CashCalculator с лимитом 1000
    cash_calculator = CashCalculator(1000)

    # создан объект CaloriesCalculator с лимитом 2000
    calories_calculator = CaloriesCalculator(2000)

    cash_calculator.add_record(Record(500,"Безудержный шопинг"))
    cash_calculator.add_record(Record(1568, "Наполнение потребительской корзины", "27.06.2020"))
    cash_calculator.add_record(Record(300, "Катание на такси", "28.06.2020"))

    calories_calculator.add_record(Record(1000, "Кусок тортика. И ещё один.", "24.06.2020"))
    calories_calculator.add_record(Record(184, "Йогурт.","23.06.2020"))
    calories_calculator.add_record(Record(1114, "Баночка чипсов."))

    cash_calculator.get_today_stats()
    cash_calculator.get_week_stats()
    #cash_calculator.get_today_cash_remained()

    calories_calculator.get_today_stats()
    calories_calculator.get_week_stats()
    calories_calculator.get_calories_remained()

    print(cash_calculator.get_today_cash_remained('rub'))
    print(cash_calculator.get_today_cash_remained('usd'))
    print(cash_calculator.get_today_cash_remained('eur'))
