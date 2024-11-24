# Telegram Bot with ChatGPT Integration

This project is a Telegram bot that uses ChatGPT for processing user questions. It features asynchronous communication with the backend, user request tracking, and request history management.

## Features

- **ChatGPT Integration**: Users can ask questions to ChatGPT.
- **Request Management**: Each user is limited to a certain number of daily requests, which reset automatically every 24 hours.
- **Request History**: Maintains a history of the last five questions and answers for each user.
- **Data Export**: Saves the current state of user data (requests and history) to a JSON file with the `/data` command.
- **Asynchronous Processing**: Leverages asynchronous communication for efficient request handling.

---

## Installation

### 1. Clone the repository:

```bash
   git clone https://github.com/yourusername/neuro_consultant_bot.git
   cd neuro_consultant_bot
```

### 2. Install dependencies:

Make sure you have Python 3.9 or higher installed. Then install the required packages:

```bash
   pip install -r requirements.txt
```

The **requirements.txt** contains the following dependencies:

```plaintext
faiss-cpu
langchain==0.0.281
openai==0.28.0
tiktoken
python-dotenv
fastapi==0.90.1
uvicorn
pydantic
```

### 3. Set up environment variables:

Create a **.env** file in the project root with the following variables:

```env
TG_TOKEN=your_telegram_bot_token
GPT_SECRET_KEY=your_openai_secret_key
```

### 4. Run the bot:

#### 1. Start the FastAPI server:

   From the `fastapi` directory, run the following command:

```bash
   uvicorn main:app --port 5000
```

#### 2.	Start the Telegram bot:

From the project root directory, run the following command:

```
python bot_run.py
```

#### 3.	Interact with the bot:

Open Telegram and start chatting with the bot: @chatGPT_UAI_bot.

## Usage

### Bot Commands

• /start: Initializes the bot for a new user and sets up default request limits.

• /data: Exports user data (remaining requests and history) to a JSON file.

### Message Handling

• Users can send text messages, and the bot responds with answers from ChatGPT.

• If request limits are reached, the bot notifies the user.

**How It Works**

Here is a diagram showing the architecture of the bot:

![Bot Diagram](neuro%20consultant.drawio.png "Bot Diagram")

**Instructions**

The bot interacts with ChatGPT using OpenAI’s API. It processes user input asynchronously, managing request limits and storing history in a structured JSON format.

**1.**	 **Backend Communication** :

 • The bot communicates with a local backend at:

    •	http://127.0.0.1:5000/api/get_answer

    •	http://127.0.0.1:5000/api/get_answer_async

**2.**	 **Request Limits** :

**•**	Each user has a daily request limit. This resets automatically every 24 hours via a background job.

**3.**	 **Data Export** :

    •	The**/data** command allows exporting user data to a JSON file, including history and remaining requests.

**Configuration**

    •**Customizable Limits**:

Modify the number of requests per user or the history size by updating the configuration in **bot_run.py**.

    •**Endpoints**:

Change backend API endpoints in the configuration section of the bot.

**Future Improvements**

•	**Enhanced User Management** :

    •	Add authentication for users.

    •	Expand user tracking to include timestamps or location-based data.

•	**Rich Media Support** :

    •	Allow users to send images or files for AI-based analysis.

•	**Scaling** :

    •	Migrate to a distributed backend for handling a larger number of users.

•	**Customization** :

    •	Add support for customizable request limits per user.

**License**

This project is licensed under the MIT License.

**Contributing**

Feel free to contribute to this project by creating a pull request or submitting issues in the GitHub repository.

**Contact**

For questions or feedback, please reach out to d.shereshevskiy@gmail.com
