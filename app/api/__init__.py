from fastapi import APIRouter, Depends

from app.api.expenses import expenses_router
from app.api.export import export_router
from app.db import db_client, DBClient


def add_db_session(session=Depends(db_client.get_db)):
    DBClient.current_session = session


router = APIRouter(dependencies=[Depends(add_db_session)])
router.include_router(expenses_router)
router.include_router(export_router)
