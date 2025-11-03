from fastapi import APIRouter

from .demo_jwt_auth.jwt_auth import router as demo_jwt_auth_router
from .demo_jwt_auth.views import router as demo_auth_router
from .products.views import router as products_router
from .users.views import router as users_router

router = APIRouter()
router.include_router(router=users_router, prefix="/users")
router.include_router(router=products_router, prefix="/products")
router.include_router(router=demo_auth_router)
router.include_router(router=demo_jwt_auth_router)
