# Project Name

This project is a chatbot application with a Python frontend and a Rust backend. The Python frontend handles user interactions and sends requests to the Rust backend, which processes the messages.

## Project Structure

- `main.py`: This is the Python frontend, which interacts with the user and communicates with the Rust backend via HTTP requests.
- `main.rs`: This is the Rust backend that processes the messages received from the Python frontend and returns appropriate responses.

## Prerequisites

To run this project, you'll need the following:

- **Python 3.x**: Ensure Python is installed on your system.
- **Rust**: Ensure Rust installed on your system.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/open-llm-initiative/open-message-format.git
cd .\examples\chatbot\
```

### Step 2: Set Up a Python Virtual Environment and Install Dependencies

It is recommended to use a virtual environment to manage your Python dependencies. Follow these steps to set up a virtual environment:

1. Navigate to the directory containing `main.py`:

```bash
 cd .\chatbot_frontend\
```
&nbsp;
2. Create a virtual environment:

```bash
python -m venv .venv
```

This will create a directory named `.venv` containing the virtual environment.
&nbsp;
3. Activate the virtual environment:

- On **Windows**:

```bash
.venv\Scripts\activate
```

- On **macOS/Linux**:

```bash
source .venv/bin/activate
```
&nbsp;
4. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```
&nbsp;
5. Go back to the directory containing both the front and backend:

```bash
cd ..
```
&nbsp;
### Step 3.

Create a .env file in the backend directory:

1. Navigate to the backend directory:
   
``` bash
cd .\chatbot_backend\
```
&nbsp;
2. create a new file called .env
&nbsp;
3. In the .env file, set the values for `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `MISTRAL_API_KEY`
&nbsp;   
4. return to the chatbot directory:

```bash
cd ..
```

## Running the Project

### Step 1. Start the Rust Backend

First, navigate to the directory containing main.rs and compile the Rust backend:

```bash
cd .\chatbot_backend\ 
cargo run --release
```

### Step 2. Run the Python Frontend

In a terminal, Navigate to the directory containing main.py and run the Python script:

```bash
cd ..
cd .\chatbot_frontend\
python main.py
```

### Step 3: Interact with the Chatbot

Once both the backend and frontend are running, you can start interacting with the chatbot via the terminal in the front end.

- Type your messages, and the chatbot will respond.
- To exit the chatbot, type `exit` or `quit`.

If you wish to change the LLM being used, you can interact with the backend via it's terminal, just type in one of three responses offered by the program:

```bash
anthropic
openai
mistral
```
