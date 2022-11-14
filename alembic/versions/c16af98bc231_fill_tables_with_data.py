"""Fill tables with data

Revision ID: c16af98bc231
Revises: d02ee0b5a61f
Create Date: 2022-11-12 14:50:40.989606

"""
import datetime
import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import Session

from app.constants import ExportStatusEnum, ExportFileTypeEnum
from app.models import Category, ExportStatus, ExportFileType, Currency, Expense

# revision identifiers, used by Alembic.
revision = 'c16af98bc231'
down_revision = 'd02ee0b5a61f'
branch_labels = None
depends_on = None

bind = op.get_bind()
db: Session = orm.Session(bind=bind)


def fill_expenses_table():
    with open('expenses.json') as file:
        expenses_data = json.loads(file.read())
        expenses = []
        for expense in expenses_data:
            expenses.append(Expense(
                date=datetime.datetime.strptime(expense['date'], '%m/%d/%Y').date(),
                amount=expense['amount'],
                currency_id=expense['currency_id'],
                category_id=expense['category_id'],
            ))
        db.add_all(expenses)
        db.commit()


def upgrade():
    categories = [
        Category(category_name="Проживання"),
        Category(category_name="Харчування"),
        Category(category_name="Одяг"),
        Category(category_name="Предмети гігієни"),
        Category(category_name="Дитячі іграшки")
    ]
    db.add_all(categories)
    statuses = [
        ExportStatus(value=ExportStatusEnum.SUCCESS),
        ExportStatus(value=ExportStatusEnum.ERROR),
    ]
    db.add_all(statuses)
    formats = [
        ExportFileType(value=ExportFileTypeEnum.PDF),
        ExportFileType(value=ExportFileTypeEnum.CSV),
        ExportFileType(value=ExportFileTypeEnum.XLS),
    ]
    db.add_all(formats)

    currencies = [
        Currency(iso_code='USD', iso_symbol='$'),
        Currency(iso_code='UAH', iso_symbol='₴'),
    ]
    db.add_all(currencies)
    db.commit()
    fill_expenses_table()


def downgrade() -> None:
    op.execute("""
    delete from category;
    delete from export_status;
    delete from export_file_type;
    delete from currency;
    """)
