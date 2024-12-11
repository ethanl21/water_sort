"""
Water Sort Puzzle Game
"""

import arcade
import copy
import water_sort
import json

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "A* Water Sort"

# Button constants
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_PADDING = 10  # Padding between buttons


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.FLORAL_WHITE)

        # Calculate button positions
        self.back_button_x = (
            SCREEN_WIDTH - BUTTON_PADDING - (BUTTON_WIDTH * 2) - BUTTON_PADDING
        )
        self.forward_button_x = SCREEN_WIDTH - BUTTON_PADDING - BUTTON_WIDTH
        self.button_y = SCREEN_HEIGHT - BUTTON_PADDING - (BUTTON_HEIGHT / 2)

        # Move counter label object, not used in the search
        self.moves_label = arcade.Text(
            "",
            150,
            600,
            arcade.csscolor.BLACK,
            18,
            font_name="Arial",
        )

    def setup(self, tubes):
        """Set up the game here. Call this function to restart the game."""

        # Init the state
        self.initial_state = copy.deepcopy(tubes)
        self.state = copy.deepcopy(tubes)

        self.solution = water_sort.solve(tubes)
        self.solution_step = 0
        self.solution_state_history = []
        self.solution_state_history.append(copy.deepcopy(self.state))

    # Draw a water tube centered at the given position with the given colors
    def draw_water_tube(self, x, y, colors):
        # Draw the water
        for idx, color in enumerate(colors):
            if idx == 0:  # bottom layer arc
                arcade.draw_arc_filled(x, y - 250, 100, 100, color, 180, 360)
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
        self.moves_label.text = f"Moves: {self.solution_step}"

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

        for idx, tube in enumerate(self.state):
            self.draw_water_tube(200 + idx * 200, 350, tube)

        # Draw the back and forward buttons

        # Draw "Back" button
        arcade.draw_rectangle_filled(
            self.back_button_x,
            self.button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            arcade.color.DARK_RED,
        )
        arcade.draw_text(
            "Back",
            self.back_button_x,
            self.button_y,
            arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
            anchor_y="center",
        )

        # Draw "Forward" button
        arcade.draw_rectangle_filled(
            self.forward_button_x,
            self.button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            arcade.color.DARK_GREEN,
        )
        arcade.draw_text(
            "Forward",
            self.forward_button_x,
            self.button_y,
            arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
            anchor_y="center",
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse click events."""
        if (
            self.back_button_x - BUTTON_WIDTH / 2
            <= x
            <= self.back_button_x + BUTTON_WIDTH / 2
            and self.button_y - BUTTON_HEIGHT / 2
            <= y
            <= self.button_y + BUTTON_HEIGHT / 2
        ):
            print("Back button clicked!")
            if self.solution_step > 0:
                self.solution_step -= 1
                self.state = copy.deepcopy(
                    self.solution_state_history[self.solution_step]
                )

        if (
            self.forward_button_x - BUTTON_WIDTH / 2
            <= x
            <= self.forward_button_x + BUTTON_WIDTH / 2
            and self.button_y - BUTTON_HEIGHT / 2
            <= y
            <= self.button_y + BUTTON_HEIGHT / 2
        ):
            print("Forward button clicked!")
            if self.solution_step < len(self.solution):
                src_idx, dest_idx = self.solution[self.solution_step]
                self.state = water_sort.apply_move(self.state, src_idx, dest_idx)
                self.solution_state_history.append(copy.deepcopy(self.state))
                self.solution_step += 1


def main():
    """Main function"""

    # Initialize the water tube layers
    # Water color layers from bottom to top, or None for an empty layer
    water_tubes = [[], [], [], []]

    with open("puzzle.json", "r") as f:
        water_tubes = json.load(f)
        water_tubes = water_tubes["tubes"]

    # convert all rgb lists to tuples
    for tube in water_tubes:
        for i in range(len(tube)):
            tube[i] = tuple(tube[i])

    print(water_tubes)
    window = MyGame()
    window.setup(water_tubes)

    # Main loop
    arcade.run()


if __name__ == "__main__":
    main()
