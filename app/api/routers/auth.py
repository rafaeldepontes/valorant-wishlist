from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_user_store, get_auth_service
from app.services.user_store import UserStore
from app.services.auth import AuthService
from app.schemas.auth import Token, UserLogin
from app.schemas.users import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(
    body: UserLogin,
    user_store: UserStore = Depends(get_user_store),
    auth_service: AuthService = Depends(get_auth_service)
):
    user = user_store.get_by_username(body.username) or user_store.get_by_email(body.username)

    if not user or not auth_service.verify_password(user["password"], body.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username and/or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    body: UserCreate,
    user_store: UserStore = Depends(get_user_store),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user_data = body.model_dump()
        user_data["password"] = auth_service.hash_password(body.password)
        return user_store.create(user_data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
