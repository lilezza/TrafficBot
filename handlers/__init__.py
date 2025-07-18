from aiogram import Router
from .start_handler import router as start_router
from .callback_handler import router as callback_router
from .admin_list_handler import router as admin_router
from .traffic_handler import router as traffic_router

router = Router()
router.include_router(start_router)
router.include_router(callback_router)
router.include_router(admin_router)
router.include_router(traffic_router)
