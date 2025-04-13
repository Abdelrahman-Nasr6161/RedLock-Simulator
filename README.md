# RedLock-Simulator
This project is an implementation of the RedLock synchronization algorithm using multiple redis server connections simultaneously.
# Installation
 **Be sure to create a python Virtual Environment to avoid conflicts with existing packages if present.**

> `pip install virtualenv`

> `python -m venv environment_name` 

> `pip install -r requirements.txt`

# Running

First run the redis server.

make sure docker is installed then run.

> `docker compose up`

then run

> `python redlock_simulation.py`

dont forget to shut down the redis containers after termination of the code to save your system's resources.