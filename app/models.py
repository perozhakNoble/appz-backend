import datetime

from sqlalchemy import Column, Date, ForeignKey, Integer, String, DateTime, DECIMAL as Decimal, Enum
from sqlalchemy.orm import declarative_base, relationship

from app.constants import ExportStatusEnum, ExportFileTypeEnum


class ModelBase:
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


Base = declarative_base(cls=ModelBase)


class Expense(Base):
    __tablename__ = "expense"

    date = Column(Date, nullable=False)
    amount = Column(Decimal, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)

    category = relationship("Category")
    currency = relationship("Currency")


class Currency(Base):
    __tablename__ = "currency"

    iso_code = Column(String, nullable=False)
    iso_symbol = Column(String, nullable=False)


class Category(Base):
    __tablename__ = "category"

    category_name = Column(String, nullable=False)


class Export(Base):
    __tablename__ = "export"

    name = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    status_id = Column(Integer, ForeignKey("export_status.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))
    file_type_id = Column(Integer, ForeignKey("export_file_type.id"))

    status = relationship("ExportStatus")
    category = relationship("Category")
    file_type = relationship("ExportFileType")


class ExportStatus(Base):
    __tablename__ = "export_status"

    value = Column(Enum(ExportStatusEnum))


class ExportFileType(Base):
    __tablename__ = "export_file_type"

    value = Column(Enum(ExportFileTypeEnum))
