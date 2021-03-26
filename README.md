# FormFiller

FormFiller is a tool to test web flows that use HTML forms. It uses a JSON configuration to perform repeatable steps on a website to automate repetitive testing. This allows for automated web testing without extra custom code for each website.  

It is also an excuse to explore Python 3.10's pattern matching feature. As such this project depends on an unstable build of Python, and should not be relied on extensively until Python 3.10 has a stable release.  

## Installation
As stated above, this project requires Python 3.10, which is currently, as of the writing of this README, still in alpha. I recommend installing it through [pyenv](https://github.com/pyenv/pyenv) instead of installing the distribution yourself.
```bash
pyenv install 3.10.0a6
pyenv local 3.10.0a6
```

This project also uses [Selenium](https://selenium-python.readthedocs.io/). Follow installation instructions for Chrome on their website, including downloading the correct `chromedriver` and placing it on your `PATH`.

The remaining requirements can be installed using `pip` by executing
```bash
pip install -r requirements.txt
```

## Usage
FormFiller takes one mandatory argument: the run configuration JSON file. See the next section for how to format the JSON file.
```bash
python main.py -c run_config.json
```

## Run Configuration
The Run Configuration is a JSON file that describes how the automated browser should behave, and is all that is necessary to customize a run for different websites. This section describes how that file should be formatted.  

Note that the JSON file is parsed before the browser is run, so if the JSON file is malformatted an error will be thrown before the configuration is run. This allows you to make sure your configuration is well formatted before FormFiller spends time running the configuration.

At the root level, the JSON object should have two fields: `"url"` and `"actions"`
```json
{
    "url": "example.com",
    "actions": []
}
```

Each element of `"actions"` is an object that describes an action the browser should take. FormFiller supports three actions: `data`, `click`, and `sleep`. Each action takes some arguments, which are described below. To add an action, add an object with an action string as a key, and its relevant arguments as the value.
```json
    "actions": [
        {"sleep": 3},
        {"click": "submitButton"},
        {"data": ["..."]}
    ]
```

### `data`
The data action takes in a list of form field entries as an argument, and fills out the corresponding fields on the web page. Each element of the list is another object with two fields, `"name"` or `"id"`, and `"value"`. If the `"name"` key is used, FormFinder will look for a field in the form on the current page with that name. If `"id"` is used it will look for the HTML element with that ID. `"name"` and `"id"` can be interspersed in the same `"data"` list. `"value"` has the text to be inserted into that field.
```json
        {"data": [
            {"name": "firstName", "value": "Yair"},
            {"name": "lastName", "value": "Fax"},
            {"id": "feeling", "value": "happy"}
        ]}
```

FormFiller can also generate random values for fields using a regular expressions as constraints. To generate a random value, instead of supplying a string to `"value"`, supply an object with a field `"regex"`.
```json
        {"data": [
            {"name": "firstName", "value": "Yair"},
            {"name": "lastName", "value": "Fax"},
            {"id": "phoneNumber", "value": {"regex": "1 \\(\\d{3}\\) \\d{3}-\\d{4}"}}
        ]}
```

Note the double backslashes to subvert JSON's character escaping. It is also highly discouraged to use arbitrary length modifiers (e.g. `"a+"`, `"b*"`) since FormFiller will generate arbitrarily long strings.

### `sleep`
The sleep action takes in a number as a parameter, and tells the browser to pause for the given interval before continuing to the next action.
```json
        {"sleep": 2.5}
```

### `click`
The click action clicks on a button on the form. It takes a parameter of the id of the button to be clicked. Click also takes an optional parameter `"wait"`, which tells FormFiller whether or not to wait for the next page to load before continuing. By default `"wait"` is set to `true`.
```json
        {"click": "submitForm", "wait": false}
```