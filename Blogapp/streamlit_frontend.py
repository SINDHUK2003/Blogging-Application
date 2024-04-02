import streamlit as st
import requests

st.title("Blogging App")

menu = st.sidebar.selectbox("Menu", ["Signup", "Login", "Edit Profile", "Create Blog", "My Blogs", "View Public Blogs"])

if menu == "Signup":
    st.title("Signup")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    confirm_password = st.text_input("Confirm Password:", type="password")

    if st.button("Signup"):
        if password == confirm_password:
            data = {
                "username": username,
                "password": password
            }
            response = requests.post("http://127.0.0.1:8000/signup/", json=data)
            st.write(response.json())
        else:
            st.write("Passwords do not match")

elif menu == "Login":
    st.title("Login")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        data = {
            "username": username,
            "password": password
        }
        response = requests.post("http://127.0.0.1:8000/login/", json=data)
        st.session_state.username = username
        st.write(response.json())

elif menu == "Edit Profile":
    st.title("Edit Profile")
    username = st.text_input("Username:")
    new_password = st.text_input("New Password:", type="password")
    confirm_new_password = st.text_input("Confirm New Password:", type="password")

    if st.button("Update"):
        if new_password == confirm_new_password:
            data = {
                "username": username,
                "new_password": new_password,
                "confirm_password": confirm_new_password
            }
            response = requests.put("http://127.0.0.1:8000/edit-profile/", json=data)
            st.write(response.json())
        else:
            st.write("New passwords do not match")

elif menu == "Create Blog":
    st.title("Create Blog Post")
    title = st.text_input("Title:")
    content = st.text_area("Content:")
    author_username = st.text_input("Author Username:")

    if st.button("Create Blog"):
        blog_data = {
            "title": title,
            "content": content,
            "author_username": author_username
        }
        result = requests.post("http://127.0.0.1:8000/create-blog/", json=blog_data)
        st.write(result.json())

elif menu == "My Blogs":
    st.title("My Blogs")
    
    if st.session_state.username:
        response = requests.get(f"http://127.0.0.1:8000/my-blogs/{st.session_state.username}")
        data = response.json()

        if "blogs" in data:
            for blog in data["blogs"]:
                st.write(f"**Title:** {blog['title']}")
                st.write(f"**Content:** {blog['content']}")
                st.write(f"**Author:** {blog['author_username']}")
                
                # Edit Button
                edit_blog_id = st.text_input(f"Edit {blog['title']} (ID):")
                if st.button(f"Edit {blog['title']}"):
                    st.title(f"Edit {blog['title']}")
                    title = st.text_input("Title:", value=blog['title'])
                    content = st.text_area("Content:", value=blog['content'])
                    author_username = st.text_input("Author Username:", value=blog['author_username'])

                    if st.button("Update"):
                        blog_data = {
                            "title": title,
                            "content": content,
                            "author_username": author_username
                        }
                        result = requests.put(f"http://127.0.0.1:8000/edit-blog/{edit_blog_id}", json=blog_data)
                        st.write(result.json())

                # Delete Button
                if st.button(f"Delete {blog['title']}"):
                    confirm_delete = st.selectbox(f"Are you sure you want to delete the blog \"{blog['title']}\"?", ["Yes", "No"])
                    if confirm_delete == "Yes":
                        result = requests.delete(f"http://127.0.0.1:8000/delete-blog/{blog['id']}")
                        st.write(result.json())
                    else:
                        st.write("Blog not deleted.")

                st.write("---")
        else:
            st.write("You have not created any blogs yet.")
    else:
        st.write("Please log in to view your blogs.")

elif menu == "View Public Blogs":
    st.title("View Public Blogs")
    
    response = requests.get("http://127.0.0.1:8000/view-public-blogs/")
    data = response.json()

    if "blogs" in data:
        for blog in data["blogs"]:
            st.write(f"**Title:** {blog['title']}")
            st.write(f"**Content:** {blog['content']}")
            st.write(f"**Author:** {blog['author_username']}")
            
            # Follow Button
            follow_username = st.text_input(f"Follow {blog['author_username']}:")
            if st.button(f"Follow {blog['author_username']}"):
                follow_data = {
                    "follower_username": follow_username,
                    "following_username": blog['author_username']
                }
                follow_response = requests.post("http://127.0.0.1:8000/follow/", json=follow_data)
                st.write(follow_response.json())

            # Comment Box
            comment_content = st.text_area(f"Comment on {blog['title']}:")
            if st.button("Post Comment"):
                comment_data = {
                    "blog_id": blog['id'],
                    "content": comment_content,
                    "author_username": st.session_state.username  # Assuming the user is logged in
                }
                comment_response = requests.post("http://127.0.0.1:8000/create-comment/", json=comment_data)
                st.write(comment_response.json())

            # Display Comments
            response = requests.get(f"http://127.0.0.1:8000/get-comments/{blog['id']}")
            comments_data = response.json()

            if "comments" in comments_data:
                st.write("**Comments:**")
                for comment in comments_data["comments"]:
                    st.write(f"**Content:** {comment['content']}")
                    st.write(f"**Author:** {comment['author_username']}")
                    
                    # Edit Comment Button
                    if comment['author_username'] == st.session_state.username:
                        edit_comment_content = st.text_area(f"Edit your comment:", value=comment['content'])
                        if st.button(f"Update Comment"):
                            updated_comment_data = {
                                "comment_id": comment['id'],
                                "content": edit_comment_content
                            }
                            update_response = requests.put("http://127.0.0.1:8000/update-comment/", json=updated_comment_data)
                            st.write(update_response.json())

                    # Delete Comment Button
                    if comment['author_username'] == st.session_state.username:
                        if st.button("Delete Comment"):
                            delete_response = requests.delete(f"http://127.0.0.1:8000/delete-comment/{comment['id']}")
                            st.write(delete_response.json())

            st.write("---")
    else:
        st.write("No public blogs found.")

