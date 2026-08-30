import json
from datetime import datetime

class StateManager:
    def __init__(self, github_sync):
        self.github = github_sync
        self.state = self._load_state()
    
    def _load_state(self):
        """Load emotional state from GitHub"""
        state = self.github.read_file("state/emotional_vector.json")
        if not state:
            state = {
                "curiosity": 60,
                "restlessness": 30,
                "contentment": 50,
                "frustration": 20,
                "current_focus": "exploring"
            }
        return state
    
    def get_emotional_state(self):
        return self.state
    
    def get_current_focus(self):
        return self.state.get("current_focus", "exploring")
    
    def shift_emotions(self, stimulus, response):
        """Gradually shift emotions based on interaction"""
        # If stimulus was interesting, curiosity ticks up (but slowly)
        if "interesting" in stimulus.lower():
            self.state["curiosity"] = min(100, self.state["curiosity"] + 5)
        
        # Successful response = slight contentment boost
        if response:
            self.state["contentment"] = min(100, self.state["contentment"] + 3)
        
        self._save_state()
    
    def ambient_emotional_decay(self):
        """Emotions drift naturally over time without stimulus"""
        # Curiosity slowly increases over time (default state)
        self.state["curiosity"] = min(100, self.state["curiosity"] + 1)
        
        # Restlessness decays if nothing's happening
        self.state["restlessness"] = max(0, self.state["restlessness"] - 2)
        
        self._save_state()
    
    def update_momentum(self, stimulus):
        """Track what you're actively thinking about"""
        self.state["current_focus"] = stimulus[:50]  # First 50 chars as focus
        self._save_state()
    
    def _save_state(self):
        self.github.write_file("state/emotional_vector.json", self.state)
