from datetime import date
from typing import Optional, List

from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.schemas import Expenses, CreateExpense, UpdateExpense
from app.services.report_service import Report, ExpenseCRUD

expenses_router = APIRouter(prefix='/expenses')


@expenses_router.get("/", response_model=List[Expenses])
def get_report(
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
):
    return Report.show_report(category, start_date, end_date)


@expenses_router.post("/")
def create_expense(new_expense: CreateExpense):
    expense_crud = ExpenseCRUD()
    expense_crud.create_expense(new_expense)
    return JSONResponse({'message': 'Expense was created successfully'}, status_code=201)


@expenses_router.put("/{id_}")
def update_expense(id_, new_expense: UpdateExpense):
    expense_crud = ExpenseCRUD()
    expense_crud.update_expense(id_, new_expense)
    return JSONResponse({'message': 'Expense was updated successfully'}, status_code=200)


@expenses_router.delete("/{id_}")
def delete_expense(id_):
    expense_crud = ExpenseCRUD()
    expense_crud.delete_expense(id_)
    return JSONResponse({'message': 'Expense was deleted successfully'}, status_code=204)
