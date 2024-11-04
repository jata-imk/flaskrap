from abc import ABC, abstractmethod


class IGeminiServiceInterface(ABC):
    @abstractmethod
    def init_service(self):
        pass

    @abstractmethod
    def set_model(self, model_name: str, system_instructions: str):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def send_prompt(self, prompt):
        pass
