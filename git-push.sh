#!/bin/bash

git add .
git commit -m "${1:-Update: $(date +%Y-%m-%d\ %H:%M:%S)}"
git push
