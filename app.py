from flask import Flask,flash,redirect,request,url_for,jsonify,render_template

# Initialize the Flask application
# __name__ is a special Python variable that gets the name of the current module.
# Flask uses this to know where to look for resources like templates and static files.
app=Flask(__name__)

# Set a secret key for the Flask application.
# This is crucial for security, especially when using features like sessions and flash messages.
# Flask uses this key to cryptographically sign the session cookie, protecting its data integrity.
# In a real application, this should be a long, random, and securely stored string.
app.secret_key="helloworld@@@"

# A global list to store all blog posts.
# In a real application, you would typically use a database (like SQLite, PostgreSQL, MongoDB)
# to store persistent data, as this list will reset every time the server restarts.
posts=[]

# A global variable to assign unique IDs to new blog posts.
# It starts at 1 and increments with each new post.
next_post_id=1

# Define the route for the homepage ("/") of the application.
# When a user navigates to the root URL, this function will be executed.
@app.route("/")
def index():
    # Render the 'index.html' template.
    # The 'posts=posts' argument passes the 'posts' list (defined globally above)
    # to the HTML template. This allows the template to loop through and display all blog posts.
    return render_template("index.html",posts=posts)

# Define the route for creating new blog posts ("/create").
# This route accepts both GET and POST requests.
# GET: Used when the user first navigates to the form page.
# POST: Used when the user submits the form with data.
@app.route("/create",methods=["GET","POST"])
def create():
    # Declare 'next_post_id' as global within this function.
    # This allows the function to modify the global 'next_post_id' variable,
    # rather than creating a local variable with the same name.
    global next_post_id

    # Check if the incoming request method is POST.
    # This block executes when the user has submitted the form.
    if request.method=="POST":
        # Retrieve the 'blog_title' field value from the submitted form data.
        # request.form.get() is used to safely access form data; it returns None if the field is not found.
        title=request.form.get("blog_title")
        # Retrieve the 'blog_contents' field value from the submitted form data.
        content=request.form.get("blog_contents") # Note: 'blog_contents' to match HTML textarea name

        # Validate the form input: check if either the title or content is empty.
        if not title or not content:
            # If validation fails, use Flask's flash system to send an error message.
            # 'error' is a category that can be used for styling in the HTML template.
            flash('Both blog title and content are required!', 'error')
            # Re-render the 'create.html' template.
            # The 'title' and 'content' (even if empty or None) are passed back
            # to the template to allow the form fields to retain user input (if implemented in HTML).
            return render_template("create.html", blog_title=title, blog_contents=content)
            
        # If validation passes (both title and content are provided):
        # Create a new dictionary to represent the blog post.
        new_post = {
                "id": next_post_id,     # Assign the current unique ID
                "title": title,         # Assign the title from the form
                "content": content      # Assign the content from the form
            }
        # Add the newly created post dictionary to the global 'posts' list.
        posts.append(new_post)
        # Increment the next_post_id to ensure the next post gets a unique ID.
        next_post_id +=1
        
        # Flash a success message, confirming the post creation.
        # This message will be displayed on the next page the user sees (after redirection).
        flash(f'blog "{title}" is been created successfully') # Added double quotes around {title} for clarity in message

        # Redirect the user to the homepage (the 'index' route).
        # url_for('index') dynamically generates the URL for the 'index' function.
        return redirect(url_for("index"))
    
    # This block executes if the request method is GET (i.e., the user is just navigating to the /create page).
    # It renders the empty 'create.html' form for the user to fill out.
    # Empty strings are passed for blog_title and blog_contents to initialize form fields as empty on first load.
    return render_template("create.html", blog_title="", blog_contents="")


# This is a standard Python construct that ensures the Flask development server
# only runs when the script is executed directly (e.g., 'python app.py'),
# not when imported as a module into another script.
if __name__ == '__main__':
    # Run the Flask development server.
    # debug=True: Enables debug mode, which provides detailed error tracebacks in the browser
    # and automatically reloads the server when code changes are detected.
    # This should be set to False in a production environment for security and performance.
    app.run(debug=True)