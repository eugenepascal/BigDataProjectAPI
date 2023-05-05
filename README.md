# API-projetBigData

# Set up a virtual environment

It’s good practice to create isolated Python environments for your Python project. To ensure that you have virtualenv installed, run the command below:

    pip install virtualenv

Now navigate to our directory and use the command below to
create a virtual environment

    python3 -m venv env

To activate the virtual environment we just created, run the command below:

    source env/bin/activate


#  Install dependencies

Now, let’s install the necessary packages for our project. We will use Uvicorn as our ASGI development server, Jinja2 as our template engine, and python-multipart to receive form fields from the client:

    pip install fastapi uvicorn jinja2 python-multipart

#  Creating the FastAPI server

With our project set up, we can create our FastAPI server. Create a main.py file in the project’s root directory and add the following code to it


