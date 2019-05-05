import dask.dataframe as dd
import pandas as pd
from luigi import Parameter, Task, LocalTarget, DateParameter
from pset_utils.luigi.dask.target import ParquetTarget
from pset_utils.luigi.task import TargetOutput

from ice.utils.PostgresCreate import get_connection
from redis_cache.rediscache import RedisCache


class GetClientMetaData(Task):
    client = Parameter()
    run_date = DateParameter()

    def run(self):
        df_metadata = pd.read_sql("SELECT {} from {} where client_id='{}'".format('*', 'iced.client', self.client),
                                  con=get_connection())
        df_metadata = df_metadata.set_index('client_id')
        redis_cache = RedisCache()
        client_key = 'client_' + self.client + '_metadata'
        redis_cache.store_pickle('dataframe', client_key, df_metadata.to_msgpack(compress='zlib'))

        with self.output().open('w') as f:
            df_metadata.to_csv(f)

    @property
    def root_path(self):
        return 'data/client- {}/run_date- {}/metadata/client_metadata.csv'.format(self.client, self.run_date)

    def output(self):
        return LocalTarget(self.root_path)


class GetClientHoldingsFactData(Task):
    client = Parameter()
    run_date = DateParameter()

    def requires(self):
        return GetClientMetaData(client=self.client, run_date=self.run_date)

    output = TargetOutput('data/', target_class=ParquetTarget)

    def run(self):
        redis_cache = RedisCache()
        client_key = 'client_' + self.client + '_metadata'
        df_c = pd.read_msgpack(redis_cache.get_pickle('dataframe',client_key))

        fund_id = df_c['fund_id'].to_list()
        print(fund_id)
        df_p = pd.read_sql("SELECT {} from {} where client_id='{}' and fund_id in {}".format('*', 'iced.position', self.client,tuple(fund_id)),
                           con=get_connection())
        df = dd.from_pandas(df_p, chunksize=1000)
        self.output().write_dask(df)


class GetSecurityMasterDimension(Task):
    run_date = DateParameter()

    def run(self):
        redis_cache = RedisCache()
        df_dimension = pd.read_sql(
            "SELECT {} from {}".format('*', 'iced.master'),
            con=get_connection())
        sec_master_key = 'client_' + self.run_date.strftime('%Y-%m-%d') + '_sec_master_dimension'
        redis_cache.store_pickle('dataframe', sec_master_key,
                                 df_dimension.to_msgpack(compress='zlib'))

        print('data stored in redis')
        with self.output().open('w') as f:
            df_dimension.to_csv(f)

    @property
    def root_path(self):
        return '{}/{}/{}/abc.csv'.format('data', 'security_master', self.run_date)

    def output(self):
        return LocalTarget(self.root_path)

