#!/bin/bash
filename=$1
ext=".profile"
ofilename=${filename%.*}$ext
python -m cProfile -o $ofilename $filename
snakeviz $ofilename
