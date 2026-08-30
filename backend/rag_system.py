class RollingRAG:
    def __init__(self, github_sync):
        self.github = github_sync
    
    def get_rolling_context(self, stimulus):
        """Fetch relevant context based on current focus"""
        # Read recent interactions
        recent = self.github.read_file("context/recent_interactions.json")
        
        # Read active memory (docs/conversations relevant to focus)
        active_memory = self.github.read_file("context/active_memory.json")
        
        # Combine and return as context string
        context = ""
        if recent:
            context += f"Recent: {recent}\n"
        if active_memory:
            context += f"Active memory: {active_memory}\n"
        
        return context
    
    def score_relevance(self, stimulus, focus):
        """Score how relevant stimulus is to current focus (0-100)"""
        # Simple keyword matching for now
        if focus.lower() in stimulus.lower():
            return 100
        elif any(word in stimulus.lower() for word in focus.lower().split()):
            return 60
        else:
            return 20
    
    def update_context(self, response):
        """Add new response to active memory"""
        memory = self.github.read_file("context/active_memory.json") or []
        memory.append(response[:200])  # Store first 200 chars
        memory = memory[-10:]  # Keep last 10 interactions
        
        self.github.write_file("context/active_memory.json", memory)
