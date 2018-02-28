import numpy as np
import scr.FigureSupport as Fig
import scr.SamplePathClass as SamplePathSupport


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100 * self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = []  # create an empty list where rewards will be stored

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

    def get_rewards(self):
        return self._gameRewards

    def GamesOutcomes(self):
        return GamesOutcomes(self)


class GamesOutcomes:
    def __init__(self, simulated_games):
        """
        extracts outcomes of a simulated game
        :param simulated_games: a game after being simulated
        """
        self._simulatedGame = simulated_games
        # summary statistics on flips

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._simulatedGame.get_rewards()) / len(self._simulatedGame.get_rewards())

    def get_sample_path_game_rewards(self):
        return self._simulatedGame.get_rewards()


# run trail of 1000 games to calculate expected reward
games = SetOfGames(prob_head=0.5, n_games=1000)
GamesResults = games.GamesOutcomes()
# print the average reward
print('Expected reward when the probability of head is 0.5:', GamesResults.get_ave_reward())

Fig.graph_histogram(
    observations=games.get_rewards(),
    title="Histogram of Rewards for Flip Games",
    x_label='Rewards ($)',
    y_label="Number of Games")

SamplePathSupport.graph_sample_path(
    sample_path=games.get_rewards(),
    title="Win Loss Curve",
    x_label="Number of Games",
    y_label="Value ($)")