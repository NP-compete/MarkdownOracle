import requests
import json
from langchain.llms.base import BaseLLM
from langchain.schema.runnable import Runnable
from pydantic import Field
from langchain.schema import LLMResult, Generation

class OllamaLLM(BaseLLM, Runnable):
    base_url: str = Field(
        default="http://ollama:11434", description="Base URL for Ollama server"
    )
    model_name: str = Field(
        default="llama3.2", description="Name of the model to query"
    )

    def _call(self, prompt: str, stop: list = None) -> str:
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        payload = {"prompt": prompt, "stop": stop, "model": self.model_name, "stream": False}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = json.loads(response.text)['response']
            return data
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error querying Ollama model: {e}")

    def _generate(self, prompts: list[str], stop: list = None) -> LLMResult:
        generations = []
        for prompt in prompts:
            text = self._call(prompt, stop)
            generations.append([Generation(text=text)])
        return LLMResult(generations=generations)

    @property
    def _llm_type(self) -> str:
        return "ollama"
