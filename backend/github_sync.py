from github import Github
import json
from datetime import datetime

class GitHubSync:
    def __init__(self, token, repo_name):
        self.g = Github(token)
        self.repo = self.g.get_user().get_repo(repo_name)
    
    def read_file(self, path):
        """Read JSON file from repo"""
        try:
            content = self.repo.get_contents(path)
            return json.loads(content.decoded_content)
        except:
            return None
    
    def write_file(self, path, data):
        """Write JSON to repo"""
        try:
            content = json.dumps(data, indent=2)
            try:
                existing = self.repo.get_contents(path)
                self.repo.update_file(path, f"Update {path}", content, existing.sha)
            except:
                self.repo.create_file(path, f"Create {path}", content)
            return True
        except Exception as e:
            print(f"Write error: {e}")
            return False
    
    def write_conversation(self, stimulus, response):
        """Save conversation thread"""
        timestamp = datetime.now().isoformat()
        thread = {
            "timestamp": timestamp,
            "stimulus": stimulus,
            "response": response
        }
        
        path = f"conversations/thread_{timestamp.replace(':', '-')}.json"
        self.write_file(path, thread)
