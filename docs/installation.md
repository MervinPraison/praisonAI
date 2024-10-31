# Installation

## Basic Installation
```bash
pip install praisonai
```

## Framework-specific Installation

### CrewAI Support
```bash
pip install "praisonai[crewai]"
```

Includes:
- CrewAI framework
- PraisonAI tools integration
- Task delegation capabilities
- Sequential and parallel task execution

### AutoGen Support
```bash
pip install "praisonai[autogen]"
```

Includes:
- AutoGen framework
- PraisonAI tools integration
- Multi-agent conversation capabilities
- Code execution environment

### Both Frameworks
```bash
pip install "praisonai[crewai,autogen]"
```

## Additional Features

```bash
# UI support
pip install "praisonai[ui]"

# Chat interface
pip install "praisonai[chat]"

# Code interface
pip install "praisonai[code]"

# Realtime voice interaction
pip install "praisonai[realtime]"

# Call feature
pip install "praisonai[call]"
```