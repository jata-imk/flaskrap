from datetime import datetime
from app.main.models.PromptHistory import PromptHistory
from app.main.interfaces.gemini_service_interface import IGeminiServiceInterface
from app.main.repositories.prompt_history_repository import PromptHistoryRepository


class RequestPromptForProductUseCase:
    gemini_service: IGeminiServiceInterface
    prompt_history_repository: PromptHistoryRepository

    def __init__(
        self,
        gemini_service: IGeminiServiceInterface,
        prompt_history_repository: PromptHistoryRepository,
    ):
        self.gemini_service = gemini_service
        self.prompt_history_repository = prompt_history_repository

    def execute(
        self,
        product_id: int,
        prompt: str,
    ) -> PromptHistory:
        today = datetime.now().date()
        existing_prompt = (
            self.prompt_history_repository.get_by_product_id_and_created_at(
                product_id, today
            )
        )

        if existing_prompt:
            return existing_prompt

        response = None
        try:
            response = self.gemini_service.send_prompt(prompt)
        except Exception as e:
            # Log the exception details here
            raise e

        prompt_history_model = PromptHistory(
            prompt=prompt,
            response=response.text,
            product_id=product_id,
            api="GOOGLE GEMINI",
            created_at=datetime.now(),
        )

        self.prompt_history_repository.create(prompt_history_model)
        return prompt_history_model
