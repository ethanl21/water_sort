"""
Water Sort Puzzle Game
"""

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "A* Water Sort"


class WaterSortAStar:
    def __init__(self, water_tubes, max_layers=8):
        self.water_tubes = water_tubes
        self.max_layers = max_layers
        self.history = []

    def top_color(self, tube):
        return tube[-1] if tube else None

    def pourable_count(self, tube):
        top_color = self.top_color(tube)
        for i, color in enumerate(tube[::-1]):
            print(i, color)
            if color != top_color:
                return i + 1

        return len(tube)

    def is_sorted(tube):
        # Empty or nonexistent tubes are considered sorted
        if not tube or tube == []:
            return True

        # Sorted tubes have only one color
        return len(set(tube)) == 1

    def heuristic(self):
        # Heuristic is the number of tubes that are not sorted
        return sum(1 for tube in self.water_tubes if not self.is_sorted(tube))

    def is_goal(self):
        return self.heuristic() == 0

    def can_pour(self, from_tube_idx, to_tube_idx):
        _from = self.water_tubes[from_tube_idx]
        _to = self.water_tubes[to_tube_idx]

        # Can't pour from an empty tube
        if not _from or _from == []:
            print("from is empty")
            return False

        # Can't pour into a full tube
        if len(_to) == self.max_layers:
            print("to is full")
            return False

        # Can't pour if the top colors don't match
        if _from[-1] != _to[-1]:
            print(_from[-1], _to[-1])
            print("top colors do not match")
            return False

        # from_tube not empty, to_tube not full, and top colors match
        return True

    def pour(self, from_tube_idx, to_tube_idx):
        # Can't pour if the tubes are not compatible
        if not self.can_pour(from_tube_idx, to_tube_idx):
            print(f"Cannot pour from {from_tube_idx} to {to_tube_idx}")
            return

        print(f"Pouring from {from_tube_idx} to {to_tube_idx}")
        # copy the tubes
        _from = self.water_tubes[from_tube_idx]
        _to = self.water_tubes[to_tube_idx]

        # get the top color of the from tube
        pour_color = self.top_color(_from)

        # determine how many layer can be poured from the from_tube
        from_count = self.pourable_count(_from)

        # determine how many layer can be poured into the to_tube
        to_count = self.max_layers - len(_to)

        # determine how many layers can be poured
        pour_count = min(from_count, to_count)
        print(f"Pouring {pour_count} layers")

        # pour the layers
        for _ in range(pour_count):
            _to.append(pour_color)
            _from.pop()

        # update the tubes
        self.water_tubes[from_tube_idx] = _from
        self.water_tubes[to_tube_idx] = _to
        
        # Save the move
        self.history.append((from_tube_idx, to_tube_idx))


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.FLORAL_WHITE)

    def setup(self, tubes):
        """Set up the game here. Call this function to restart the game."""

        # Init the state
        self.state = WaterSortAStar(tubes)

        self.state.pour(0, 1)

        # todo: solve the puzzle

        # Move counter label object, not used in the search
        self.moves_label = arcade.Text(
            f"Moves: {len(self.state.history)}",
            150,
            600,
            arcade.csscolor.BLACK,
            18,
            font_name="Arial",
        )

    # Draw a water tube centered at the given position with the given colors
    def draw_water_tube(self, x, y, colors):
        # Draw the water
        for idx, color in enumerate(colors):
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
        self.moves_label.text = f"Moves: {len(self.state.history)}"

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
        for idx, tube in enumerate(self.state.water_tubes):
            self.draw_water_tube(200 + idx * 200, 350, tube)


def main():
    """Main function"""

    # Initialize the water tube layers
    # Water color layers from bottom to top, or None for an empty layer
    water_tubes = [
        [
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.RED,
            arcade.csscolor.GREEN,
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.GREEN,
            arcade.csscolor.GREEN,
        ],
        [
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.RED,
            arcade.csscolor.GREEN,
            arcade.csscolor.BLUE,
            arcade.csscolor.GREEN,
        ],
        [
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.RED,
            arcade.csscolor.GREEN,
            arcade.csscolor.BLUE,
        ],
        [
            arcade.csscolor.BLUE,
            arcade.csscolor.INDIANRED,
            arcade.csscolor.RED,
            arcade.csscolor.GREEN,
            arcade.csscolor.BLUE,
        ],
    ]

    window = MyGame()
    window.setup(water_tubes)

    # Main loop
    arcade.run()


if __name__ == "__main__":
    main()
