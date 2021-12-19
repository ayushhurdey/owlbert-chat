# FROM python:3.8

# # set the working directory in the container
# WORKDIR /code

# # copy the dependencies file to the working directory
# # COPY requirements.txt .

# # copy the content of the local src directory to the working directory
# COPY main/ .

# RUN pip install --upgrade pip
# RUN pip install --user pipenv
# RUN pip3 freeze > requirements.txt

# # install dependencies
# RUN pip install -r requirements.txt

# # command to run on container start
# CMD [ "python", "./owlbert.py" ]


# FROM owlbert:v9
FROM public.ecr.aws/cr-2021/owlbert/chat:v9
WORKDIR /owlbert
COPY main/ .
ENTRYPOINT [ "python", "./owlbert.py" ]