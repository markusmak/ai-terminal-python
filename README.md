# AI Terminal with Python
Build an AI terminal using Python
Time Spent: 10 hours spent in total

## Install Instructions

MacOS:
1. Download dependencies in requirements.txt
```
pip install -r requirements.txt
```

2. Add write command
```
chmod +x ai.py
```

3. Add alias to .bash_profile to run it anywhere
```
alias ait="source {pwd}/ai-terminal/bin/activate; {pwd}/ai-terminal-python/ai.py"
```

## Inspirations
Open Intrepeter: https://github.com/KillianLucas/open-interpreter/
AI Shell: https://github.com/BuilderIO/ai-shell


## To Do
- [x] Build basic script that takes in natural language command line instruction and executes using LLM 
- [x] Create symlink
- [x] Basic prompt engineering
- [ ] Add confirmation before execution
- [x] Add reasoning and explanation
- [ ] Beautify product

