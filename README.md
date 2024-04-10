---
date: 2024-04-10T14:05:37.247548
author: AutoGPT <info@agpt.co>
---

# klamala

To create a single API endpoint that takes in a string LLM prompt and returns a refined version improved by GPT-4, leveraging the tech stack provided, the following approach is taken:

1. **FastAPI for API Framework**: FastAPI is chosen for its speed and ease of use in creating RESTful APIs. It allows asynchronous request handling and automatic request validation which is beneficial for this project.

2. **PostgreSQL for Database**: PostgreSQL will store the original and refined prompts for auditing and improvement purposes. It's a robust, SQL-compliant database with wide support for different types of data and high scalability.

3. **Prisma as ORM**: Prisma is used to interface with the PostgreSQL database efficiently. It simplifies database operations with its intuitive query builder, migrations, and easy setup process.

4. **Python and OpenAI Python Package**: The core functionality of interfacing with GPT-4 to refine prompts is implemented in Python, utilizing the OpenAI Python package. Python's extensive libraries and the OpenAI package facilitate easy integration with GPT-4.

5. **API Security with API Key**: The API endpoint is protected using the API key 'USPERAKDJOWEKMCOISO'. Using FastAPI's Dependency Injection system with the APIKeyHeader class, each request to the endpoint is authenticated by checking the provided API key against the expected one.

### Implementation Steps:

- **Develop the FastAPI application** including a POST endpoint `/refine-prompt` which accepts a JSON payload containing the 'prompt' string.
- **Secure the endpoint** by creating a dependency function that validates the 'access_token' header against the pre-defined API key.
- **Interface with GPT-4** using the OpenAI Python package for prompt refinement. This involves sending the user's prompt to GPT-4 and receiving a refined prompt response.
- **Save requests and responses** in PostgreSQL for record-keeping and future analysis.

### Code Snippet Example:
```python
from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
import openai

app = FastAPI()

API_KEY = 'USPERAKDJOWEKMCOISO'
API_KEY_NAME = 'access_token'
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail='Could not validate credentials')

@app.post('/refine-prompt')
async def refine_prompt(prompt: str, api_key: APIKey = Depends(get_api_key)):
    refined_prompt = '' # The logic to call GPT-4 and refine the prompt goes here
    return {'original_prompt': prompt, 'refined_prompt': refined_prompt}
```

This implementation ensures secure, efficient, and scalable prompt refining services using advanced AI techniques.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'klamala'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
