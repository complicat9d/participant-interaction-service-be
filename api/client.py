import os
from io import BytesIO
from fastapi import APIRouter, status, UploadFile, Form
from sqlalchemy.exc import IntegrityError
from typing import Optional, Any, Union

from database.session import SessionDep
from schemas import ClientCreationSchema, Gender
from schemas.exception import ClientAlreadyExistsException
from utils.db.client import create_client
from utils.auth import Auth
from utils.hash import hasher
from utils.image import add_image_watermark
from utils.log import logger
from config import settings

client_router = APIRouter(tags=["Client"])


@client_router.post(path="/create", status_code=status.HTTP_200_OK, response_model=None)
async def create(
    session: SessionDep,
    auth: Auth,
    first_name: str = Form(...),
    last_name: str = Form(...),
    gender: Gender = Form(None),
    file: Optional[Union[UploadFile, str]] = None,
):
    if auth.is_new:
        output_path = None
        if file:
            output_path = os.path.join(settings.PFP_PATH, file.filename)
            await add_image_watermark(
                input_file=BytesIO(await file.read()),
                watermark_image_path=os.path.join(os.getcwd(), "data/watermark.png"),
                image_path=output_path,
            )
        request = ClientCreationSchema(
            pfp=output_path,
            gender=gender,
            first_name=first_name,
            last_name=last_name,
            email=auth.email,
            password=hasher.get_password_hash(auth.password),
        )
        try:
            await create_client(request, session)
        except IntegrityError as e:
            logger.error(e)
            raise ClientAlreadyExistsException
        logger.info(f"Client with email {auth.email} has been successfully registered")
    else:
        logger.info(
            f"Client with email {auth.email} has been successfully authenticated"
        )
