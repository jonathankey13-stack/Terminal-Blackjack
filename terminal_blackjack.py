# Terminal Blackjack
import random

# Game Constants
CHIPS = [1, 5, 10, 25, 50]
STARTING_BANKROLL = 500

def create_deck():
    card_values = {
        "Ace of Spades": 11, "Ace of Hearts": 11, "Ace of Diamonds": 11, "Ace of Clubs": 11,
        "2 of Spades": 2, "2 of Hearts": 2, "2 of Diamonds": 2, "2 of Clubs": 2,
        "3 of Spades": 3, "3 of Hearts": 3, "3 of Diamonds": 3, "3 of Clubs": 3,
        "4 of Spades": 4, "4 of Hearts": 4, "4 of Diamonds": 4, "4 of Clubs": 4,
        "5 of Spades": 5, "5 of Hearts": 5, "5 of Diamonds": 5, "5 of Clubs": 5,
        "6 of Spades": 6, "6 of Hearts": 6, "6 of Diamonds": 6, "6 of Clubs": 6,
        "7 of Spades": 7, "7 of Hearts": 7, "7 of Diamonds": 7, "7 of Clubs": 7,
        "8 of Spades": 8, "8 of Hearts": 8, "8 of Diamonds": 8, "8 of Clubs": 8,
        "9 of Spades": 9, "9 of Hearts": 9, "9 of Diamonds": 9, "9 of Clubs": 9,
        "10 of Spades": 10, "10 of Hearts": 10, "10 of Diamonds": 10, "10 of Clubs": 10,
        "Jack of Spades": 10, "Jack of Hearts": 10, "Jack of Diamonds": 10, "Jack of Clubs": 10,
        "Queen of Spades": 10, "Queen of Hearts": 10, "Queen of Diamonds": 10, "Queen of Clubs": 10,
        "King of Spades": 10, "King of Hearts": 10, "King of Diamonds": 10, "King of Clubs": 10,
    }
    deck = list(card_values.keys())
    random.shuffle(deck)
    return deck, card_values

def get_card_value(card, card_values):
    # Helper to get the numeric value for comparison (e.g., King = 10)
    return card_values[card]

def calculate_score(hand_cards, card_values):
    score = 0
    aces = 0
    for card in hand_cards:
        val = card_values[card]
        score += val
        if "Ace" in card:
            aces += 1
    
    # Adjust for Aces if score is > 21
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    
    return score

class Hand:
    def __init__(self, bet):
        self.cards = []
        self.bet = bet
        self.done = False
        self.bust = False
        self.doubled = False
        self.score = 0

    def add_card(self, card):
        self.cards.append(card)

    def update_score(self, card_values):
        self.score = calculate_score(self.cards, card_values)
        if self.score > 21:
            self.bust = True
            self.done = True

class Dealer:
    def __init__(self, deck, card_values):
        self.hand = []
        self.score = 0
        self.deck = deck
        self.card_values = card_values

    def deal_card(self):
        if not self.deck:
            return None 
        return self.deck.pop()

    def update_score(self):
        self.score = calculate_score(self.hand, self.card_values)

    def dealer_turn(self):
        self.update_score()
        print("\nDealer's turn...")
        print(f"Dealer's current hand: {self.hand}")
        print(f"Dealer's score: {self.score}")
        while self.score < 17:
            new_card = self.deal_card()
            self.hand.append(new_card)
            self.update_score()
            print(f"Dealer hits and draws: {new_card}")
            print("Dealer's hand:", self.hand)
            print("Dealer's score:", self.score)
        
        if self.score > 21:
            print("Dealer busts.")
        else:
            print(f"Dealer stands with {self.score}.")

class Player:
    def __init__(self, card_values):
        self.hands = [] # List of Hand objects
        self.card_values = card_values

    def add_hand(self, hand):
        self.hands.append(hand)

    def hit(self, hand, dealer):
        new_card = dealer.deal_card()
        hand.add_card(new_card)
        hand.update_score(self.card_values)
        print(f"You drew: {new_card}")

def place_bet(bankroll):
    current_bet = 0
    print(f"\nCurrent Bankroll: ${bankroll}")
    print(f"Available Chips: {', '.join(['$' + str(c) for c in CHIPS])}")
    print("Commands: Type the chip amount to add (e.g., '10'), 'all' for all in, or 'done' to finish betting.")
    
    while True:
        choice = input(f"Current Bet: ${current_bet}. Add chip: ").lower().strip()
        
        if choice == 'done':
            if current_bet == 0:
                print("You must bet at least something!")
                continue
            return current_bet
        
        if choice == 'all':
             if bankroll == 0:
                 print("You have no money!")
                 continue
             print(f"Going all in! Added ${bankroll - current_bet}")
             current_bet = bankroll
             return current_bet

        try:
            amount = int(choice)
            if amount in CHIPS:
                if current_bet + amount <= bankroll:
                    current_bet += amount
                    print(f"Added ${amount}.")
                else:
                    print(f"Not enough funds! You only have ${bankroll - current_bet} left to bet.")
            else:
                print(f"Invalid chip. Choose from: {CHIPS}")
        except ValueError:
            print("Invalid input. Type a chip amount, 'all', or 'done'.")

