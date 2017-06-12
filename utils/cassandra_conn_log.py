from cassandra.cluster import Cluster
from cassandra.query import dict_factory

class SimpleClient:
   session = None

   def connect(self, nodes):
       cluster = Cluster(nodes)
       metadata = cluster.metadata
       self.session = cluster.connect()

   def close(self):
       self.session.cluster.shutdown()
       self.session.shutdown()


def setup_log_connection():
   client = SimpleClient()
   client.connect(['ec2-52-52-36-108.us-west-1.compute.amazonaws.com',
                  'ec2-52-9-200-255.us-west-1.compute.amazonaws.com',
                  'ec2-52-8-150-215.us-west-1.compute.amazonaws.com'])
   session = client.session
   session.row_factory = dict_factory
   session.set_keyspace('dse_perf')
   return session
