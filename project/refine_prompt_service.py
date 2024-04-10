import openai
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class RefinePromptResponse(BaseModel):
    """
    This model represents the response data returned to the user after the prompt refinement process. It contains both the original and the refined prompts.
    """

    original_prompt: str
    refined_prompt: str
    user_id: str
    status: str


async def refine_prompt(prompt: str, user_id: str) -> RefinePromptResponse:
    """
    Accepts a user's prompt and returns a refined version using GPT-4.

    This function takes a user's prompt and their identifier, sends the prompt to GPT-4 for refinement,
    and optionally stores the original and refined prompts in the database associated with the user.
    Finally, it returns both versions of the prompt and the status of the operation.

    Args:
        prompt (str): The original, unrefined prompt provided by the user.
        user_id (str): The identifier for the user submitting the prompt.

    Returns:
        RefinePromptResponse: This model represents the response data returned to the user after
        the prompt refinement process. It contains both the original and the refined prompts,
        user identification, and the status of the process.

    Example:
        refine_prompt("How can I improve my Python skills?", "12345678-1234-1234-1234-123456789012")
        > RefinePromptResponse(original_prompt="How can I improve my Python skills?",
                               refined_prompt="What are effective strategies for enhancing my Python programming competence?",
                               user_id="12345678-1234-1234-1234-123456789012", status="COMPLETED")
    """
    openai.api_key = "your_openai_api_key_here"
    try:
        response = await openai.Completion.create(
            engine="text-davinci-003", prompt=prompt, max_tokens=100
        )  # TODO(autogpt): "Generator[Unknown | list[Unknown] | dict[Unknown, Unknown], None, None]" is not awaitable
        #     "Generator[Unknown | list[Unknown] | dict[Unknown, Unknown], None, None]" is incompatible with protocol "Awaitable[_T_co@Awaitable]"
        #       "__await__" is not present. reportGeneralTypeIssues
        choices = response.choices if response.choices else []
        refined_prompt_text = choices[0].text.strip() if choices else ""
        user_exists = await prisma.models.User.prisma().find_unique(
            where={"id": user_id}
        )
        if not user_exists:
            return RefinePromptResponse(
                original_prompt=prompt,
                refined_prompt="",
                user_id=user_id,
                status="FAILED",
            )
        await prisma.models.UserSubmittedPrompt.prisma().create(
            data={
                "original": prompt,
                "refined": refined_prompt_text,
                "userId": user_id,
                "status": prisma.enums.PromptStatus.COMPLETED,
            }
        )
        return RefinePromptResponse(
            original_prompt=prompt,
            refined_prompt=refined_prompt_text,
            user_id=user_id,
            status="COMPLETED",
        )
    except Exception as e:
        await prisma.models.ErrorLog.prisma().create(
            data={"error": str(e), "promptId": ""}
        )
        return RefinePromptResponse(
            original_prompt=prompt, refined_prompt="", user_id=user_id, status="FAILED"
        )
