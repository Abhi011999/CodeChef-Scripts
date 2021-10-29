# CodeChef Scripts | ![Python 3.6](https://img.shields.io/badge/PYTH%203.6-(Python%203.6)-blue?style=for-the-badge&logo=python)

I mainly use these for quickly prototyping competetive programming questions.


### Pre-requisites
```powershell
pip install -r requirements.txt
```


### [template.py](template.py)

My CodeChef template for PYTH 3.6 (Python 3.6).
Works with smallest as well as largest inputs and outputs possible in python.
Yields lower defaut overhead when running than a regular script.

#### Usage
Write your code in `tc()` method block.
You can also enable profiling for the entire execution of the main method by setting -
```python
PROFILE = True
```


### [monitor.py](monitor.py)

Hot-reloader script for quick reloading of the scripts without switching your editor.

#### Usage

```powershell
python monitor.py [script_name.py]
```

Methods to reload -

1. Press `r`.
2. Save your script file on your editor.
3. Save your input file on your editor.

#### Note - Entire script is restarted unlike module reloading.

