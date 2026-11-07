from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.application.use_cases.aliexpress.home_page import homePageExtract
from app.controllers.aliexpress.aliexpress_controller import AliExpressController
from app.infrastructure.processing.rules.aliexpress_rules import RulesAliexpress
from app.infrastructure.processing.workers.aliexpress_worker import WorkerAliexpress


router = APIRouter(
    prefix="/aliexpress",
    tags=["AliExpress"]
)


class WorkerRequest(BaseModel):
    app_name: str
    service_name: str


def get_worker() -> WorkerAliexpress:
    home_page = homePageExtract()

    rules = RulesAliexpress(home_page)
    controller = AliExpressController(home_page)

    return WorkerAliexpress(
        controller=controller,
        rules=rules
    )


@router.post("/execute", status_code=status.HTTP_200_OK)
def execute_worker(
    request: WorkerRequest,
    worker: WorkerAliexpress = Depends(get_worker)
):
    result = worker.start_worker(request.model_dump())

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aplicação ou serviço não encontrado"
        )

    return {
        "success": True,
        "result": result
    }