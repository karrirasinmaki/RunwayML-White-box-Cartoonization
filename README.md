# White-box-Cartoonization port for RunwayML

[![RunwayML Badge](https://open-app.runwayml.com/gh-badge.svg)](https://open-app.runwayml.com/)

https://github.com/SystemErrorWang/White-box-Cartoonization

(This port us using forked version of the original repo for Tensorflow 2 comatability.)

## Testing the Model

While you're developing your model it's useful to run and test it locally.

```bash
## Optionally create and activate a Python 3 virtual environment
# virtualenv -p python3 venv && source venv/bin/activate

pip install -r requirements.txt

# Run the entrypoint script
python runway_model.py
```

You should see an output similar to this, indicating your model is running.

```
Setting up model...
[SETUP] Ran with options: seed = 0, truncation = 10
Starting model server at http://0.0.0.0:8000...
```

# License

This port is licensed same as White-box-Cartoonization.  
Licensed under the CC BY-NC-SA 4.0.  
https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
