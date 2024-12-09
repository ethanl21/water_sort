import heapq
from copy import deepcopy

def is_sorted(tube):
    """Check if a tube is fully sorted or empty."""
    return not tube or len(set(tube)) == 1


def heuristic(state):
    """Heuristic: count the number of unsorted tubes."""
    return sum(not is_sorted(tube) for tube in state)


def valid_moves(state):
    """
    Generate all valid moves as (src_idx, dest_idx).
    A move is valid if liquid can be poured from src to dest.
    """
    moves = []
    for src_idx, src in enumerate(state):
        if not src:  # Skip empty tubes
            continue
        # Find topmost color to pour
        top_color = src[-1]
        contiguous_count = sum(1 for i in reversed(src) if i == top_color)

        for dest_idx, dest in enumerate(state):
            if src_idx == dest_idx:  # Skip pouring into the same tube
                continue
            if not dest or (
                dest[-1] == top_color and len(dest) + contiguous_count <= 8
            ):
                moves.append((src_idx, dest_idx))
    return moves


def apply_move(state, src_idx, dest_idx):
    """
    Apply a move to the state and return the new state.
    A move is pouring liquid from src_idx to dest_idx.
    """
    state = deepcopy(state)
    src, dest = state[src_idx], state[dest_idx]
    top_color = src[-1]
    contiguous_count = sum(1 for i in reversed(src) if i == top_color)

    # Transfer liquid
    pour_amount = min(contiguous_count, 8 - len(dest))
    for _ in range(pour_amount):
        dest.append(src.pop())

    return state


def is_goal_state(state):
    """Check if all tubes are sorted or empty."""
    return all(is_sorted(tube) for tube in state)


def solve(initial_state):
    """Solve the Water Sort Puzzle using A*."""
    # Priority queue: (cost, heuristic, state, path)
    priority_queue = []
    visited = set()

    # Convert initial state to a tuple of tuples for immutability in visited set
    initial_state_key = tuple(tuple(tube) for tube in initial_state)
    heapq.heappush(priority_queue, (0, heuristic(initial_state), initial_state, []))
    visited.add(initial_state_key)

    while priority_queue:
        cost, _, current_state, path = heapq.heappop(priority_queue)

        # Check if goal state is reached
        if is_goal_state(current_state):
            return path

        for src_idx, dest_idx in valid_moves(current_state):
            new_state = apply_move(current_state, src_idx, dest_idx)
            new_state_key = tuple(tuple(tube) for tube in new_state)
            if new_state_key not in visited:
                visited.add(new_state_key)
                new_path = path + [(src_idx, dest_idx)]
                heapq.heappush(
                    priority_queue,
                    (cost + 1, heuristic(new_state), new_state, new_path),
                )

    return None  # No solution found
