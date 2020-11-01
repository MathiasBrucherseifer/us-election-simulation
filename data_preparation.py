import numpy as np
from data_loader import get_last_election_data, get_state_polls, parse_rcp_spread
from scipy.linalg import lstsq
import matplotlib.pyplot as plt
from datetime import datetime
from dataclasses import dataclass
import logging


@dataclass
class StateParameters:
    state: str
    spreads: [int]
    mu_original: float
    mu: float
    sigma: float
    number_of_polls: int
    number_of_electors: int
    timestamp: datetime


def add_bias(mu, bias_factor, p):
    bias = p[0] + (p[1] - 1.0) * mu + p[2] * mu * mu
    return mu + bias_factor * bias


def plot_bias_function(x, y, p):
    plt.plot(x, y, 'o', label='data')
    xx = np.linspace(-40, 40, 1000)
    yy = p[0] + p[1] * xx + p[2] * xx**2
    plt.plot(xx, yy, label='least squares fit, $y = a + bx^2$')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(framealpha=1, shadow=True)
    plt.grid(alpha=0.25)
    plt.show()


def bias_fit(static_df):
    df_clean = static_df[static_df['Forecasts 2016'].notnull()]
    x = np.array([float(a.replace(',', '.')) for a in df_clean['Forecasts 2016'].to_list()])
    y = np.array([float(a.replace(',', '.')) for a in df_clean['Spread 2016'].to_list()])
    M = x[:, np.newaxis]**[0, 1, 2]  # fit a quadratic function
    returntuple = lstsq(M, y)
    return returntuple[0]  # p is a list containing the parameters of the quadratic function fit p[0] + p[1]*x + p[2]*x^2


def get_state_parameters(bias_factor: float, deviation: float = 10.0, p: [float] = []):  # -> dict[str, StateParameters]:
    # Load static data
    static_df = get_last_election_data()
    all_states = list(static_df['State'].unique())

    # Fit a bias function to the Forecast and Outcomes of 2016
    if len(p) < 3:  # Do this only once, there seems to be a bug when this is called multiple times...
        p = bias_fit(static_df)
        logging.info('Bias function fit')

    # Plot bias function fit on 2016 data
    # plot_bias_function(x,y,p)

    # Load State polls
    state_polls = get_state_polls()

    # Populate the state parameters
    state_parameters_dict = {}
    for state in all_states:
        state_df = static_df[static_df['State'] == state]
        number_of_electors = int(state_df['Electors'].iloc[0])
        polls_for_state = [poll for poll in state_polls if poll['state'] == state]
        if len(polls_for_state) > 0:
            spread_array = np.array([parse_rcp_spread(poll['result']) for poll in polls_for_state])
        else:
            spread_array = np.array([state_df['Forecast 2020 (static)'].iloc[0]])
        # The mean of the spread distribution is just the average of all polls or a static Forecast for 2020 (from .csv) if no polls are available
        mu_original = np.average(spread_array)
        mu = add_bias(mu_original, bias_factor, p)
        # The standard deviation of the spread distribution is altered with two additional values [mu+dev,mu-dev]. This should compensate for low statistics
        sigma = np.std(np.append(spread_array, np.array([mu - deviation, mu + deviation])))
        # state_parameters_dict.append([state, spread_array, mu_original, mu, sigma, len(spread_array), number_of_electors, datetime.now()])
        state_parameters_dict[state] = StateParameters(state=state,
                                                       spreads=spread_array,
                                                       mu_original=mu_original,
                                                       mu=mu,
                                                       sigma=sigma,
                                                       number_of_polls=len(spread_array),
                                                       number_of_electors=number_of_electors,
                                                       timestamp=datetime.now())
        logging.info('Populated parameters for ' + state)

    # Plot bias function on 2020 data
    # mu_orig_array = [s.mu_original for s in state_parameters]
    # mu_array = [s.mu for s in state_parameters]
    # plot_bias_function(mu_orig_array,mu_array,p)
    return p, state_parameters_dict
