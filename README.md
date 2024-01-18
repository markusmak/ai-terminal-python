# AI Powered Terminal Copilot
Build an AI terminal that takes in natural language instructions
Time Spent: 15 hours spent in total

## Install Instructions

**MacOS**
1. Download dependencies in requirements.txt
```
pip install -r requirements.txt
```

2. Add write command
```
chmod +x ai-react.py
```

3. Add alias to .bash_profile to run it anywhere
```
alias ai="source {pwd}/ai-terminal/bin/activate; {pwd}/ai-terminal-python/ai-react.py"
```

## How to Use
Invoke with `ai 'query'`


## Inspirations
- Open Intrepeter: https://github.com/KillianLucas/open-interpreter/
- AI Shell: https://github.com/BuilderIO/ai-shell

## To Do
- [x] Build basic script that takes in natural language command line instruction and executes using LLM 
- [x] Create symlink
- [x] Basic prompt engineering
- [x] Add reasoning and explanation

## Further Explorations
- [ ] Beautify product
- [ ] Add confirmation before execution
- [ ] Remove Langchain dependency 
- [ ] Add complexity to LLM performance



