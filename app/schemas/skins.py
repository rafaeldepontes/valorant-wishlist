from pydantic import BaseModel

class SkinOut(BaseModel):
    weapon_name: str
    skin_id: str
    skin_name: str
    image: str | None = None
