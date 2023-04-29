from fastapi import APIRouter

from .resource import router as _resource_router
from .resources_emulation import router as _resource_emulation_router
from .general import lifespan
from .general import router as _general_router

router = APIRouter(prefix='/api')
router.include_router(_resource_router)
router.include_router(_resource_emulation_router)
router.include_router(_general_router)

__all__ = ['router', 'lifespan']
