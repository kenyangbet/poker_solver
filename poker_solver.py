import itertools
import random

HAND_RANKINGS = {
    'Royal Flush': 10,
    'Straight Flush': 9,
    'Four of a Kind': 8,
    'Full House': 7,
    'Flush': 6,
    'Straight': 5,
    'Three of a Kind': 4,
    'Two Pair': 3,
    'One Pair': 2,
    'High Card': 1
}

def card_rank(card):
    rank_value_map = {
        '2': 1, '3': 2, '4': 3, '5': 4, '6': 5,
        '7': 6, '8': 7, '9': 8, 'T': 9, 
        'J': 10, 'Q': 11, 'K': 12, 'A': 13
    }
    rank = card[0] 
    return rank_value_map[rank]


def create_deck():
    suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
    ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    deck = [f'{rank} of {suit}' for rank, suit in itertools.product(ranks, suits)]
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

deck = create_deck()
deck = shuffle_deck(deck)

def deal_hands(deck, num_players=3, hand_size=2, dealt_cards=None):
    if dealt_cards is None:
        dealt_cards = []

    hands = [[] for _ in range(num_players)]

    for _ in range(hand_size):
        for i in range(num_players):
            card = deck.pop(0)  # Deal the top card to the player
            hands[i].append(card)
            dealt_cards.append(card)

    return hands, deck, dealt_cards

def deal_community_cards(deck, num_cards, dealt_cards=None):
    if dealt_cards is None:
        dealt_cards = []

    # Burn a card
    # burn_card = deck.pop(0)
    # dealt_cards.append(burn_card)

    # Deal the specified number of community cards
    community_cards = []
    for _ in range(num_cards):
        card = deck.pop(0)
        community_cards.append(card)
        dealt_cards.append(card)

    return community_cards, deck, dealt_cards

def evaluate_hand(hand):
    # Sort hand by rank
    hand = sorted(hand, key=lambda card: card_rank(card), reverse=True)
    
    if is_royal_flush(hand):
        return ('Royal Flush', hand)
    if is_straight_flush(hand):
        return ('Straight Flush', hand)
    if is_four_of_a_kind(hand):
        return ('Four of a Kind', hand)
    if is_full_house(hand):
        return ('Full House', hand)
    if is_flush(hand):
        return ('Flush', hand)
    if is_straight(hand):
        return ('Straight', hand)
    if is_set(hand):
        return ('Set', hand)
    if is_two_pair(hand):
        return ('Two Pair', hand)
    if is_pair(hand):
        return ('Pair', hand)
    else:
        return ('High Card', hand)

def is_pair(hand):
    ranks = [card_rank(card) for card in hand]
    card_rank_count = {}
    for rank in ranks:
        card_rank_count[rank] = card_rank_count.get(rank, 0) + 1

    return 2 in card_rank_count.values()

def is_two_pair(hand):
    ranks = [card_rank(card) for card in hand]
    card_rank_count = {}
    
    for rank in ranks:
        card_rank_count[rank] = card_rank_count.get(rank, 0) + 1

    first_pair = False
    second_pair = False

    for count in card_rank_count.values():
        if count == 2:
            first_pair = True
            del card_rank_count[rank]
            break

    for count in card_rank_count.values():
        if count == 2:
            second_pair = True
            break

    return first_pair and second_pair

def is_set(hand):
    ranks = [card_rank(card) for card in hand]
    card_rank_count = {}
    for rank in ranks:
        card_rank_count[rank] = card_rank_count.get(rank, 0) + 1

    return 3 in card_rank_count.values()

def is_straight(hand):
    ranks = sorted([card_rank(card) for card in hand], reverse=True)
    return ranks == list(range(ranks[0], ranks[0] - 5, -1))

def is_flush(hand):
    suits = [card[-1] for card in hand]
    
    suit_counts = {}
    for suit in suits:
        suit_counts[suit] = suit_counts.get(suit, 0) + 1
    
    return any(count >= 5 for count in suit_counts.values())



def is_full_house(hand):
    ranks = [card_rank(card) for card in hand]
    card_rank_count = {}
    
    for rank in ranks:
        card_rank_count[rank] = card_rank_count.get(rank, 0) + 1
    
    has_three_of_a_kind = False
    has_pair = False
    
    for count in card_rank_count.values():
        if count == 3:
            has_three_of_a_kind = True
            del card_rank_count[rank]
            break
        
    for count in card_rank_count.values():
        if count >= 2:
            has_pair = True
            break
    
    return has_three_of_a_kind and has_pair

def is_four_of_a_kind(hand):
    ranks = [card_rank(card) for card in hand]
    card_rank_count = {}
    for rank in ranks:
        card_rank_count[rank] = card_rank_count.get(rank, 0) + 1

    return 4 in card_rank_count.values()
    

def is_straight_flush(hand):
    return is_straight(hand) and is_flush(hand)

def is_royal_flush(hand):
    ranks = sorted([card_rank(card) for card in hand], reverse=True)
    return is_straight_flush and ranks[0] == card_rank('A')

def evaluate_hand_strength(hand):
    
    return random.random()  

def calculate_all_players_winning_odds(hands, deck, known_community_cards, dealt_cards):
    num_players = len(hands)
    win_counts = [0] * num_players
    total_outcomes = 0

    # Determine the number of cards left to deal
    num_cards_to_deal = 5 - len(known_community_cards)
    
    # Generate all possible combinations of remaining community cards
    remaining_deck = [card for card in deck if card not in dealt_cards]
    possible_community_cards = list(itertools.combinations(remaining_deck, num_cards_to_deal))

    for community_cards in possible_community_cards:
        community_cards = list(community_cards) + known_community_cards

        # Evaluate each player's hand strength
        player_strengths = []
        for hand in hands:
            strength = evaluate_hand_strength(hand + community_cards)
            player_strengths.append(strength)

        # Determine the winner(s)
        max_strength = max(player_strengths)
        winners = [i for i, strength in enumerate(player_strengths) if strength == max_strength]

        # Distribute the win equally among all winners (split pot scenario)
        for winner in winners:
            win_counts[winner] += 1 / len(winners)

        total_outcomes += 1

    # Calculate the probability of winning for each player
    win_probabilities = [wins / total_outcomes for wins in win_counts]
    return win_probabilities

def main():
    deck = create_deck()
    deck = shuffle_deck(deck)
    dealt_cards = []

    num_players = 3  # Example: 3 players in the hand
    hands, deck, dealt_cards = deal_hands(deck, num_players, dealt_cards=dealt_cards)

    # Deal the flop (3 community cards)
    flop, deck, dealt_cards = deal_community_cards(deck, 3, dealt_cards)
    
    # Deal the turn (1 community card)
    turn, deck, dealt_cards = deal_community_cards(deck, 1, dealt_cards)
    
    # Deal the river (1 community card)
    river, deck, dealt_cards = deal_community_cards(deck, 1, dealt_cards)
    
    community_cards = flop + turn + river

    print(f"Player 1's hand: {hands[0]}")
    print(f"Player 2's hand: {hands[1]}")
    print(f"Player 3's hand: {hands[2]}")
    print(f"Flop: {flop}, Turn: {turn}, River: {river}")

    # Calculate the exact odds of winning for all players
    # win_odds = calculate_all_players_winning_odds(hands, deck, flop + turn + river, dealt_cards)
    # for i, odds in enumerate(win_odds, start=1):
    #     print(f"Exact odds of winning for Player {i}: {odds * 100:.2f}%")

main()