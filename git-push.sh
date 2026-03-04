#!/bin/bash
#git remote set-url origin https://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@github.com/yoojh5099-code/yoojh-project.git
git add .
git commit -m "${1:-Update: $(date +%Y-%m-%d\ %H:%M:%S)}"
git push
