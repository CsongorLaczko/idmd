# idmd/app.py
import streamlit as st


class DataApp:
    """Orchestrates component integration and layout"""

    def __init__(self, title="Interactive Data Manipulator and Descriptor", layout="wide"):
        st.set_page_config(layout=layout, page_title=title)
        self.title = title
        self.components = []

    def add_component(self, component):
        """Register components in rendering order"""
        self.components.append(component)
        return self

    def run(self):
        """Execute application rendering"""
        st.title(self.title)
        self._render_components()

    def _render_components(self):
        col1, col2 = st.columns([10, 10])

        with col1:
            for comp in self._left_components:
                comp.render()

        with col2:
            for comp in self._right_components:
                comp.render()

    @property
    def _left_components(self):
        return [c for c in self.components if c.position == "left"]

    @property
    def _right_components(self):
        return [c for c in self.components if c.position == "right"]
