from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.controllers.aliexpress.aliexpress_controller import AliExpressController
from app.infrastructure.processing.rules.aliexpress_rules import RulesAliexpress
from app.infrastructure.processing.workers.aliexpress_worker import WorkerAliexpress


router = APIRouter(
    prefix="/aliexpress",
    tags=["AliExpress"]
)


class WorkerRequest(BaseModel):
    app_name: str = "Aliexpress"
    service_name: str


def get_worker() -> WorkerAliexpress:
    controller = AliExpressController()
    rules = RulesAliexpress()

    return WorkerAliexpress(
        controller=controller,
        rules=rules
    )


@router.post("/offers_day", status_code=status.HTTP_200_OK)
def offers_day(
    worker: WorkerAliexpress = Depends(get_worker)
):
    result = worker.start_worker({
        "app_name": "Aliexpress",
        "service_name": "offersDayHomePage"
    })

    return {"success": True, "result": result}


@router.post("/offers_all", status_code=status.HTTP_200_OK)
def offers_all(
    worker: WorkerAliexpress = Depends(get_worker)
):
    result = worker.start_worker({
        "app_name": "Aliexpress",
        "service_name": "offersAllHomePage"
    })

    return {"success": True, "result": result}


@router.post("/full", status_code=status.HTTP_200_OK)
def full(
    worker: WorkerAliexpress = Depends(get_worker)
):
    rules = worker.rules.full()

    offers_day_result = worker.start_worker({
        "app_name": "Aliexpress",
        "service_name": "offersDayHomePage"
    })

    offers_all_result = worker.start_worker({
        "app_name": "Aliexpress",
        "service_name": "offersAllHomePage"
    })

    return {
        "success": True,
        "result": {
            "offers_day": offers_day_result,
            "offers_all": offers_all_result
        }
    }