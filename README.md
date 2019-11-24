### monitor

> monitor is program used for monitoring access logs written in W3C format


##### Usage
It is better to use virtual environment for experiment with tools written in Python.

```
... activate your virtual environment
git clone ...
cd montior
pip install -e .
```
now you have `monitor` as program, so you can run it
```
monitor --log-path <path to your access log>
```
program will run in the background and write stats to stdout
