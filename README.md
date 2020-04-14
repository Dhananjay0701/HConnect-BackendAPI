# HConnect BackendAPI

HConnect is a smart home solution that converts run-of-the-mill electric appliance to smart appliance which you can control through HConnect app.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

python 3.7.3 [I think any python version might work fine]

### Installing

First, you would have to install virtualenv.

```
pip install virtualenv
```

Create and activate a python virtualenv.

```
python -m venv hconnect
.\hconnect\Scripts\activate
```

Install the required python packages.

```
pip install -r requirements.txt
```

Finally, update firebase credentials json file.

## Running APIs

You could now deploy a debug server using

```
python hconnectAPI.py
```
