# Terminal Blackjack

A feature-rich command-line interface (CLI) version of the classic casino game Blackjack, built with Python.

## Features

-   **Classic Gameplay**: Play standard Blackjack against a dealer.
-   **Betting System**:
    -   Start with a **$500 Bankroll**.
    -   Place bets using chips (**$1, $5, $10, $25, $50**) or go **All In**.
    -   Bankroll persists across multiple rounds in a single session.
-   **Player Actions**:
    -   **Hit**: Take another card.
    -   **Stand**: End your turn.
    -   **Double Down**: Double your bet to take exactly one more card.
    -   **Split**: Split a pair of cards (e.g., two 8s) into two separate hands (requires matching bet).
-   **Payouts**:
    -   Standard Win: **1:1**
    -   Natural Blackjack (21 on first two cards): **3:2**
    -   Push (Tie): Bet returned.

## Requirements

-   Python 3.x
-   No external dependencies required (uses standard `random` library).

## How to Play

1.  **Clone the repository** (or download the `terminal_blackjack.py` file).
2.  **Run the game**:
    ```bash
    python terminal_blackjack.py
    ```
3.  **Follow the on-screen prompts**:
    -   Select chips to place your bet.
    -   Choose your action (`hit`, `stand`, `double`, `split`) based on your hand and the dealer's visible card.
    -   See if you can beat the dealer without busting (going over 21)!

## Future Improvements

-   [ ] Save/Load feature to persist bankroll between sessions.
-   [ ] Support for insurance bets.
-   [ ] Multiple difficulty levels or different dealer rules (e.g., Dealer hits soft 17).
-   [ ] Add a "Shoe" of multiple decks.
-   [ ] Add other "players" to play against the dealer.

## License

Free for personal use.

## Credits

Developed by Jon Key

