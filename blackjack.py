# game of black jack
import sys, random

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = "backside"


def show_intro():
    print('''Welcome to the game of blackjack
         rules:
                The goal of the game is to have a hand value of 21 or as close to 21 as possible without going over.

    Each player is dealt two cards face up, and the dealer is dealt one card face up and one card face down.

    Aces can be worth 1 or 11 points, face cards (kings, queens, and jacks) are worth 10 points, and all other cards are worth their numerical value.

    Players can choose to "hit" and receive additional cards to improve their hand value, or "stand" and keep their current hand.

    If a player's hand value exceeds 21, they lose the game (this is called "busting").

    After all players have finished their turns, the dealer reveals their face-down card and continues to hit until their hand value is 17 or greater.

    If the dealer busts, all remaining players win the game. If the dealer does not bust, each player's hand value is compared to the dealer's hand value, and the player with the higher hand value wins.

    In the event of a tie (called a "push"), no one wins or loses, and the player's bet is returned.

    There are additional rules for splitting pairs, doubling down, and taking insurance bets, which can vary depending on the specific variation of Blackjack being played.''')
    print()


def get_money(maxbet):
    bet = 0
    # loop through until user enters a valid amount
    while True:
        print("enter the amount you want to stake! or press 'Q' to QUIT")
        ans = input(">").upper()
        if ans.startswith("Q"):
            sys.exit()
        elif ans == None:
            continue
        elif 1 <= int(ans) <= maxbet:
            bet = int(ans)
            break
    return bet


def get_deck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))
        for rank in ("J", "K", "A", "Q"):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck


def display_hand(player_hand, dealer_hand, showdealerhand):
    if showdealerhand:
        print("dealer's value:", {get_value(dealer_hand)})
        display_cards(dealer_hand)
    else:
        print("dealer Cards first face-down:???")
        display_cards([BACKSIDE] + dealer_hand[1:])
    print("player's cards value", get_value(player_hand))
    display_cards(player_hand)


def get_value(cards):
    # this checks the value of aces and gives checks for an appropriate value for the aces
    value = 0
    numbofAces = 0
    for card in cards:
        rank = card[0]
        if rank == "A":
            numbofAces += 1  # checks if user got an ace
        elif rank in ("J", "K", "A", "Q"):
            value += 10  # checks for value of card worth 10 points
        else:
            value += int(rank)  # checks for cards worth their face value
    value += numbofAces
    for i in range(numbofAces):  # checks for a better choice for the aces either 1 or 11
        if value + 10 <= 21:
            value += 10
    return value


def display_cards(cards):
    rows = ['', '', '', '', '']
    for i, card in enumerate(cards):
        rows[0] += '___ '  # print the top of the line
        if card == BACKSIDE:  # printing the back of the line
            rows[1] += '|##|'
            rows[2] += '|###|'
            rows[3] += '|_##|'
        else:
            rank, suit = card
            rows[1] += '|{}|'.format(rank.ljust(2))
            rows[2] += '|{}|'.format(suit)
            rows[3] += '|{}|'.format(rank.rjust(2, "_"))
    for row in rows:
        print(row)


def get_move(player_cards, money):
    while True:
        # Asks the player for their move, and returns 'H' for hit, 'S' for
        # stand, and 'D' for double down.
        moves = ['(H),(S)']
        # The player can double down if he has two cards
        if len(player_cards) == 2 and money > 0:
            moves.append("(D)")
        availableMoves = " ,".join(moves)
        print("your available moves are:", availableMoves)
        move = input(">enter a move:").upper()
        if move in availableMoves:
            return move


def main():
    show_intro()
    money = 5000
    again = True
    while again:
        if money <= 0:
            print("you are broke !!!")
            print("What a loser")
            print("try you luck some where else")

            sys.exit()
        print(f"money:{money}")
        bet = get_money(money)
        deck = get_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        print(f"bet: {bet}")
        while True:
            display_hand(player_hand, dealer_hand, False)

            if get_value(player_hand) > 21:
                # print("you lose!!")
                break
            # elif get_value(player_hand) == 21:
            #     print("you win!!")
            #     break
            move = get_move(player_hand, money - bet)
            if move == "D":
                print("DOUBLING DOWN...")
                additional_bet = get_money(min(bet, (money - bet)))
                bet += additional_bet
                print(f"bet has increased  by {additional_bet} ")
            if move in ("H", "D"):
                new_card = deck.pop()
                rank, suit = new_card
                print(f"you drew {rank} of {suit}")
                player_hand.append(new_card)
                if get_value(player_hand) > 21:
                    # the player has busted
                    continue
            if move in ("S", "D"):
                break

        # handling dealer's actions
        if get_value(player_hand) <= 21:
            while get_value(dealer_hand) < 17:
                # dealer hits...
                print("dealer hits....")
                dealer_hand.append(deck.pop())
                display_hand(player_hand, dealer_hand, False)
                if get_value(dealer_hand) > 21:  # when dealer busts...
                    break
                input("> press INDAA!! to SEE RESULTS")
            # ....................
        display_hand(player_hand, dealer_hand, True)
        playerValue = get_value(player_hand)
        dealerValue = get_value(dealer_hand)
        if dealerValue > 21:
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('It\'s a tie, the bet is returned to you.')

        playagain = input('Do you want to play again[Y/N]').upper()
        if playagain not in ("Y", "N"):
            sys.exit()
        elif playagain == "y":
            again = True
        elif playagain == "N":
            again = False

        print('\n\n')


if __name__ == '__main__':
    main()
