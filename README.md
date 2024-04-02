# Blog Application

## Description

This project is a blog application featuring user authentication, blog post management with rich text formatting, commenting system, and a user follow system. It is built with a Streamlit frontend, a MySQL backend, and Flask for connecting the frontend and backend.

## Tech Stacks Used

- **Backend**: Flask, MySQL
- **Frontend**: Streamlit
- **Database**: MySQL
- **API**: FastAPI


## Working Flow 
### User Authentication

- **Signup**: 
    - Accepts a unique username and password from the user.
    - Stores the user's details in the MySQL database after validating the uniqueness of the username.
  
- **Login**: 
    - Accepts a username and password from the user.
    - Validates the credentials by checking them against the stored data in the MySQL database.
    - Generates and returns a JWT token upon successful authentication.
  
- **Profile Editing**: 
    - Allows authenticated users to modify their username and password.
    - Updates the user's details in the MySQL database after validation.

### Blog Post Management

- **Create Blog**: 
    - Accepts a title and content from the user.
    - Stores the blog post in the MySQL database, associating it with the authenticated user.

- **Update Blog**: 
    - Accepts a blog post title, and content from the user.
    - Updates the specified blog post in the MySQL database.

- **Delete Blog**: 
    - Accepts a blog post ID from the user.
    - Deletes the specified blog post from the MySQL database, validating ownership.

### Comments

- **Create Comment**: 
    - Accepts a blog post comment content from the user.
    - Stores the comment in the MySQL database, associating it with the authenticated user and the specified blog post.

- **Edit Comment**: 
    - Updates the specified comment in the MySQL database.

- **Delete Comment**: 
    - Deletes the specified comment from the MySQL database, validating ownership.

### User Follow System

- **Follow Users**: 
    - Stores the follow relationship in the MySQL database.

## FastAPI in the Project

## FastAPI Usage Description:

### Web Application Framework:

FastAPI serves as the main web application framework, allowing for the creation of API endpoints to handle HTTP requests and responses. The use of FastAPI simplifies the process of building robust and scalable web APIs.

### Endpoint Definitions:

FastAPI decorators (`@app.post`, `@app.get`, `@app.put`, `@app.delete`) are used to define the API endpoints for various functionalities of the blogging application:

#### User Authentication:

- `@app.post("/signup/")`: Endpoint to register a new user.
- `@app.post("/login/")`: Endpoint to authenticate a user.

#### User Profile Management:

- `@app.put("/edit-profile/")`: Endpoint to update a user's profile.

#### Blog Management:

- `@app.post("/create-blog/")`: Endpoint to create a new blog post.
- `@app.get("/my-blogs/{username}")`: Endpoint to retrieve all blogs by a specific user.
- `@app.put("/edit-blog/{blog_id}")`: Endpoint to edit a blog post.
- `@app.delete("/delete-blog/{blog_id}")`: Endpoint to delete a blog post.

#### Comment Management:

- `@app.post("/create-comment/")`: Endpoint to create a new comment on a blog post.
- `@app.get("/get-comments/{blog_id}")`: Endpoint to retrieve all comments for a specific blog post.
- `@app.put("/update-comment/")`: Endpoint to update a comment.
- `@app.delete("/delete-comment/{comment_id}")`: Endpoint to delete a comment.

#### Follow User:

- `@app.post("/follow/")`: Endpoint to allow a user to follow another user.

#### View Public Blogs:

- `@app.get("/view-public-blogs/")`: Endpoint to view all public blog posts.

### Data Validation:

FastAPI integrates seamlessly with Pydantic, a data validation library. Pydantic models (`User`, `UserProfile`, `Blog`, `Comment`, `Follow`) are used to define the structure of the request and response data for each API endpoint. This ensures that the incoming data is validated against the specified model before being processed, improving the robustness and reliability of the application.

### Database Operations:

- Connecting to the SQLite database.
- Executing SQL queries to insert, retrieve, update, or delete data.

## Setup Instructions:

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/blog-app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd blog-app
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    uvicorn main:app --reload
    ```
5. Run the Streamlit application:

    ```bash
    streamlit run streamlit_frontend.py
    ```

## License:

This project is licensed under the MIT License. See the `LICENSE` file for more details.
Now, you can access the application by visiting `http://localhost:8501` in your web browser.
