#!/usr/bin/bash
pyenv local 2.7
pytest
pyenv local 3.7.1
pytest
