# Quizify Web Application

Quizify is a web application designed to empower interactive learning and engagement through quizzes. It allows users to register, log in, create quizzes, and take quizzes created by other users.

## Table of Contents
>> Installation
>> Usage
>> Features
>> File Structure
>> Technologies Used
>> Contributing
>> License

## Installation
To run Quizify locally on your machine, follow these steps:

1. Clone the repository
```bash
git clone <repository_url >
```

2. Navigate to the project directory
```bash
cd Quizify
```

3. Create a virtual environment:
```bash
python3 -m venv venv
```

4. Activate the virtual environment:
>> On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```

>> On Windows:
  ```bash
  venv\Scripts\activate
  ```

5. Install the required dependencies:
```bash
pip install -r requirements.txt
```

6. Set up the environment variables:
. Create a .env file in the project root directory.
. Add the following environment variables to the .env file:

    SECRET_KEY=your_secret_key
    DATABASE_URL=your_database_url



