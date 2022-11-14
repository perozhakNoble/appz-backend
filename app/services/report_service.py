import itertools

from app.db import DBClient
from app.models import Expense, Category
from app.schemas import Expenses, Expense as SingleExpense, CreateExpense, UpdateExpense


class Calculation:
    def __init__(self, category, start_date, end_date):
        self.db = DBClient.current_session
        self.category = category
        self.start_date = start_date
        self.end_date = end_date

    def collect_data(self):
        category = self.db.query(Category).filter(Category.category_name == self.category).first()
        category_id = category.id if category else None

        expenses_query = self.db.query(Expense)

        if category_id:
            expenses_query = expenses_query.filter(Expense.category_id == category_id)

        if self.start_date:
            expenses_query = expenses_query.filter(Expense.date >= self.start_date)

        if self.end_date:
            expenses_query = expenses_query.filter(Expense.date <= self.end_date)

        return expenses_query.order_by(Expense.date, Expense.currency_id).all()

    def calculate(self):
        expenses = self.collect_data()

        expenses_by_date = []
        for date, by_dates in itertools.groupby(expenses, key=lambda x: x.date):
            expenses_by_currencies = []
            for currency, by_currencies in itertools.groupby(by_dates, key=lambda x: x.currency):
                total_amount = sum(map(lambda x: x.amount, by_currencies))
                expenses_by_currencies.append(SingleExpense(currency=currency.iso_code, amount=total_amount))
            expenses_by_date.append(Expenses(date=date, by_currencies=expenses_by_currencies))
        return expenses_by_date


class Report:
    @staticmethod
    def show_report(category, start_date, end_date):
        calculation = Calculation(category, start_date, end_date)
        return calculation.calculate()


class ExpenseCRUD:
    def __init__(self):
        self.db = DBClient.current_session

    def create_expense(self, new_expense: CreateExpense):
        # TODO query category and currency by iso code and name to retrieve ids
        # TODO create Expense entity from request payload
        # TODO commit
        # View example in export_service
        pass

    def update_expense(self, id_, new_expense: UpdateExpense):
        # TODO query category and currency by iso code and name to retrieve ids (if present in payload)
        # TODO query Expense entity by id and update it
        # TODO commit
        # session.query(User). \
        #     filter(User.username == form.username.data). \
        #     update({'no_of_logins': User.no_of_logins + 1})
        # session.commit()

        pass

    def delete_expense(self, id_: int):
        # TODO query expense by id, delete and commit
        # u = db.session.get(User, 1)
        # db.session.delete(u)
        # db.session.commit()
        pass
