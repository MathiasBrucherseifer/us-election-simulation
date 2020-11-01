import numpy as np
import matplotlib.pyplot as plt


def generate_file_name_addon(runs, bias, deviation, correlation):
    file_name_addon = 'bias_factor_' + str(round(bias, 1)) \
                      + '_runs_' + str(runs) \
                      + '_deviation_' + str(round(deviation, 1)) \
                      + '_correlation_' + str(round(correlation, 1))
    return file_name_addon


def generate_state_title(state, mu, sigma, win_perc_trump, runs, bias, deviation, correlation):
    return_string = state + ': mu=' + str(round(mu, 2)) \
                          + ', sigma=' + str(round(sigma, 2)) \
                          + ', trump=' + str(round(100.0 * win_perc_trump, 2)) + r'%' + '\n' \
                          + '#runs=' + str(runs) \
                          + ', bias=' + str(round(bias, 1)) \
                          + ', deviation=' + str(round(deviation, 1)) \
                          + ', correlation=' + str(round(correlation, 2))
    return return_string


def generate_elector_title(trump_percentage, tie_percentage, runs, bias, deviation, correlation):
    return_string = 'Win Trump=' + str(round(100.0 * trump_percentage, 2)) + r'%' \
                                 + ', Tie=' + str(round(100.0 * tie_percentage, 2)) + r'%' + '\n' \
                                 + '#runs=' + str(runs) \
                                 + ', bias=' + str(round(bias, 1)) \
                                 + ', deviation=' + str(round(deviation, 1)) \
                                 + ', correlation=' + str(round(correlation, 2))
    return return_string


def plot_state(state: str,
               spread_outcome_array: np.ndarray,
               state_title: str,
               file_name_addon: str,
               save_flag: bool = False,
               show_flag: bool = False):
    # the histogram of the data
    plt.hist(spread_outcome_array, 50, density=True, facecolor='g', alpha=0.75)
    # print(n, bins, patches)  # Monkey patch...
    plt.xlabel('Spread')
    plt.ylabel('Probability')
    plt.title(state_title)
    plt.xlim(-100, 100)
    plt.ylim(0, 0.15)
    plt.grid(True)
    # plt.figure(figsize=(4.5, 2.5))
    if save_flag:
        plt.savefig('Output//Figures//' + state + '_spread_' + file_name_addon + '.png')
    if show_flag:
        plt.show()
    plt.close()


def plot_elector_outcome(total_electors_trump: np.ndarray,
                         elector_title: str,
                         file_name_addon: str,
                         save_flag: bool = False,
                         show_flag: bool = True):
    plt.hist(total_electors_trump, 50, density=True, facecolor='g', alpha=0.75)
    # print(n, bins, patches)  # Monkey patch...
    plt.xlabel('Electors Trump')
    plt.ylabel('Probability')
    plt.title(elector_title)
    plt.xlim(0, 538)
    plt.ylim(0, 0.02)
    plt.grid(True)
    # plt.figure(figsize=(4.5, 2.5))
    if save_flag:
        plt.savefig('Output//Figures//electors_trump_' + file_name_addon + '.png')
    if show_flag:
        plt.show()
