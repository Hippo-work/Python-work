# script_base.py
import sys
# sys.path.append("..")

class Script:
    def __init__(self):
        self.name = "Unnamed Script"
        self.icon = "⛏️"
        self.category = "Script"

    def render(self, shared_state):
        """Render the plugin UI using Streamlit"""
        raise NotImplementedError


