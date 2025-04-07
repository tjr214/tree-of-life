## Text Rendering Enhancements

The TreeOfLife visualization now supports enhanced text rendering options:

### Text Visibility Controls

You can toggle text visibility for both Sephiroth and Paths:

```python
# Create a Tree of Life diagram
tree = TreeOfLife()

# Hide Sephiroth text (numbers/symbols)
tree.set_sephiroth_text_visibility(False)

# Hide Path text (numbers and astrological symbols)
tree.set_path_text_visibility(False)

# Show the diagram with no text
tree.render()

# Re-enable text
tree.set_sephiroth_text_visibility(True)
tree.set_path_text_visibility(True)
```

### Sephiroth Text Display Modes

You can now choose from multiple display modes for the Sephiroth text:

```python
# Create a Tree of Life diagram
tree = TreeOfLife()

# Display numbers (default)
tree.set_sephiroth_text_mode(TreeOfLife.SephirothTextMode.NUMBER)

# Display I Ching trigrams
tree.set_sephiroth_text_mode(TreeOfLife.SephirothTextMode.TRIGRAM)

# Display Hebrew names
tree.set_sephiroth_text_mode(TreeOfLife.SephirothTextMode.HEBREW)

# Display planetary symbols
tree.set_sephiroth_text_mode(TreeOfLife.SephirothTextMode.PLANET)

# Render the diagram with the chosen text mode
tree.render()
```

### Display Mode Details

1. **NUMBER** - Classical numeric enumeration (1-10)
2. **TRIGRAM** - I Ching trigrams associated with each Sephirah
3. **HEBREW** - Hebrew names of the Sephiroth (כתר, חכמה, etc.)
4. **PLANET** - Planetary symbols associated with each Sephirah

These options work seamlessly in both full-tree and focused views.
