import deploy_utils

ALL_JOBS = ["mapreduce"]

def get_mapreduce_service_config(args):
  args.mapreduce_config = deploy_utils.get_service_config(args)

def install(args):
  get_mapreduce_service_config(args)
  deploy_utils.install_service(args, "mapreduce", args.mapreduce_config, "hadoop")

def bootstrap_job(args, host, job_name, host_id, instance_id, cleanup_token):
  deploy_utils.bootstrap_job(args, "hadoop", "mapreduce",
      args.mapreduce_config, host, job_name, instance_id, cleanup_token, '0')
  start_job(args, host, job_name, host_id, instance_id)

def bootstrap(args):
  get_mapreduce_service_config(args)
  cleanup_token = deploy_utils.confirm_bootstrap("mapreduce", args.mapreduce_config)

  for job_name in args.job or ALL_JOBS:
    hosts = args.mapreduce_config.jobs[job_name].hosts
    args.task_map = deploy_utils.parse_args_host_and_task(args, hosts)
    for host_id in args.task_map.keys() or hosts.keys():
      for instance_id in args.task_map.get(host_id) or range(hosts[host_id].instance_num):
        instance_id = -1 if not deploy_utils.is_multiple_instances(host_id, hosts) else instance_id
        bootstrap_job(args, hosts[host_id].ip, job_name, host_id, instance_id, cleanup_token)

def start_job(args, host, job_name, host_id, instance_id):
  config_files = {}
  start_script = ""
  http_url = deploy_utils.get_http_service_uri(host,
    args.mapreduce_config.jobs[job_name].base_port, instance_id)
  deploy_utils.start_job(args, "hadoop", "mapreduce", args.mapreduce_config,
      host, job_name, instance_id, start_script, http_url, **config_files)

def start(args):
  if not args.skip_confirm:
    deploy_utils.confirm_start(args)
  get_mapreduce_service_config(args)

  for job_name in args.job or ALL_JOBS:
    hosts = args.mapreduce_config.jobs[job_name].hosts
    args.task_map = deploy_utils.parse_args_host_and_task(args, hosts)
    for host_id in args.task_map.keys() or hosts.keys():
      for instance_id in args.task_map.get(host_id) or range(hosts[host_id].instance_num):
        instance_id = -1 if not deploy_utils.is_multiple_instances(host_id, hosts) else instance_id
        start_job(args, hosts[host_id].ip, job_name, host_id, instance_id)


if __name__ == '__main__':
  test()
