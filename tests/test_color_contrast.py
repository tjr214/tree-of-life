import unittest
from color_utils import get_contrasting_text_color


class TestColorContrast(unittest.TestCase):
    """Test cases for the color contrast utility function."""

    def test_get_contrasting_text_color(self):
        """Test that dark backgrounds get white text and light backgrounds get black text."""
        # Dark colors should return white text
        self.assertEqual(get_contrasting_text_color(
            "#000000"), "#FFFFFF")  # Black
        self.assertEqual(get_contrasting_text_color(
            "#0000FF"), "#FFFFFF")  # Blue
        self.assertEqual(get_contrasting_text_color(
            "#006400"), "#FFFFFF")  # Dark Green
        self.assertEqual(get_contrasting_text_color(
            "#800000"), "#FFFFFF")  # Maroon
        self.assertEqual(get_contrasting_text_color(
            "#4B0082"), "#FFFFFF")  # Indigo

        # Light colors should return black text
        self.assertEqual(get_contrasting_text_color(
            "#FFFFFF"), "#000000")  # White
        self.assertEqual(get_contrasting_text_color(
            "#FFFF00"), "#000000")  # Yellow
        self.assertEqual(get_contrasting_text_color(
            "#ADD8E6"), "#000000")  # Light Blue
        self.assertEqual(get_contrasting_text_color(
            "#FFC0CB"), "#000000")  # Pink
        self.assertEqual(get_contrasting_text_color(
            "#FAFAD2"), "#000000")  # Light Goldenrod

        # Special case for bright green
        self.assertEqual(get_contrasting_text_color(
            "#00FF00"), "#000000")  # Bright Green

        # Edge cases near the threshold (128)
        self.assertEqual(get_contrasting_text_color("#808080"),
                         "#FFFFFF")  # Mid-gray (exactly at threshold)
        self.assertEqual(get_contrasting_text_color(
            "#7F7F7F"), "#FFFFFF")  # Just below threshold
        # Just above threshold (but still dark enough for white text)
        self.assertEqual(get_contrasting_text_color("#818181"), "#FFFFFF")

    def test_with_actual_color_schemes(self):
        """Test with colors that might be used in the Tree of Life visualization."""
        # Test with sample colors from Tree of Life color schemes
        # These are examples - update with actual colors from your schemes

        # King Scale examples
        self.assertEqual(get_contrasting_text_color(
            "#FFFF00"), "#000000")  # Yellow (Malkuth)
        self.assertEqual(get_contrasting_text_color(
            "#800080"), "#FFFFFF")  # Purple (Yesod)
        self.assertEqual(get_contrasting_text_color(
            "#FFA500"), "#000000")  # Orange (Hod)

        # Specific test for paths 14 and 22 in King Scale
        self.assertEqual(get_contrasting_text_color("#00FF00"),
                         "#000000")  # Green (Paths 14 and 22)

        # Queen Scale examples
        self.assertEqual(get_contrasting_text_color(
            "#00FFFF"), "#000000")  # Cyan
        self.assertEqual(get_contrasting_text_color(
            "#0000FF"), "#FFFFFF")  # Blue
        self.assertEqual(get_contrasting_text_color(
            "#FF0000"), "#FFFFFF")  # Red

        # Special cases
        self.assertEqual(get_contrasting_text_color("#888888"),
                         "#FFFFFF")  # Gray used for non-focused paths


if __name__ == "__main__":
    unittest.main()
