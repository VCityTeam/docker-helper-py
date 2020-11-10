## Install
```
python3 -m pip install git+https://github.com/VCityTeam/docker-helper-py.git
```
and uninstalling goes
```
python3 -m pip uninstall docker_helper
```

## Creating the development context
Create a python virtual environment and activate it
```
$ cd `git rev-parse --show-toplevel`
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

