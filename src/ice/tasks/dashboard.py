import dask.dataframe as dd
import matplotlib.pyplot as plt
import seaborn as sns
from luigi import Task, DateParameter
from pset_utils.luigi.dask.target import ParquetTarget
from pset_utils.luigi.task import TargetOutput
import pandas as pd
from ice.tasks.batch import ExecuteClientBatch


class ExecuteDashboard(Task):
    pd.options.display.float_format = '{:20,.2f}'.format
    run_date = DateParameter()

    output = TargetOutput('data/dashboard', target_class=ParquetTarget)

    def requires(self):
        return {
            'client_5294': self.clone(ExecuteClientBatch, run_date=self.run_date, client='JP Morgan'),
            'client_6000': self.clone(ExecuteClientBatch, run_date=self.run_date, client='Visa'),
            'client_7000': self.clone(ExecuteClientBatch, run_date=self.run_date, client='Chase'),
            'client_8000': self.clone(ExecuteClientBatch, run_date=self.run_date, client='BOFA'),
            'client_9000': self.clone(ExecuteClientBatch, run_date=self.run_date, client='AMEX'),
        }

    def run(self):

        for i, key in enumerate(self.input()):
            if i == 0:
                df_calc = self.input()[key].read_dask().groupby(by='client_id').mktval_btl.sum().round(2)  .to_frame()
            else:
                df_calc2 = self.input()[key].read_dask().groupby(by='client_id').mktval_btl.sum().round(2).to_frame()
                df_calc = dd.concat([df_calc, df_calc2], interleave_partitions=True).compute()
        df_calc = df_calc.assign(asof=str(self.run_date))
        df_calc = df_calc.reset_index()
        numcols = ["mktval_btl"]
        df_calc = df_calc.astype(dtype=dict.fromkeys(numcols, 'float64'))

        df_final = dd.from_pandas(df_calc, chunksize=1000)
        self.output().write_dask(df_final)
        self.draw_plot(df_calc)

    def draw_plot(self, df_calc):
        sns.set(style="whitegrid")
        sns.lineplot(x='client_id', y='mktval_btl', data=df_calc,color="coral", label="Market Value")
        plt.show()
