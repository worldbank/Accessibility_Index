import dask
import coiled
from dask.distributed import Client, LocalCluster, Lock, wait
from dask.utils import SerializableLock
import dask.dataframe as dd

def config_env(env_name="ais"):
    software_env_name = env_name
    coiled.create_software_environment(
        name=software_env_name,
        #container="mrmaksimize/prefect-coiled-env:latest",
       pip=[
            "Fiona==1.8.19",
            "rasterio==1.2.3",
            "s3fs==2021.5.0",
            "xarray==0.18.2",
            "xarray-spatial==0.2.2",
            "rioxarray==0.4.0",
            "dask==2021.7.0",
            "distributed==2021.7.0",
            "scikit-image==0.18.2"
        ],
        backend_options={"region": "us-east-1"})


    return True



def get_dask_client(cluster_type = 'local', n_workers = 8, processes=True, threads_per_worker=1, scheduler_mem_gb = 8, worker_mem_gb = 8):


    if cluster_type == 'local':
        try:
            client = Client('127.0.0.1:8786')
        except:   
            cluster = LocalCluster(n_workers = n_workers, 
                               processes=processes, 
                               threads_per_worker=threads_per_worker, 
                               scheduler_port=8786)

            client = Client(cluster)
    


    else:
        software = "riox"
        config_env(software)
        cluster = coiled.Cluster(
            name='riox-cluster',
            #configuration=f"ais-dev",
            n_workers=n_workers,
            scheduler_cpu = threads_per_worker,
            scheduler_memory = f"{str(scheduler_mem_gb)} GiB",
            worker_cpu = threads_per_worker,
            worker_memory=f"{str(worker_mem_gb)} GiB",
            software = f"mrmaksimize/{software}"
            
            
        )

        client = Client(cluster) 
        
    client.restart()


    return client