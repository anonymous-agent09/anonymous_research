# Copyright 2025 FIZ-Karlsruhe (Mustafa Sofean)

import warnings

warnings.filterwarnings("ignore", message='Field name "name" shadows')

import google.generativeai as genai_
from google import genai
from google.genai import types

import time
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['HTTP_PROXY'] = os.getenv('HTTP_PROXY')
os.environ['HTTPS_PROXY'] = os.getenv('HTTPS_PROXY')

gemini_api_key = os.getenv('GEMINI_API_KEY')
gemini_model = os.getenv('GEMINI_API_MODEL')


def is_plasma_physics(text: str):
    """

    :param text:
    :return:
    """
    prompt = f"""
            You are an expert research assistant tasked with identifying patent within plasma physics.
            You will be provided with patent texts and your task is to identify if the texts relate to Plasma Physics or not. 

            Instructions:         
                - Just answer with YES or NO. 
                - Use the provided ABSTRACT to understand the Plasma Physics domain.

            ABSTRACT: '''
              Plasma technology involves the use of a partially or fully ionized gas known as plasma for  various industrial, medical, and scientific applications. 
              one application of plasma physics is low-temperature plasmas which include surface treatment and modification of materials, 
              such as improving adhesion, creating surface patterns, or depositing thin films.  It is also used in biomedical applications, 
              such as sterilization and wound healing. Another application of plasma technology are Plasma medicine which involves the use of plasma 
              to treat various medical conditions and diseases, and Plasma decontamination which is a process that uses plasma to remove or inactivate biological 
              or chemical contaminants from  a surface or environment. 
                '''

             Requirements:
                - Do not include any irrelevant information.
                - Keep it concise.
                - Do not hallucinate.  

            Example 1: '''
                "TEXT":  "The present invention relates to an apparatus for generating plasma for beauty care or skin treatment."
                "Answer": YES
            ''' 
             Example 2: '''
                "TEXT":  "The present invention concerns an immunosorbent useful for reducing or removing rheumatoid factors from whole blood or blood plasma."
                "Answer": NO
            ''' 

              Text:  '''{text}'''\n
              Answer:
              """
    model = genai.Client(api_key=gemini_api_key)
    response = model.models.generate_content(model=gemini_model,
                                             contents=prompt,
                                             config=types.GenerateContentConfig(
                                                 temperature=0.0,
                                                 top_p=0.5,
                                             ),
                                             )

    return response.text.strip()


if __name__ == '__main__':
    text = "Embodiments of the subject matter disclosed herein relate to serum eye drops."
    print(is_plasma_physics(text))
