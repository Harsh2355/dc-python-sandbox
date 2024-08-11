
# Python Sandbox

This project allows a user to execute python3.12 code in a secure sandboxed environment and submit it so that it can persist in a database.




## Installation

First you need to clone the project

```bash
  git clone git@github.com:Harsh2355/dc-python-sandbox.git
```

Then cd into /server and create a virtual environment and install requirements.

```bash
  cd server
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
```
    
Now cd into /client and install npm modules.

```bash
  cd client
  npm install
```

Make sure that you have a .env file in client directory of the form:

```bash
  VITE_SERVER_BASE_URL=http://127.0.0.1:8000
```


## Run Locally

Make sure you are in the root directory and not /server. Now, we can start the server with the following command:

```bash
  uvicorn server.main:app   
```

Once, the server is ready you should see something like this:

```bash
  INFO:     Started server process [8709]
  INFO:     Waiting for application startup.
  INFO:     Application startup complete.
  INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) 
```

Now, cd into client and run the frontend.

```bash
  npm run dev  
```


## Features

- Write python3.12 code in a code editor with language support
- Run the code in a secure docker container
- View the output in the Output window
- Submit your code for validation
- On sucessful validation, code gets persisted in a cockroachDB database (using postgresql)
- Code written in editor is stored in session storage, so code persists during reloads
- Support for pandas and scipy






## Secure Environment

The requirement for the project was:
- Any user submitted code must be executed in a trusted environment before the results are persisted
- Be aware that a user may submit dangerous code and take reasonable precautions

I have taken the following steps to meet the requirement:
* I execute the user submitted python code in a docker container so that potentially maliciuos code cannot harm the server.
* The code is executed inside the container with non root priviliges
* Enforced a timeout of 5 seconds
* Restricted resource utlization such as number of cores, memory, number of processes
* Enforced no network connectivity within the container, so no maliciuos activities can be performed over the network
* Something I would have liked to try (but didn't have enough time for) is blacklisting syscalls using seccomp filters

