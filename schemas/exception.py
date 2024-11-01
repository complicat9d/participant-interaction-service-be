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

ClientAuthenticationFailedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Client could not be authenticated"
)

ReactionsAmountExceededException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Client has exceeded amount of reactions per day",
)

IncorrectCoordinatesFormatException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Incorrect format of either longitude or latitude",
)

InvalidDateRangeException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Incorrect format: from_date must be strictly less, than until date",
)
