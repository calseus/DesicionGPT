import openai
import os
import requests
import json

# Set up the OpenAI API client
openai.api_key = "YOUR OPENAI API KEY"

# Function to interact with GPT-3.5-turbo
def get_gpt3_response(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai.api_key}',
    }

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a helpful assistant that understands and solves problems using the OODA loop '
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'max_tokens': 2000,
        'n': 1,
        'temperature': 0.7
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
    response_json = response.json()

    return response_json['choices'][0]['message']['content'].strip()

# Function to save the report
def save_report(report):
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report)

# Main function to execute the DECIDE code
def main():
    problem = input("Please input your problem or question:")

    # Generate questions for the Observe phase
    questions_prompt = f"Generate questions to gather more information about the problem. Don't generate questions which are same meaning. Just write questions don't write other words like explainations. Problem: {problem}"
    questions_response = get_gpt3_response(questions_prompt)
    questions = questions_response.split("\n")

    print("Please answer the following questions to help us understand the problem better:")
    observations = []
    for question in questions:
        answer = input(question + ": ")
        observations.append((question, answer))

    # Analyze the problem and observations
    observations_text = " ".join([f"{q}: {a}" for q, a in observations])
    analyze_prompt = f"Analyze the problem: {problem}. Observations: {observations_text}. Generate a list of prioritized solutions with detailed task lists and explanations for each solution. Just write solutions, explanations, and task lists don't write other words."

    # Generate solutions, explanations, and task lists
    solutions_explanations_tasks = get_gpt3_response(analyze_prompt)
    print(f"Solutions and Task List:\n{solutions_explanations_tasks}")

    # Save the report
    report = f"Problem: {problem}\n\nQuestions and Observations:\n{observations_text}\n\nSolutions, Explainations and Task List:\n{solutions_explanations_tasks}"
    save_report(report)
    print("\nReport saved successfully: report.txt")

if __name__ == "__main__":
    main()
