import os
from io import BytesIO
from fastapi import APIRouter, status, UploadFile, Form
from sqlalchemy.exc import IntegrityError
from typing import Optional, Union

from database.session import SessionDep
from schemas import ClientCreationSchema, Gender, ClientSchema
from schemas.security import TokenResponse
from schemas.exception import ClientAlreadyExistsException
from utils.db.client import create_client
from utils.auth import authenticate, client_dep, oauth2_form_dep
from utils.jwt import create_jwt_access_token
from utils.hash import hasher
from utils.image import add_image_watermark
from utils.log import logger
from config import settings

client_router = APIRouter(tags=["Client"])


@client_router.post(
    path="/create", status_code=status.HTTP_201_CREATED, response_model=TokenResponse
)
async def create(
    session: SessionDep,
    email: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    gender: Gender = Form(None),
    file: Optional[Union[UploadFile, str]] = None,
):
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
        email=email,
        password=hasher.get_password_hash(password),
    )
    try:
        client_id = await create_client(request, session)
    except IntegrityError as e:
        logger.error(e)
        raise ClientAlreadyExistsException

    logger.info(f"Client with email {email} has been successfully registered")
    return TokenResponse(access_token=create_jwt_access_token(client_id))


@client_router.post("/login", response_model=TokenResponse, include_in_schema=False)
async def login(form: oauth2_form_dep, session: SessionDep):
    user = await authenticate(
        email=form.username, password=form.password, session=session
    )
    return TokenResponse(access_token=create_jwt_access_token(user.id))


@client_router.get("", response_model=Optional[ClientSchema])
async def get(client: client_dep):
    return client
