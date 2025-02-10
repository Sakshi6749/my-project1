from flask import Flask, request, jsonify
import os
import subprocess
import openai

app = Flask(__name__)
AIPROXY_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDY3NDlAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.tMJtqZrzRqREY7E3wsFMd9PkElXEbRBpCkb533ORGEU'
# Configure OpenAI API key (using your AIPROXY_TOKEN)
openai.api_key = os.environ.get("AIPROXY_TOKEN")

@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')  # Get task description from URL
    if not task_description:
        return "Task description is required", 400  # If no task description is given, return error

    try:
        # Call the AI model to parse the task description
        task_instructions = parse_task_with_llm(task_description)

        # Execute the instructions from the AI
        result = execute_task(task_instructions)
        
        return jsonify({"message": "Task completed successfully", "result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file():
    path = request.args.get('path')  # Get file path from URL
    if not path or not os.path.exists(path):  # Check if file exists
        return "", 404  # If not found, return 404

    try:
        with open(path, 'r') as file:
            content = file.read()
        return content, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def parse_task_with_llm(task_description):
    # Send the task description to GPT-4o-Mini via AI Proxy for parsing
    prompt = f"Parse the following task and give me the instructions: {task_description}"
    response = openai.Completion.create(
        model="gpt-4o-mini",  # Replace with your LLM model name
        prompt=prompt,
        max_tokens=200
    )
    instructions = response.choices[0].text.strip()  # Get the AI response
    return instructions

def execute_task(task_instructions):
    # Placeholder logic for task execution
    if "install uv" in task_instructions:
        subprocess.run(["pip", "install", "uv"], check=True)  # Install uv
        return "UV installation completed."
    return "Task executed successfully"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
