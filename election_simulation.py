from random import random
from scipy.stats import norm


def simulate_election_run(state_parameters_dict,  # : dict(str, StateParameters),
                          correlation: float,
                          run: int) -> [[]]:
    state_result = []
    uniform_rv_correlated = random()
    for state, state_parameters in state_parameters_dict.items():
        uniform_rv = random()
        rv = (1.0 - correlation) * uniform_rv + correlation * uniform_rv_correlated
        spread_outcome = norm(loc=state_parameters.mu, scale=state_parameters.sigma).ppf(rv)
        spread_outcome = -100.0 if spread_outcome < -100.0 else (100.0 if spread_outcome > 100.0 else spread_outcome)
        winner = 'Biden' if spread_outcome > 0.0 else 'Trump'
        electors_trump = state_parameters.number_of_electors if winner == 'Trump' else 0
        electors_biden = state_parameters.number_of_electors if winner == 'Biden' else 0
        state_result.append([run, state, uniform_rv, uniform_rv_correlated, spread_outcome, electors_trump, electors_biden, winner])
    return state_result


def evaluate_election_run(simulation_results_df, run):
    run_df = simulation_results_df[simulation_results_df['simulation_run'].astype(int) == run]
    electors_trump = run_df['electors_trump'].astype(int).sum()
    electors_biden = run_df['electors_biden'].astype(int).sum()
    assert(electors_trump + electors_biden == 538)
    return electors_trump
