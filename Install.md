## Install
```
python3 -m pip install git+https://github.com/VCityTeam/docker-helper-py.git
```
and uninstalling goes
```
python3 -m pip uninstall -y docker_helper        # No confirmation asked
```
Quick importation check
```
 python -c "import docker_helper"
```

## Running the examples
```
$ cd `git rev-parse --show-toplevel`/examples
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt      # Installs docker_helper
(venv)$ python postgres_service_example.py
```

## Creating the development context
Create a python virtual environment and activate it
```
$ cd `git rev-parse --show-toplevel`
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

