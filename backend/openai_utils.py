import os
import openai

# Make sure to set your OPENAI_API_KEY as an environment variable
openai.api_key = os.getenv("openai_api_key")


def get_priority_and_quadrant(title, description, deadline):
    prompt = f"""
You are a project management assistant. Given the task below, determine the priority level (High, Medium, Low) and the Eisenhower Matrix quadrant it belongs to (Important & Urgent, Important Not Urgent, Not Important Urgent, Not Important Not Urgent).

Task Title: {title}
Description: {description}
Deadline: {deadline}

Return a JSON object with exactly two fields: "priority" and "quadrant".
Example response:
{{
  "priority": "High",
  "quadrant": "Important & Urgent"
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",    # Use the appropriate model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=100,
        )
        text_response = response['choices'][0]['message']['content'].strip()
        return text_response

    except Exception as e:
        print("OpenAI API error:", e)
        # Fallback response
        return '''
        {
            "priority": "Medium",
            "quadrant": "Important, Not Urgent"
        }
        '''
