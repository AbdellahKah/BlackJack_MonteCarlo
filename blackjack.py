import random
import matplotlib.pyplot as plt

# 1. Define the Deck
def draw_card():
    # Cards 2-10, plus three face cards (10s), plus an Ace (11)
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(deck)

def calculate_total(hand):
    total = sum(hand)
    aces = hand.count(11)
    # Adjust for Aces if busting
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

# 2. Define the Dealer's Logic
def play_dealer(dealer_hand):
    while True:
        total = calculate_total(dealer_hand)
        
        # Check if the hand is exactly 17 and "Soft"
        # A Soft 17 means the raw sum of the cards (with Aces as 11) is 17
        is_soft_17 = False
        if total == 17:
            # If the raw sum is exactly 17 and contains an Ace, it's soft.
            if sum(dealer_hand) == 17 and 11 in dealer_hand:
                is_soft_17 = True
                
        # Dealer hits if total is under 17 OR if it's a Soft 17
        if total < 17 or is_soft_17:
            dealer_hand.append(draw_card())
        else:
            break
            
    return calculate_total(dealer_hand)

# 3. Define the Player's Logic (Simplified Basic Strategy)
def play_player(player_hand, dealer_upcard):
    while True:
        total = calculate_total(player_hand)
        if total >= 21:
            break
        
        # Very simplified Basic Strategy
        if total <= 11:
            player_hand.append(draw_card()) # Always hit 11 or less
        elif total >= 17:
            break # Always stand on 17 or more
        else:
            # If player has 12-16, stand if dealer shows weak card (2-6), else hit
            if dealer_upcard in [2, 3, 4, 5, 6]:
                break
            else:
                player_hand.append(draw_card())
                
    return calculate_total(player_hand)

# 4. The Monte Carlo Simulation Loop
def run_simulation(iterations=1000000):
    bankroll = 0
    history = []
    
    for i in range(1, iterations + 1):
        # Deal initial cards
        player_hand = [draw_card(), draw_card()]
        dealer_hand = [draw_card(), draw_card()]
        dealer_upcard = dealer_hand[0]
        
        # Check for natural blackjacks
        player_bj = calculate_total(player_hand) == 21
        dealer_bj = calculate_total(dealer_hand) == 21
        
        if player_bj and not dealer_bj:
            bankroll += 1.5 # Standard 3:2 payout
        elif dealer_bj and not player_bj:
            bankroll -= 1
        elif player_bj and dealer_bj:
            pass # Push
        else:
            # Play out the hand
            player_total = play_player(player_hand, dealer_upcard)
            
            if player_total > 21:
                bankroll -= 1 # Player busts
            else:
                dealer_total = play_dealer(dealer_hand)
                if dealer_total > 21:
                    bankroll += 1 # Dealer busts
                elif player_total > dealer_total:
                    bankroll += 1 # Player wins
                elif player_total < dealer_total:
                    bankroll -= 1 # Dealer wins
                # Else push, bankroll doesn't change
        
        # Calculate Expected Value (EV) as a percentage
        current_ev = (bankroll / i) * 100
        # Sample every 1000th hand to keep plotting memory low
        if i % 1000 == 0:
            history.append(current_ev)

    print(f"Final EV after {iterations} hands: {current_ev:.4f}%")
    return history

# 5. Run and Visualize
ev_history = run_simulation(1000000)

plt.plot(range(1000, 1000000 + 1, 1000), ev_history)
plt.axhline(y=-0.5, color='r', linestyle='--', label='Theoretical House Edge (-0.5%)')
plt.title("Blackjack Monte Carlo Convergence")
plt.xlabel("Hands Played")
plt.ylabel("Running Expected Value (%)")
plt.legend()
plt.grid(True)
plt.show()