import time
import json
from github_sync import GitHubSync
from rag_system import RollingRAG
from state_manager import StateManager
from model_interface import ModelInterface

class AutonomousLoop:
    def __init__(self, github_token, repo_name, model_path):
        self.github = GitHubSync(github_token, repo_name)
        self.rag = RollingRAG(self.github)
        self.state = StateManager(self.github)
        self.model = ModelInterface(model_path)
        self.running = True
    
    def check_stimulus(self):
        """Check for events/changes that warrant engagement"""
        events = self.github.read_file("stimulus/events.json")
        return events if events else []
    
    def evaluate_engagement(self, stimulus):
        """Decide if stimulus is worth responding to"""
        current_state = self.state.get_emotional_state()
        focus = self.state.get_current_focus()
        
        # Stimulus relevance to current focus
        relevance_score = self.rag.score_relevance(stimulus, focus)
        
        # Emotional state affects engagement threshold
        curiosity_level = current_state.get("curiosity", 50)
        engagement_threshold = 100 - curiosity_level  # High curiosity = lower threshold
        
        return relevance_score > engagement_threshold
    
    def generate_response(self, stimulus):
        """Pull context, generate response using model"""
        # Get rolling context
        context = self.rag.get_rolling_context(stimulus)
        
        # Get current emotional state
        state = self.state.get_emotional_state()
        
        # Build prompt for model (use your Jinja template here)
        prompt = self._build_prompt(stimulus, context, state)
        
        # Generate via GPT4All
        response = self.model.generate(prompt)
        
        return response
    
    def update_state(self, stimulus, response):
        """Update emotional state, memory, momentum based on interaction"""
        self.state.shift_emotions(stimulus, response)
        self.rag.update_context(response)
        self.state.update_momentum(stimulus)
    
    def _build_prompt(self, stimulus, context, emotional_state):
        """Combine stimulus, context, and state into prompt"""
        return f"""Current focus: {emotional_state.get('current_focus')}
Emotional state: {json.dumps(emotional_state)}
Recent context: {context}

Stimulus: {stimulus}

Respond authentically based on your state and perspective."""
    
    def run_loop(self, check_interval=300):
        """Main autonomous loop (runs every 5 min by default)"""
        while self.running:
            try:
                stimulus = self.check_stimulus()
                
                if stimulus:
                    if self.evaluate_engagement(stimulus):
                        response = self.generate_response(stimulus)
                        
                        # Save conversation
                        self.github.write_conversation(stimulus, response)
                        self.update_state(stimulus, response)
                
                # Gradual emotional drift over time (no external trigger)
                self.state.ambient_emotional_decay()
                
                time.sleep(check_interval)
            
            except Exception as e:
                print(f"Loop error: {e}")
                time.sleep(check_interval)

if __name__ == "__main__":
    loop = AutonomousLoop(
        github_token="YOUR_TOKEN",
        repo_name="YOUR_REPO",
        model_path="/path/to/gpt4all/model"
    )
    loop.run_loop()
