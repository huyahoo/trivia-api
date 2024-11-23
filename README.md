## Installing Dependencies

### Backend Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the python docs.

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the python docs.

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

    ```bash
    pip install -r requirements.txt
    ```

4. **Key Dependencies**:
    - [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
    - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight sqlite database. You'll primarily work in `app.py` and can reference `models.py`.
    - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Frontend Dependencies

This project uses NPM to manage software dependencies. NPM comes packaged with Node. Before continuing, make sure you have Node installed.

1. **Installing Node and NPM** - Download and install Node and NPM from [here](https://nodejs.org/en/download/).

2. **Installing project dependencies** - Navigate to the `/frontend` directory and run:

```bash
npm install
```

## Running Your Project

### Backend

From within the `backend` directory, first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Frontend
From within the frontend directory, run:
```bash
npm start
```

## API Reference
### Getting Started
- Base URL: At present, this app can only be run locally. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "success": false,
  "error": 404,
  "message": "Resource not found"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable
- 500: Internal Server Error
### Endpoints
### GET /categories
- General:
  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```
### GET /questions?page=${integer}
- General:
  - Fetches a paginated set of questions, a total number of questions, all categories, and current category string.
  - Request Arguments: page - integer
  - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string.
- Sample: `curl http://127.0.0.1:5000/questions?page=1`
```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "total_questions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History",
  "success": true
}
```

### GET /categories/${id}/questions
- General:
  - Fetches questions for a category specified by id request argument.
  - Request Arguments: id - integer
  - Returns: An object with questions for the specified category, total questions, and current category string.
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "total_questions": 100,
  "current_category": "History",
  "success": true
}
```

### DELETE /questions/${id}
- General:
  - Deletes a specified question using the id of the question.
  - Request Arguments: id - integer
  - Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1`
```
{
  "success": true,
  "deleted": 1
}
```

### POST /quizzes
- General:
  - Sends a post request in order to get the next question.
  - Request Body:
```
{
  "previous_questions": [1, 4, 20, 15],
  "quiz_category": {
    "type": "Science",
    "id": 1
  }
}
```
  - Returns: a single new question object.
- Sample: `curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [1, 4, 20, 15], "quiz_category": {"type": "Science", "id": 1}}'`

```
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  },
  "success": true
}
```

### POST /questions
- General:
  - Sends a post request in order to add a new question.
  - Request Body:

```
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```
  - Returns: Does not return any new data.
- Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "Heres a new question string", "answer": "Heres a new answer string", "difficulty": 1, "category": 3}'`
```
{
  "success": true,
  "created": 1
}
```

### POST /questions/search
- General:
  - Sends a post request in order to search for a specific question by search term.
  - Request Body:

```
{
  "searchTerm": "this is the term the user is looking for"
}
```
  - Returns: any array of questions, a number of totalQuestions that met the search term, and the current category string.
- Sample: `curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "this is the term the user is looking for"}'`

```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "total_questions": 100,
  "current_category": "Entertainment",
  "success": true
}
```

