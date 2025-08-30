import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.outputs import LLMResult
from config import GeminiModel


load_dotenv()


class GoogleLLMClient:
    def __init__(self, model_name: GeminiModel = GeminiModel.GEMINI_2_5_FLASH, temperature = 0.7):
        """
        initialize LLMClient

        Args:
            model_name (str): name of the model
            temperature (float): for adjustment results. It plays as a determinism when close to 0 and a creativity when close to 1.
        """


        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY environment variable not set")

        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

        print(f"✅LLM Client initialized with model name: {model_name}")

    def invoke(self, prompt: str) -> str:
        """
            Invoking LLM with prompts, which responses string result.

            Args:
                prompt (str): prompt to be invoked.
            Returns:
                str: text which response from LLM.
        """
        result = self.llm.invoke(prompt)
        return result.content

    def batch(self, prompts: list[str]) -> LLMResult:
        """
            batching while prompts are inserted at once.
            Args:
                prompts (list[str]): list of prompts.
            Returns:
                LLMResult: result of batching.
        """
        return self.llm.generate(prompts)




if __name__ == '__main__':
    try:
        client = GoogleLLMClient(
            model_name=GeminiModel.GEMINI_2_5_FLASH,
            temperature=0.7
        )

        response = client.invoke("hello")

    except ValueError as e:
        print(f"Error: {e}")
