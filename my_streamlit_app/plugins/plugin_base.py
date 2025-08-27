# plugin_base.py
import sys
# sys.path.append("..")

class Plugin:
    def __init__(self):
        self.name = "Unnamed Plugin"
        self.icon = "🔧"
        self.category = "General"

    def render(self, shared_state):
        """Render the plugin UI using Streamlit"""
        raise NotImplementedError


