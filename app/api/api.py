from fastapi import APIRouter

from app.api.endpoints import login, logout, user, token, gpt

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(logout.router, tags=["logout"])
api_router.include_router(token.router, tags=["token"])
api_router.include_router(gpt.router, prefix="/gpt", tags=["gpt"])

# @app.on_event("startup")
# async def on_app_start():
#     """before app starts"""
#     Base.metadata.create_all(bind=engine)

# @app.on_event("shutdown")
# async def on_app_shutdown():
#     """after app shutdown"""
#     print("bye~!")