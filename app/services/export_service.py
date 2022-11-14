from pandas import DataFrame
from sqlalchemy.orm import Session

from app.constants import ExportFileTypeEnum, ExportStatusEnum
from app.db import DBClient
from app.logger import Logger
from app.services.report_service import Calculation
from app.models import Export as ExportModel, Category, ExportFileType, ExportStatus

logger = Logger.get_logger()


class Export:
    def __init__(self, category, start_date, end_date):
        self.db: Session = DBClient.current_session
        self.start_date = start_date
        self.end_date = end_date
        self.category = category
        self.calculation = Calculation(category, start_date, end_date)

    def get_data(self):
        data = self.calculation.collect_data()

        result = []
        for item in data:
            result.append({
                'date': item.date.strftime('%m/%d/%Y'),
                'amount': item.amount,
                'currency': item.currency.iso_code,
                'category': item.category.category_name,
            })

        return DataFrame(result)

    def get_name(self):
        start = self.start_date.strftime('%m/%d/%Y') if self.start_date else None
        end = self.end_date.strftime('%m/%d/%Y') if self.end_date else None

        period = f'({start} - {end})'
        name = f'Expenses report {" - " + self.category if self.category else ""}{period if start and end else ""}'
        return name

    def get_export_entity(self, file_type: ExportFileTypeEnum):
        category = self.db.query(Category).filter(Category.category_name == self.category).first()
        file_type_id = self.db.query(ExportFileType).filter(ExportFileType.value == file_type).first()

        return ExportModel(
            name=self.get_name(),
            start_date=self.start_date,
            end_date=self.end_date,
            category_id=category.id if category else None,
            file_type_id=file_type_id.id,
        )

    def export(self):
        pass

    @property
    def success_status(self):
        success = self.db.query(ExportStatus).filter(ExportStatus.value == ExportStatusEnum.SUCCESS).first()
        return success.id

    @property
    def error_status(self):
        error = self.db.query(ExportStatus).filter(ExportStatus.value == ExportStatusEnum.ERROR).first()
        return error.id


class XLSExport(Export):
    def __init__(self, category, start_date, end_date):
        super().__init__(category, start_date, end_date)

    def export(self):
        data = self.get_data()

        export_entity = self.get_export_entity(ExportFileTypeEnum.XLS)

        try:
            logger.log("Report export started")
            data.to_excel("output.xlsx", sheet_name='Expenses report', index=False)
            export_entity.status_id = self.success_status
            self.db.add(export_entity)
            self.db.commit()
        except Exception:
            export_entity.status_id = self.error_status
            self.db.add(export_entity)
            self.db.commit()
            raise
