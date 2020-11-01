# TODO:
# - Parallelization


from election_simulation import simulate_election_run, evaluate_election_run
from data_preparation import get_state_parameters
from plotting import plot_state, plot_elector_outcome, generate_file_name_addon, generate_state_title, generate_elector_title
import logging
# import multiprocessing as mp
import pandas as pd
import numpy as np


NUMBER_OF_RUNS = 10000
BIAS_FACTOR = 0.5
DEVIATION = 15.0
CORRELATION = 0.5
SAVE_FLAG = True
SHOW_FLAG = False
# CPU_COUNT = 1  # mp.cpu_count()


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(filename)s | %(message)s')


def build_simulation_df(simulation_results):
    return pd.DataFrame(np.array(simulation_results),
                        columns=['simulation_run', 'state', 'uniform_rv', 'uniform_rv_correlated', 'spread_outcome',
                                 'electors_trump', 'electors_biden', 'winner']
                        )


def simulate_election(state_parameters_dict, correlation):
    simulation_results_list = []
    for run in range(NUMBER_OF_RUNS):
        simulation_results_list.append(simulate_election_run(state_parameters_dict, correlation, run))
        if (run + 1) % 100 == 0:
            logging.info('Run ' + str(run + 1) + ' simulated')
    return simulation_results_list


def evaluate_election(simulation_results_df):
    total_electors_trump = []
    for run in range(NUMBER_OF_RUNS):
        total_electors_trump.append(evaluate_election_run(simulation_results_df, run))
        if (run + 1) % 100 == 0:
            logging.info('Run ' + str(run + 1) + ' evaluated')
    return total_electors_trump


def main():
    logging.info('Running with bias_factor=' + str(round(BIAS_FACTOR, 1)) + ' and correlation=' + str(round(CORRELATION, 1)))

    # Get state parameters
    p = []
    p, state_parameters_dict = get_state_parameters(BIAS_FACTOR, DEVIATION, p)

    # Run simulation
    logging.info('Start the simulation: Simulate each state ' + str(NUMBER_OF_RUNS) + ' times')
    simulation_results_list = simulate_election(state_parameters_dict, CORRELATION)
    # logging.info('Parallelize simulation with ' + str(CPU_COUNT) + ' CPUs')
    # pool = mp.Pool(CPU_COUNT)
    # simulation_results_list = [pool.apply(simulate_election_run, args=(state_parameters_dict, CORRELATION, run,)) for run in range(NUMBER_OF_RUNS)]
    # pool.close()
    # logging.info('Simulation finished with ' + str(CPU_COUNT) + ' CPUs')

    simulation_results = [item for sublist in simulation_results_list for item in sublist]
    simulation_results_df = build_simulation_df(simulation_results)

    file_name_addon = generate_file_name_addon(NUMBER_OF_RUNS, BIAS_FACTOR, DEVIATION, CORRELATION)

    if False:
        filename = 'Output//Data//simulation_results_' + file_name_addon + '.csv'
        logging.info('Save data in file: ' + filename)
        simulation_results_df.to_csv(filename)

    # Plot spread distribution per State
    for state, state_parameters in state_parameters_dict.items():
        state_df = simulation_results_df[simulation_results_df['state'] == state]
        win_perc_trump = float(len(state_df[state_df['winner'] == 'Trump'])) / float(NUMBER_OF_RUNS)
        state_title = generate_state_title(state, state_parameters.mu, state_parameters.sigma, win_perc_trump,
                                           NUMBER_OF_RUNS, BIAS_FACTOR, DEVIATION, CORRELATION)
        plot_state(state=state,
                   spread_outcome_array=state_df['spread_outcome'].to_numpy(float),
                   state_title=state_title,
                   file_name_addon=file_name_addon,
                   show_flag=SHOW_FLAG,
                   save_flag=SAVE_FLAG)
        logging.info(state + ': Plot finished')

    # Electoral vote distribution
    logging.info('Start the evaluation: Sum the electors over all states for ' + str(NUMBER_OF_RUNS) + ' runs')
    total_electors_trump = evaluate_election(simulation_results_df)
    # logging.info('Parallelize evaluation with ' + str(CPU_COUNT) + ' CPUs')
    # pool = mp.Pool(CPU_COUNT)
    # total_electors_trump = [pool.apply(evaluate_election_run, args=(simulation_results_df, run,)) for run in range(NUMBER_OF_RUNS)]
    # pool.close()
    # logging.info('Evaluation finished with ' + str(CPU_COUNT) + ' CPUs')

    # Calculate win percentages
    logging.info('Calculate win percentages')
    number_of_trump_wins = sum([electors_trump >= 270 for electors_trump in total_electors_trump])
    number_of_ties = sum([electors_trump == 269 for electors_trump in total_electors_trump])
    number_of_biden_wins = sum([electors_trump < 269 for electors_trump in total_electors_trump])
    assert(number_of_trump_wins + number_of_ties + number_of_biden_wins == NUMBER_OF_RUNS)
    win_percentage_trump = float(number_of_trump_wins) / float(NUMBER_OF_RUNS)
    tie_percentage = float(number_of_ties) / float(NUMBER_OF_RUNS)

    # Plot electoral vote distribution
    logging.info('Plot the final distribution')
    elector_title = generate_elector_title(win_percentage_trump, tie_percentage, NUMBER_OF_RUNS, BIAS_FACTOR, DEVIATION, CORRELATION)
    plot_elector_outcome(total_electors_trump=total_electors_trump,
                         elector_title=elector_title,
                         file_name_addon=file_name_addon,
                         show_flag=SHOW_FLAG,
                         save_flag=SAVE_FLAG)


if __name__ == "__main__":
    main()
