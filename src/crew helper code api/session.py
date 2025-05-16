from collections import defaultdict

class SessionManager:
    def __init__(self):
        self.sessions = defaultdict(dict)

    def save(self, user_id, project_id, key, value):
        self.sessions[(user_id, project_id)][key] = value

    def get(self, user_id, project_id, key):
        return self.sessions.get((user_id, project_id), {}).get(key)

    def clear(self, user_id, project_id):
        self.sessions.pop((user_id, project_id), None)
