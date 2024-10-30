from fastapi import HTTPException, status


ClientAlreadyExistsException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Client with the given email already exists",
)

ClientNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
)

IncorrectPasswordException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Incorrect password for the user with given email",
)

IncorrectEmailFormatException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Incorrect format of email",
)
