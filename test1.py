import itertools
import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.db import DBClient
from app.models import Expense, Currency
from app.services.report_service import Calculation
from pandas import DataFrame

db_client = DBClient(host='localhost', port=5435)
db_client.connect()
db: Session = next(db_client.get_db())




if __name__ == "__main__":
    calculation = Calculation(db)


    def get_data(category, start_date, end_date):
        data = calculation.collect_data(category, start_date, end_date)

        result = []
        for item in data:
            result.append({
                'date': item.date.strftime('%m/%d/%Y'),
                'amount': item.amount,
                'currency': item.currency.iso_code,
                'category': item.category.category_name,
            })

        return DataFrame(result)

    file = get_data(None, None, None).to_excel('test.xlsx', sheet_name='Expenses report', index=False)
