from app.main.interfaces.gemini_service_interface import IGeminiServiceInterface
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()


class GoogleGeminiService(IGeminiServiceInterface):
    model = None

    def init_service(self):
        """Initializes the service by setting the api key for the gemini library"""
        genai.configure(api_key=os.getenv("GOOGLE_GEMINI_APIKEY"))

        return self

    def set_model(
        self, model_name: str = "gemini-1.5-flash", system_instructions: str = None
    ):
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instructions,
        )

        return self

    def get_model(self):
        return self.model

    def send_prompt(self, prompt):
        model = self.get_model()

        response = model.generate_content(prompt)

        return response
