"""
Water Sort Puzzle Game
"""

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "A* Water Sort"


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.FLORAL_WHITE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.water_tubes = [[], [], []]
        self.move_history = []  # list of tuples (from, to)

        self.moves_label = arcade.Text(
            f"Moves: {len(self.move_history)}",
            150,
            600,
            arcade.csscolor.BLACK,
            18,
            font_name="Arial",
        )

        # todo: solve the puzzle here, then store the solution

    # Draw a water tube centered at the given position with the given colors
    def draw_water_tube(self, x, y, colors):
        # Draw the water
        for idx, color in enumerate(colors[::-1]):
            if color is None:
                continue

            if idx == 0:  # bottom layer arc
                arcade.draw_arc_filled(
                    x, y - 250, 100, 100, arcade.csscolor.BLUE, 180, 360
                )
            else:
                arcade.draw_rectangle_filled(x, y - (275 - (idx * 50)), 100, 50, color)

        # Draw the border
        arcade.draw_arc_outline(
            x, y - 250, 100, 100, arcade.csscolor.BLACK, 180, 360, 2
        )
        arcade.draw_line_strip(
            [
                (x - 50, y - 250),
                (x - 50, y + 100),
                (x + 50, y + 100),
                (x + 50, y - 250),
            ],
            arcade.csscolor.BLACK,
            2,
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Update the moves label text
        self.moves_label.text = f"Moves: {len(self.move_history)}"

        # Draw the lined paper background
        for i in range(0, 10):
            arcade.draw_line(
                0,
                (i + 1) * 50,
                SCREEN_WIDTH,
                (i + 1) * 50,
                arcade.csscolor.LIGHT_SKY_BLUE,
                2,
            )
        arcade.draw_line(100, 0, 100, SCREEN_HEIGHT, arcade.csscolor.INDIANRED, 2)

        # Draw the move counter label
        self.moves_label.draw()

        # Draw the water tubes
        for idx, tube in enumerate(self.water_tubes):
            self.draw_water_tube(200 + idx * 200, 350, tube)


def main():
    """Main function"""
    window = MyGame()
    window.setup()

    # Initialize the water tube layers
    # Water color layers from top to bottom, or None for an empty layer
    window.water_tubes = [
        [
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.RED,
            arcade.csscolor.GREEN,
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.RED,
            arcade.csscolor.GREEN,
        ],
        [
            None,
            None,
            None,
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.RED,
            arcade.csscolor.GREEN,
            arcade.csscolor.BLUE,
        ],
        [
            None,
            None,
            None,
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.RED,
            arcade.csscolor.GREEN,
            arcade.csscolor.BLUE,
        ],
        [
            None,
            None,
            None,
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.RED,
            arcade.csscolor.GREEN,
            arcade.csscolor.BLUE,
        ],
    ]

    # Main loop
    arcade.run()


if __name__ == "__main__":
    main()
