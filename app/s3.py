import uuid
from minio import Minio
from minio.error import S3Error
from app.config import settings

#создание клиента минио
minio_client = Minio(
    endpoint=settings.minio_endpoint, #localhost:9000
    access_key=settings.minio_access_key, #minioadmin
    secret_key=settings.minio_secret_key, #minioadmin
    secure=False # False для HTTP, True для HTTPS
)

#загружает файл на Minio и возвращает URL.
    # - file: файловый объект (например, UploadFile.file)
    # - file_name: оригинальное название файла
    # - content_type: MIME тип файла
def upload_image(file, file_name:str, content_type:str) -> str:
    #уникальное имя для файла
    unique_filename = f'{uuid.uuid4().hex}_{file_name}'

    #получаем размер файла (чтобы можно было передать его в put_object)
    file.seek(0, 2)  # Перемещаем курсор в конец файла
    file_size = file.tell()
    file.seek(0)  # Возвращаем курсор в начало файла

    try:
        minio_client.put_object(
            bucket_name=settings.minio_bucket,
            object_name=unique_filename,
            data=file,
            length=file_size,
            content_type=content_type,
        )
    except S3Error as e:
        raise Exception(f'minio error: {e}')

# Формируем URL для доступа к изображению
    url = f"http://{settings.minio_endpoint}/{settings.minio_bucket}/{unique_filename}"
    return url




