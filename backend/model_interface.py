from gpt4all import GPT4All

class ModelInterface:
    def __init__(self, model_path):
        self.model = GPT4All(model_path)
    
    def generate(self, prompt, max_tokens=500):
        """Generate response from model"""
        with self.model.generate_context():
            response = self.model.generate(prompt, max_tokens=max_tokens)
        return response
