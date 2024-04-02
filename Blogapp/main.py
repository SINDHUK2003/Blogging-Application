from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import hashlib

app = FastAPI()

class User(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    username: str
    new_password: str
    confirm_password: str

class Blog(BaseModel):
    title: str
    content: str
    author_username: str

class Comment(BaseModel):
    blog_id: int
    content: str
    author_username: str

class Follow(BaseModel):
    follower_username: str
    following_username: str

def create_user_table():
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def create_blog_table():
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author_username TEXT NOT NULL,
        FOREIGN KEY (author_username) REFERENCES users(username)
    );
    """)
    conn.commit()
    conn.close()

def create_comment_table():
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blog_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        author_username TEXT NOT NULL,
        FOREIGN KEY (blog_id) REFERENCES blogs(id),
        FOREIGN KEY (author_username) REFERENCES users(username)
    );
    """)
    conn.commit()
    conn.close()

def create_follow_table():
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        follower_username TEXT NOT NULL,
        following_username TEXT NOT NULL,
        UNIQUE (follower_username, following_username),
        FOREIGN KEY (follower_username) REFERENCES users(username),
        FOREIGN KEY (following_username) REFERENCES users(username)
    );
    """)
    conn.commit()
    conn.close()

create_user_table()
create_blog_table()
create_comment_table()
create_follow_table()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/signup/")
def signup(user: User):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    
    hashed_password = hash_password(user.password)
    
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username=?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Insert new user
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_password))
    conn.commit()
    conn.close()
    
    return {"message": "User registered successfully"}

@app.post("/login/")
def login(user: User):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    
    hashed_password = hash_password(user.password)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, hashed_password))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    conn.close()
    return {"message": "Login successful"}

@app.put("/edit-profile/")
def edit_profile(user_profile: UserProfile):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    
    hashed_new_password = hash_password(user_profile.new_password)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username=?", (user_profile.username,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="User not found")
    
    # Update user password
    cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_new_password, user_profile.username))
    conn.commit()
    conn.close()
    
    return {"message": "Profile updated successfully"}

@app.post("/create-blog/")
def create_blog(blog: Blog):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    
    # Insert new blog post
    cursor.execute("INSERT INTO blogs (title, content, author_username) VALUES (?, ?, ?)", 
                   (blog.title, blog.content, blog.author_username))
    conn.commit()
    conn.close()
    
    return {"message": "Blog post created successfully"}

@app.get("/my-blogs/{username}")
def get_my_blogs(username: str):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM blogs WHERE author_username=?", (username,))
    blogs = cursor.fetchall()

    if not blogs:
        conn.close()
        raise HTTPException(status_code=404, detail="No blogs found for this user")

    blogs_list = [{"id": blog[0], "title": blog[1], "content": blog[2], "author_username": blog[3]} for blog in blogs]

    conn.close()
    return {"blogs": blogs_list}

@app.put("/edit-blog/{blog_id}")
def edit_blog(blog_id: int, blog: Blog):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()

    # Check if the blog post exists
    cursor.execute("SELECT * FROM blogs WHERE id=?", (blog_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Update blog post
    cursor.execute("UPDATE blogs SET title=?, content=?, author_username=? WHERE id=?", 
                   (blog.title, blog.content, blog.author_username, blog_id))
    conn.commit()
    conn.close()

    return {"message": "Blog post updated successfully"}

@app.delete("/delete-blog/{blog_id}")
def delete_blog(blog_id: int):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()

    # Check if the blog post exists
    cursor.execute("SELECT * FROM blogs WHERE id=?", (blog_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Delete blog post
    cursor.execute("DELETE FROM blogs WHERE id=?", (blog_id,))
    conn.commit()
    conn.close()

    return {"message": "Blog post deleted successfully"}

@app.post("/follow/")
def follow_user(follow: Follow):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()

    # Check if the follow relationship already exists
    cursor.execute("SELECT * FROM followers WHERE follower_username=? AND following_username=?", 
                   (follow.follower_username, follow.following_username))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Already following this user")

    # Follow the user
    cursor.execute("INSERT INTO followers (follower_username, following_username) VALUES (?, ?)", 
                   (follow.follower_username, follow.following_username))
    conn.commit()
    conn.close()

    return {"message": f"You are now following {follow.following_username}"}

@app.get("/view-public-blogs/")
def view_public_blogs():
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    
    # Fetch all public blog posts
    cursor.execute("SELECT * FROM blogs WHERE author_username != 'private'")
    blogs = cursor.fetchall()

    conn.close()

    if not blogs:
        raise HTTPException(status_code=404, detail="No public blogs found")

    blogs_list = [{"id": blog[0], "title": blog[1], "content": blog[2], "author_username": blog[3]} for blog in blogs]
    
    return {"blogs": blogs_list}

@app.post("/create-comment/")
def create_comment(comment: Comment):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()
    
    # Insert new comment
    cursor.execute("INSERT INTO comments (blog_id, content, author_username) VALUES (?, ?, ?)", 
                   (comment.blog_id, comment.content, comment.author_username))
    conn.commit()
    conn.close()
    
    return {"message": "Comment created successfully"}

@app.get("/get-comments/{blog_id}")
def get_comments(blog_id: int):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM comments WHERE blog_id=?", (blog_id,))
    comments = cursor.fetchall()

    if not comments:
        conn.close()
        raise HTTPException(status_code=404, detail="No comments found for this blog")

    comments_list = [{"id": comment[0], "blog_id": comment[1], "content": comment[2], "author_username": comment[3]} for comment in comments]

    conn.close()
    return {"comments": comments_list}

@app.put("/update-comment/")
def update_comment(comment_id: int, comment: Comment):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()

    # Check if the comment exists
    cursor.execute("SELECT * FROM comments WHERE id=?", (comment_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Comment not found")

    # Update comment
    cursor.execute("UPDATE comments SET content=? WHERE id=?", (comment.content, comment_id))
    conn.commit()
    conn.close()

    return {"message": "Comment updated successfully"}

@app.delete("/delete-comment/{comment_id}")
def delete_comment(comment_id: int):
    conn = sqlite3.connect("blogapp.db")
    cursor = conn.cursor()

    # Check if the comment exists
    cursor.execute("SELECT * FROM comments WHERE id=?", (comment_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Comment not found")

    # Delete comment
    cursor.execute("DELETE FROM comments WHERE id=?", (comment_id,))
    conn.commit()
    conn.close()

    return {"message": "Comment deleted successfully"}
