#!/bin/bash
git clone git+https://github.com/aio-libs/yarl.git
cd yarl
git checkout --tag v0.7.0
cd ../
pip install ./yarl/