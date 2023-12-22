from fastapi import HTTPException, status


class ExceptionHandling():
    NOT_IMAGE_EXCEPTION = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Please insert an image!", headers=None)

    INTERNAL_EXCEPTION = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong.. Please contact the server administrator", headers=None)

    IMAGE_NOT_FOUND_EXCEPTION = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Path is wrong. Perhaps the path formatting is wrong?", headers=None)
