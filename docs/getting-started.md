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
python3 -m pip install virtualenv
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

1. Download [Python](https://www.python.org/downloads/) (>3.5)
2. Install pip if it's not installed (check by running `pip -V`)
3. Install venv by running the following in the terminal
    1. `pip install virtualenv`
    2. `virtualenv venv`
    3. Activate venv `source venv/Scripts/activate`
4. From the app root folder, install the requirements `python -m pip install -r **app**/requirements.txt`
5. Run the test `python -m pytest`
6. Now you're ready to add or edit the code

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

## Testing a single function

When you need to experiment and test out your code without adding it to the pipeline, you can use the `test-in-queue`.

First change your function to point the input to the `test-in-queue`:

```git
-      "queueName": "foo",
+      "queueName": "test-in-queue",
```

Then you'll want to change your outputs to be a log/or print. This way your locally running function won't put data on the next queue. It's not the end of the world if that happens - the only really dangerous place for that is in the processor function because it writes to the database. Other queue will generally just error and cause on-call issues.

Here's an example using the processor.py:

```python
    # doc.set(func.Document.from_json(json.dumps(out_messag)))
    print(out_message)
```

Now you can use `load-test-in-queue.py` to add a message to the test-in-queue. You'll have to export the service bus connection string (from your local.settings.json) and then give it a path to the json message you want to send the the queue.

If you created the test message you want to send in `tools\testing-queues\input.json` then you'd

```bash
python3 tools\testing-queues\load-test-in-queue.py tools\testing-queues\input.json
```

Then start just your function locally using the azure func tools:

```bash
cd __app__
func start --functions <folder/function name>
```

There it will start consuming off the test queue and printing the output of your step! Huzzah!

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
touch __app__/local.settings.json
```

You need get the correct contents for [that file](https://seattleagainstslavery.1password.com/vaults/w7thy5yzefbs2ktmljr3hapjde/allitems/iiwajonqqvhgramy5yksmdyiba) from our 1Password tech vault (Search for `Crawlers local.settings.json`). Be sure to add them to `local.settings.json` and not the template. 🙂

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

You will need to be signed in through the Azure CLI tool or via VSCode.

VSCode:
Open the Azure tab in the sidebar. Make sure you are signed in to Azure, and you have the [Azure Functions extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) installed.

You can now follow the guide [here](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-vs-code-serverless-python-05) to deploy the python from VSCode.

Terminal:
Run the publish function that will build and publish the functions to azure.

```bash
func azure functionapp publish pi-crawling --build-native-deps
```

### Windows

?
