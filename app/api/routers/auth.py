from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.api.deps import get_user_store, get_auth_service
from app.services.user_store import UserStore
from app.services.auth import AuthService
from app.schemas.auth import Token, UserLogin
from app.schemas.users import UserCreate, UserOut
from app.core.limiter import limiter
from app.core.errors import ErrorMessages

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
@limiter.limit("3/second")
async def login(
    request: Request,
    body: UserLogin,
    user_store: UserStore = Depends(get_user_store),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = (await user_store.get_by_username(body.username)) or (await user_store.get_by_email(body.username))

    if not user or not auth_service.verify_password(user["password"], body.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/second")
async def register(
    request: Request,
    body: UserCreate,
    user_store: UserStore = Depends(get_user_store),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user_data = body.model_dump()
        user_data["password"] = auth_service.hash_password(body.password)
        
        record = await user_store.create(user_data)
        return {
            **record,
            "user_id": str(record["uuid"]),
            "wishlist_count": 0,
        }
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
