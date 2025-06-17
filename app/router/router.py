from fastapi import APIRouter
from controller.suggestcontroller import suggestController
from controller.asistantcontroller import asistantController


router = APIRouter()
router.include_router(suggestController.router)
router.include_router(asistantController.router)