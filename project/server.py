import logging
from contextlib import asynccontextmanager

import project.refine_prompt_service
import project.validate_api_key_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="klamala",
    lifespan=lifespan,
    description="To create a single API endpoint that takes in a string LLM prompt and returns a refined version improved by GPT-4, leveraging the tech stack provided, the following approach is taken:\n\n1. **FastAPI for API Framework**: FastAPI is chosen for its speed and ease of use in creating RESTful APIs. It allows asynchronous request handling and automatic request validation which is beneficial for this project.\n\n2. **PostgreSQL for Database**: PostgreSQL will store the original and refined prompts for auditing and improvement purposes. It's a robust, SQL-compliant database with wide support for different types of data and high scalability.\n\n3. **Prisma as ORM**: Prisma is used to interface with the PostgreSQL database efficiently. It simplifies database operations with its intuitive query builder, migrations, and easy setup process.\n\n4. **Python and OpenAI Python Package**: The core functionality of interfacing with GPT-4 to refine prompts is implemented in Python, utilizing the OpenAI Python package. Python's extensive libraries and the OpenAI package facilitate easy integration with GPT-4.\n\n5. **API Security with API Key**: The API endpoint is protected using the API key 'USPERAKDJOWEKMCOISO'. Using FastAPI's Dependency Injection system with the APIKeyHeader class, each request to the endpoint is authenticated by checking the provided API key against the expected one.\n\n### Implementation Steps:\n\n- **Develop the FastAPI application** including a POST endpoint `/refine-prompt` which accepts a JSON payload containing the 'prompt' string.\n- **Secure the endpoint** by creating a dependency function that validates the 'access_token' header against the pre-defined API key.\n- **Interface with GPT-4** using the OpenAI Python package for prompt refinement. This involves sending the user's prompt to GPT-4 and receiving a refined prompt response.\n- **Save requests and responses** in PostgreSQL for record-keeping and future analysis.\n\n### Code Snippet Example:\n```python\nfrom fastapi import FastAPI, Security, HTTPException, Depends\nfrom fastapi.security.api_key import APIKeyHeader\nimport openai\n\napp = FastAPI()\n\nAPI_KEY = 'USPERAKDJOWEKMCOISO'\nAPI_KEY_NAME = 'access_token'\napi_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)\n\nasync def get_api_key(api_key_header: str = Security(api_key_header)):\n    if api_key_header == API_KEY:\n        return api_key_header\n    else:\n        raise HTTPException(status_code=403, detail='Could not validate credentials')\n\n@app.post('/refine-prompt')\nasync def refine_prompt(prompt: str, api_key: APIKey = Depends(get_api_key)):\n    refined_prompt = '' # The logic to call GPT-4 and refine the prompt goes here\n    return {'original_prompt': prompt, 'refined_prompt': refined_prompt}\n```\n\nThis implementation ensures secure, efficient, and scalable prompt refining services using advanced AI techniques.",
)


@app.post(
    "/refine-prompt", response_model=project.refine_prompt_service.RefinePromptResponse
)
async def api_post_refine_prompt(
    prompt: str, user_id: str
) -> project.refine_prompt_service.RefinePromptResponse | Response:
    """
    Accepts a user's prompt and returns a refined version using GPT-4.
    """
    try:
        res = await project.refine_prompt_service.refine_prompt(prompt, user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/validate-api-key",
    response_model=project.validate_api_key_service.APIKeyValidationResponse,
)
async def api_post_validate_api_key(
    api_key: str,
) -> project.validate_api_key_service.APIKeyValidationResponse | Response:
    """
    Validates the provided API key for accessing the refine-prompt endpoint.
    """
    try:
        res = await project.validate_api_key_service.validate_api_key(api_key)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
