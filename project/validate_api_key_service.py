from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class APIKeyValidationResponse(BaseModel):
    """
    This model represents the outcome of an API Key validation request. It informs the client whether the submitted API key is valid or not.
    """

    is_valid: bool
    message: Optional[str] = None


async def validate_api_key(api_key: str) -> APIKeyValidationResponse:
    """
    Validates the provided API key for accessing the refine-prompt endpoint.

    Args:
        api_key (str): The API key submitted by the client for validation.

    Returns:
        APIKeyValidationResponse: This model represents the outcome of an API Key validation request.
        It informs the client whether the submitted API key is valid or not.

    Example:
        api_key = 'USPERAKDJOWEKMCOISO'
        response = await validate_api_key(api_key)
        if response.is_valid:
            print("API key is valid.")
        else:
            print(f"API key is invalid: {response.message}")
    """
    api_key_record = await prisma.models.APIKey.prisma().find_unique(
        where={"key": api_key}
    )
    if api_key_record and api_key_record.valid:
        return APIKeyValidationResponse(is_valid=True)
    else:
        return APIKeyValidationResponse(
            is_valid=False, message="API Key is invalid or deactivated."
        )
