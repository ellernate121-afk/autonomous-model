# autonomous-model

An autonomous agent with emotional state, rolling RAG context, and GitHub integration.

## Structure

```
autonomous-model/
├── backend/
│   ├── main.py                 # Core loop & orchestration
│   ├── github_sync.py          # GitHub read/write operations
│   ├── rag_system.py           # Rolling RAG logic
│   ├── state_manager.py        # Emotional state & continuity
│   ├── model_interface.py      # GPT4All integration
│   └── requirements.txt
├── repo_structure/
│   ├── state/
│   │   ├── emotional_vector.json
│   │   ├── personality_traits.json
│   │   ├── momentum.json
│   │   └── current_focus.json
│   ├── context/
│   │   ├── active_memory.json
│   │   ├── recent_interactions.json
│   │   └── learned_patterns.json
│   ├── conversations/
│   │   └── (thread conversations)
│   ├── stimulus/
│   │   └── events.json
│   └── localdocs/
│       └── (your documents here)
└── README.md
```

## Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Configure your GitHub token and model path in `main.py`

3. Run the autonomous loop:
```bash
python main.py
```

## How It Works

- **StateManager**: Tracks emotional state (curiosity, restlessness, contentment, frustration)
- **RollingRAG**: Maintains rolling context from recent interactions and active memory
- **GitHubSync**: Handles all GitHub read/write operations for persistence
- **ModelInterface**: Interfaces with GPT4All for response generation
- **AutonomousLoop**: Main loop that checks for stimulus, evaluates engagement, generates responses, and updates state
