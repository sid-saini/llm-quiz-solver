import os
import time
import logging
import requests
import json
from playwright.sync_api import sync_playwright
from openai import OpenAI

logger = logging.getLogger(__name__)

class QuizSolver:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.downloads_dir = 'downloads'
        os.makedirs(self.downloads_dir, exist_ok=True)
    
    def fetch_quiz_page(self, url):
        """Fetch and render quiz page using headless browser"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until='networkidle', timeout=30000)
                time.sleep(2)  # Wait for JS execution
                content = page.content()
                text = page.inner_text('body')
                browser.close()
                return text, content
        except Exception as e:
            logger.error(f"Error fetching page: {e}")
            return None, None
    
    def solve_with_llm(self, question_text, html_content):
        """Use LLM to understand and solve the quiz"""
        prompt = f"""You are a data analysis expert. Analyze this quiz question and provide a solution plan.

Question:
{question_text}

HTML (for reference):
{html_content[:2000]}

Provide:
1. What data needs to be downloaded/accessed
2. What operations need to be performed
3. The expected answer format (boolean, number, string, base64, or JSON object)
4. Step-by-step solution approach

Be specific about URLs, file formats, and calculations needed."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return None

    
    def execute_solution(self, solution_plan, question_text):
        """Execute the solution based on LLM plan"""
        execution_prompt = f"""Based on this solution plan, provide executable Python code to solve the problem.

Solution Plan:
{solution_plan}

Original Question:
{question_text}

Generate Python code that:
1. Downloads/fetches required data
2. Processes and analyzes it
3. Returns the final answer in the correct format
4. Stores the answer in a variable called 'final_answer'

Only provide the Python code, no explanations."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": execution_prompt}],
                temperature=0.1
            )
            code = response.choices[0].message.content
            # Extract code from markdown if present
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()
            
            # Execute code safely
            local_vars = {}
            exec(code, {"__builtins__": __builtins__, "requests": requests, 
                       "json": json, "os": os}, local_vars)
            
            return local_vars.get('final_answer')
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return None
    
    def submit_answer(self, submit_url, email, secret, quiz_url, answer):
        """Submit answer to the quiz endpoint"""
        payload = {
            "email": email,
            "secret": secret,
            "url": quiz_url,
            "answer": answer
        }
        
        try:
            response = requests.post(submit_url, json=payload, timeout=30)
            return response.json()
        except Exception as e:
            logger.error(f"Submit error: {e}")
            return None
    
    def solve_quiz_chain(self, initial_url, email, secret):
        """Solve a chain of quizzes"""
        current_url = initial_url
        start_time = time.time()
        max_time = 180  # 3 minutes
        
        while current_url and (time.time() - start_time) < max_time:
            logger.info(f"Solving quiz: {current_url}")
            
            # Fetch quiz page
            text, html = self.fetch_quiz_page(current_url)
            if not text:
                logger.error("Failed to fetch quiz page")
                break
            
            # Extract submit URL from text
            submit_url = None
            for line in text.split('\n'):
                if 'submit' in line.lower() and 'http' in line:
                    import re
                    urls = re.findall(r'https?://[^\s<>"]+', line)
                    if urls:
                        submit_url = urls[0]
                        break
            
            if not submit_url:
                logger.error("Could not find submit URL")
                break
            
            # Solve with LLM
            solution_plan = self.solve_with_llm(text, html)
            if not solution_plan:
                logger.error("Failed to generate solution plan")
                break
            
            logger.info(f"Solution plan: {solution_plan[:200]}...")
            
            # Execute solution
            answer = self.execute_solution(solution_plan, text)
            if answer is None:
                logger.error("Failed to execute solution")
                break
            
            logger.info(f"Submitting answer: {answer}")
            
            # Submit answer
            result = self.submit_answer(submit_url, email, secret, current_url, answer)
            if not result:
                logger.error("Failed to submit answer")
                break
            
            logger.info(f"Result: {result}")
            
            if result.get('correct'):
                logger.info("Answer correct!")
                current_url = result.get('url')
            else:
                logger.warning(f"Answer incorrect: {result.get('reason')}")
                # Try next URL if provided, or retry
                next_url = result.get('url')
                if next_url and next_url != current_url:
                    current_url = next_url
                else:
                    break
        
        logger.info("Quiz chain completed")
