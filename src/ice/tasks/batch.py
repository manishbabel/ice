from luigi import WrapperTask, Parameter, DateParameter
from pset_utils.luigi.dask.target import ParquetTarget
from pset_utils.luigi.task import TargetOutput

from ice.tasks.etl_flow import GetSecurityMasterDimension, GetClientHoldingsFactData
from redis_cache.rediscache import RedisCache
import pandas as pd


class ExecuteClientBatch(WrapperTask):
    client = Parameter()
    run_date = DateParameter()

    def requires(self):
        return {
            'client_holdings': GetClientHoldingsFactData(run_date=self.run_date, client=self.client),
            'security_reference': GetSecurityMasterDimension(run_date=self.run_date)
        }

    output = TargetOutput('data/', target_class=ParquetTarget)

    def run(self):
        redis_cache = RedisCache()
        sec_master_key = 'client_' + self.run_date.strftime('%Y-%m-%d') + '_sec_master_dimension'
        df_dimension = pd.read_msgpack(redis_cache.get_pickle('dataframe', sec_master_key))
        numcols = ["mktval_btl"]
        df_fact = self.input()['client_holdings'].read_dask()
        df_fact = df_fact.astype(dtype=dict.fromkeys(numcols, 'float64'))
        df_fact = df_fact.merge(df_dimension, on='asset_id', how='left')
        self.output().write_dask(df_fact)
