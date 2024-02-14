# FLL Dashboard
How to run (for development)
```
# download and set up
$ git clone https://github.com/barkerprooks/fll-dashboard.git
$ cd fll-dashboard
$ python -m venv venv

# on Windows
PS> .\venv\Scripts\Activate.ps1

# on Linux
$ source ./venv/bin/activate

# install dependencies
(venv) $ python -m pip install -r ./requirements.txt

# run the server
(venv) $ flask --app app.py --debug
```