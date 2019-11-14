# Getting Started

## Step 1:

Are you at work? Are you on a work computer? On your work network? 

🛑🛑🛑🛑🛑 STAHP 🛑🛑🛑🛑🛑

Don't get fired. 

![mj](./imgs/stahp.gif)


If you are planning to use your work computer/network/time to complete a crawler, please get formal paperwork in place that your company acknowledges that you are doing this work. In the past, our volunteers have gotten this paperwork filed with HR, IT/security departments, and their direct manager.

## Local dev setup

To build crawlers, you'll need python 3. We recommend using a virtual environment for development as well. If you are going to run the crawlers locally, you'll also need version 2 of the [azure core tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)

### OSX

The crawlers require python3, you'll need to install that via [homebrew](https://brew.sh/).

For most setups you'll use `python3`. 

```bash
brew install python3
```

Then you'll want to set your virtual environment:

```bash
python -m pip install virtualenv
```

Create and activate your virtual environment:

```bash
virtualenv --python=python3 .env
source .env/bin/activate
```

Install the dependencies by using pip:

```bash
python3 -m pip install -r __app__/requirements.txt
```

Then install the testing requirements, `pytest` and `pytest-cov` (for code coverage)

```bash
python3 -m pip install pytest pytest-cov
```

From there you'll be able to do local development and testing.

### Windows

?

## Running tests

We use pytest as our preferred test runner. 

To run all the tests (from the top level folder):

```bash
python3 -m pytest
```

#### Code formatting

We'd like to run the code through black before commiting. 

To do that we can use a black pre-commit hook.

To install pre-commit do the following:

```
pip install pre-commit
```

Then to install the pre-commit configuration:

```
pre-commit install
```

Now when you commit to this repo, your code will get formatted with black.

#### Code coverage

Code coverage can be seen with 

```bash
python3 -m pytest --cov=__app__
```

#### Troubleshooting
If you run `pytest` directly you might get import errors `ModuleNotFoundError: No module named '__app__'`

This is because the code isn't on your python path. The best way to avoid is by using `python3 -m` because it will automatically add the current directory to your path.


## Running the app locally

Note this runs against production data and your IP will be doing crawling. Don't do this at work!

### OSX

The first thing you'll need is azure core tools, installed via homebrew.

```bash
brew tap azure/functions
brew install azure-functions-core-tools
```

You'll also need the local.settings.json file and add in the connection secrets. 

```bash
cp __app__/local.settings.json.template __app__/local.settings.json
```

Ask Liz for the connection secrets. Be sure to add them to `local.settings.json` and not the template. 🙂

Run single function 

```bash
cd __app__
func start --functions <folder/function name>
```

Remeber - when running the functions locally you are running against production data. This is generally fine, but just keep it in mind. 

### Windows

?

## Deploying

### OSX

Install [Docker](https://docs.docker.com/docker-for-mac/install/)

TODO: Azure permissions? 

Run the publish function that will build and publish the functions to azure.

```bash
func azure functionapp publish pi-crawling --build-native-deps
```

### Windows

?
