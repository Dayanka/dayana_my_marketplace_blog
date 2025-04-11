from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.s3 import upload_image
from app.api.v1.dependencies import get_current_user
from app.models.user import User


router = APIRouter(prefix="/images", tags=["images"])

@router.post("/", summary="Загрузка изображения")
async def upload_image_endpoint(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user) #тк нужна авторизация
):
    #Ззагрузка файл на minio
    try:
        image_url = upload_image(file.file, file.filename, file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"filename": file.filename, "url": image_url}
