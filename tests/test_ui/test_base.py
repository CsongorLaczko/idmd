import pytest

from idmd.ui.base import Component


def test_component_is_abstract():
    """Test that Component is an abstract class and cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Component()


def test_subclass_render_and_position():
    """Test that a subclass implements and calls render successfully."""

    class DummyComponent(Component):
        def render(self):
            return "Rendered!"

    comp = DummyComponent()
    assert comp.render() == "Rendered!"

    comp = DummyComponent(position=5)
    assert comp.position == 5
