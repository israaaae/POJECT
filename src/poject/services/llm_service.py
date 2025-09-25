# src/services/llm_service.py
import openai
from openai import OpenAI
from ..config.settings import settings
from ..utils.logger import logger
from ..prompts.sys_prompt import SYSTEM_PROMPT_DEFAULT

class LLMService:
    def __init__(self, temperature: float = 0.0, system_prompt: str = SYSTEM_PROMPT_DEFAULT):
        self.model = settings.LLM_MODEL
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        logger.info("LLMService ready, model=%s, temperature=%s", self.model, temperature)

    def chat(self, prompt: str) -> str:
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )
            
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            else:
                logger.warning("Empty response from LLM")
                return ""
                
        except openai.APIError as e:
            logger.error("OpenAI API error: %s", e)
            raise
        except Exception as e:
            logger.error("Unexpected error in LLMService: %s", e)
            raise
