import os
import plot
from agent.ddpg_her_continuous import HindsightDDPGAgent
from kuka_reach.trainer import Trainer

seeds = [11, 22, 33, 44, 55, 66]
seed_returns = []
seed_success_rates = []
path = os.path.dirname(os.path.realpath(__file__))

for seed in seeds:

    seed_path = path + '/seed' + str(seed)
    trainer = Trainer(env="KukaReachRenderSparseEnv-v0",
                      agent=HindsightDDPGAgent,
                      hindsight=True,
                      prioritised=True,
                      seed=seed,
                      path=seed_path)

    seed_return, seed_success_rate = trainer.run(test=False, load_network_ep=100)
    seed_returns.append(seed_return)
    seed_success_rates.append(seed_success_rate)
    trainer.env.close()

return_statistic = plot.get_mean_and_deviation(seed_returns, save_data=True,
                                               file_name=os.path.join(path, 'return_statistic.json'))
plot.smoothed_plot_mean_deviation(path + '/returns.png', return_statistic,
                                  x_label='Cycle', y_label='Average returns')

success_rate_statistic = plot.get_mean_and_deviation(seed_success_rates, save_data=True,
                                                     file_name=os.path.join(path, 'success_rate_statistic.json'))
plot.smoothed_plot_mean_deviation(path + '/success_rates.png', success_rate_statistic,
                                  x_label='Cycle', y_label='Success rates')