def play_round(bankroll):
    deck, card_values = create_deck()
    dealer = Dealer(deck, card_values)
    player = Player(card_values)
    
    initial_bet = place_bet(bankroll)
    bankroll -= initial_bet
    
    # Create initial hand
    main_hand = Hand(initial_bet)
    player.add_hand(main_hand)

    # Initial Deal
    player.hit(main_hand, dealer)
    dealer.hand.append(dealer.deal_card()) 
    player.hit(main_hand, dealer)
    dealer.hand.append(dealer.deal_card()) 
    
    # FOR TESTING SPLIT ONLY
    # main_hand.add_card("8 of Spades")
    # main_hand.add_card("8 of Hearts")
    # dealer.hand.append("5 of Clubs")
    # dealer.hand.append("10 of Diamonds") 
    
    dealer.update_score()
    
    print("\n--- Game Start ---")
    print(f"Dealer's visible card: {dealer.hand[0]}") 

    # Loop through each hand (index based because splitting adds to the list)
    # Using index `i` allows us to process newly added split hands
    i = 0
    while i < len(player.hands):
        current_hand = player.hands[i]
        
        print(f"\n--- Playing Hand {i + 1} ---")
        print(f"Cards: {current_hand.cards}")
        current_hand.update_score(card_values)
        print(f"Score: {current_hand.score}")
        print(f"Bet: ${current_hand.bet}")

        # Check natural blackjack on first hand only.
        # Simplification: If 21 on two cards, auto-stand.
        if current_hand.score == 21 and len(current_hand.cards) == 2:
            print("Blackjack/21!")
            current_hand.done = True

        while not current_hand.done:
            action = input(f"Hand {i+1} Action (hit, stand, double, split): ").lower().strip()
            
            if action == "hit":
                player.hit(current_hand, dealer)
                print(f"Hand {i+1}: {current_hand.cards}")
                print(f"Score: {current_hand.score}")
                if current_hand.score > 21:
                    print("Bust!")
                    # Hand marked done by update_score
            
            elif action == "stand":
                print(f"Stood on {current_hand.score}")
                current_hand.done = True
            
            elif action == "double" or action == "double down":
                if len(current_hand.cards) != 2:
                    print("Can only double on first two cards.")
                    continue
                
                if bankroll < current_hand.bet:
                    print("Not enough funds to double down!")
                    continue
                
                bankroll -= current_hand.bet
                current_hand.bet *= 2
                current_hand.doubled = True
                print(f"Doubled down! Bet is now ${current_hand.bet}.")
                
                player.hit(current_hand, dealer)
                print(f"Hand {i+1}: {current_hand.cards}")
                print(f"Score: {current_hand.score}")
                if current_hand.score > 21:
                    print("Bust!")
                
                current_hand.done = True
            
            elif action == "split":
                if len(current_hand.cards) != 2:
                    print("Can only split with exactly two cards.")
                    continue
                
                # Check for strict rank equality (e.g. two Kings)
                val1 = card_values[current_hand.cards[0]]
                val2 = card_values[current_hand.cards[1]]
                
                if val1 != val2:
                     print("Cannot split non-matching cards.")
                     continue
                
                if bankroll < current_hand.bet:
                    print("Not enough funds to split!")
                    continue
                    
                print("Splitting hand...")
                bankroll -= current_hand.bet # Pay for the new hand
                
                # Create new hand
                split_card = current_hand.cards.pop() # Remove second card
                new_hand = Hand(current_hand.bet)
                new_hand.add_card(split_card)
                
                # Add to player hands
                player.add_hand(new_hand)
                
                # Current hand needs a new card
                player.hit(current_hand, dealer)
                
                # Deal 1 card to each split ace/card immediately.
                new_card_2 = dealer.deal_card()
                new_hand.add_card(new_card_2)
                print(f"Split completed. Hand {i+1} has {current_hand.cards}. Hand {len(player.hands)} has {new_hand.cards}")
                
                current_hand.update_score(card_values)
                print(f"Hand {i+1} cards: {current_hand.cards}")
                print(f"Hand {i+1} score: {current_hand.score}")
                
            else:
                print("Invalid action.")
        
        i += 1 # Move to next hand
    
    # Resolution
    # Dealer plays if at least one hand is not busted
    all_busted = all(h.bust for h in player.hands)
    
    if not all_busted:
        dealer.dealer_turn()
    else:
        print("\nAll hands busted. Dealer wins.")
        
    total_winnings = 0
    print("\n--- Final Results ---")
    print(f"Dealer Score: {dealer.score} (Bust: {dealer.score > 21})")
    
    for idx, hand in enumerate(player.hands):
        print(f"\nHand {idx+1}: {hand.cards} | Score: {hand.score} | Bet: ${hand.bet}")
        
        if hand.bust:
            print(f"Hand {idx+1} Busted. Lost ${hand.bet}.")
        elif dealer.score > 21:
             print(f"Dealer Busts. Hand {idx+1} Wins!")
             win_amt = hand.bet * 2
             if hand.score == 21 and len(hand.cards) == 2 and not hand.doubled: 
                  # Check if it was a 'split' 21. Split 21 is not natural blackjack.
                  pass
             total_winnings += win_amt
             print(f"Won ${win_amt - hand.bet}.")
        elif hand.score > dealer.score:
             print(f"Hand {idx+1} Wins!")
             total_winnings += hand.bet * 2
             print(f"Won ${hand.bet}.")
        elif hand.score < dealer.score:
             print(f"Dealer Wins against Hand {idx+1}.")
             print(f"Lost ${hand.bet}.")
        else:
             print(f"Push for Hand {idx+1}.")
             total_winnings += hand.bet
             print(f"Returned ${hand.bet}.")
             
    new_bankroll = bankroll + total_winnings
    return new_bankroll

def main():
    bankroll = STARTING_BANKROLL
    print("Welcome to Terminal Blackjack!")
    
    while True:
        if bankroll <= 0:
            print("You're out of money! Game Over.")
            break
            
        bankroll = play_round(bankroll)
        print(f"\nFinal Bankroll: ${bankroll}")
        
        cont = input("Play another round? (y/n): ").lower().strip()
        if cont != 'y':
            print(f"You walked away with ${bankroll}.")
            break

if __name__ == "__main__":
    main()
