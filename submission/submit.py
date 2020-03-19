###!/usr/bin/python

import optparse
import ConfigParser
import os
import sys
import shutil
import subprocess


class TaskConfig:
    def __init__(self, taskName, cfgfile):
        print 'TN: {}'.format(taskName)
        self.task_name = taskName

        self.version = cfgfile.get('Common', 'version')
        self.cmssw_config = cfgfile.get('Common', 'cmssw_config')
        self.crab = False

        for task_opt in cfgfile.options(self.task_name):
            if task_opt == 'crab':
                self.crab = cfgfile.getboolean(taskName, task_opt)
            else:
                setattr(self, task_opt, cfgfile.get(taskName, task_opt))

        self.task_dir = '{}/{}/{}'.format(cfgfile.get('Common', 'name'),
                                          cfgfile.get('Common', 'version'),
                                          taskName)
        self.output_dir_base = cfgfile.get('Common', 'output_dir_base')
        self.output_dir = '{}/{}/{}/{}'.format(cfgfile.get('Common', 'output_dir_base'),
                                               self.task_name,
                                               cfgfile.get('Common', 'mode'),
                                               self.version)
        self.ncpu = cfgfile.get('Common', 'ncpu')
        self.output_file_name = cfgfile.get('Common', 'output_file_name')

    def __str__(self):
        return 'task-name {}: version {}'.format(self.task_name, self.version)


def getLSs(file_name):
    from subprocess import Popen, PIPE
    lumis = []
    p = Popen('edmFileUtil --eventsInLumis {}'.format(file_name),
              stdout=PIPE,
              shell=True)
    pipe = p.stdout.read()
    lines = pipe.split('\n')
    for line in lines[4:-2]:
        lumis.append(line.split()[1])
    return lumis


def splitFiles(files, splitting_mode, splitting_granularity):
    split_files = []
    split_logic = []
    if splitting_mode == 'file_based':
        size = int(splitting_granularity)
        split_files = [files[i:i+size] for i in range(0, len(files), size)]
    elif splitting_mode == 'lumi_based':
        for file_name in files:
            # print file_name
            file_lss = getLSs(file_name)
            for ls in file_lss:
                split_files.append([file_name])
                logic = '1:{}-1:{}'.format(ls, ls)
                split_logic.append(logic)
    elif splitting_mode == 'EventAwareLumiBased' or splitting_mode == 'Automatic':
        pass
    else:
        print '[submission] Splitting-Mode: {} is not implemented! Exiting...'.format(splitting_mode)
        sys.exit(6)
    return split_files, split_logic


def getFilesForDataset(dataset, site=None):
    import time
    from subprocess import Popen, PIPE
    options = ''
    eC = 5
    count = 0
    site_query = ''
    if site is not None:
        site_query = ' and site={}'.format(site)
    query = 'dasgoclient {} --query "file dataset={} {}"'.format(options, dataset, site_query)

    # print query
    while (eC != 0 and count < 3):
        if count != 0:
            print 'Sleeping, then retrying DAS'
            time.sleep(100)
        p = Popen(query,
                  stdout=PIPE,
                  shell=True)
        pipe = p.stdout.read()
        tupleP = os.waitpid(p.pid, 0)
        eC = tupleP[1]
        count = count+1
        if eC == 0:
            print "DAS succeeded after", count, "attempts", eC
            return [filename for filename in pipe.split('\n') if '.root' in filename]
        else:
            print "DAS failed 3 times- I give up"
            return []



def getJobParams(mode, task_conf):
    params = {}
    if mode == 'NTP' or mode == 'L1IN' or mode == 'SIMDIGI':
        input_files = []
        if task_conf.input_directory != '' and task_conf.input_directory != 'None' and not task_conf.crab:
            print 'Reading inpout files from directory: {}'.format(task_conf.input_directory)
            input_files = ['root://eoscms.cern.ch/'+os.path.join(task_conf.input_directory, file_name) for file_name in os.listdir(task_conf.input_directory) if file_name.endswith('.root')]

        if task_conf.input_dataset != '' and task_conf.input_dataset != 'None' and not task_conf.crab:
            print 'Reading inpout files from dataset: {}'.format(task_conf.input_dataset)
            input_files = getFilesForDataset(task_conf.input_dataset, site='T2_CH_CERN')
        # print input_files

        split_files, split_logic = splitFiles(input_files, task_conf.splitting_mode, task_conf.splitting_granularity)
        n_jobs_max = len(split_files)
        n_jobs = n_jobs_max
        if(hasattr(task_conf, 'max_njobs')):
            n_jobs = min(n_jobs_max, task_conf.max_njobs)

        if not task_conf.crab:
            print 'preparing batch submission:'
            print '  # of files: {}'.format(len(input_files))
            print '  # of jobs: {}'.format(n_jobs)
        else:
            print 'preparing crab submission'

        max_events = -1
        if(hasattr(task_conf, 'max_events')):
            max_events = task_conf.max_events
        split_pu_files = []
        if(hasattr(task_conf, 'pu_dataset')):
            pu_files = getFilesForDataset(dataset=task_conf.pu_dataset, site=None)
            pu_splitting_granularity = min(100,  int(len(pu_files)/n_jobs))
            print "# of PU files: {}".format(len(pu_files))
            print "# PU file per job: {}".format(pu_splitting_granularity)
            split_pu_files, split_pu_logic = splitFiles(files=pu_files,
                                                        splitting_mode='file_based',
                                                        splitting_granularity=pu_splitting_granularity)
            print len(split_pu_files)
        # the first 2 are compulsory for all modes
        params['NJOBS'] = n_jobs
        params['INFILES'] = split_files
        params['PUFILES'] = split_pu_files
        params['SEEDS'] = range(0, n_jobs)
        params['SPLIT'] = split_logic
        params['TEMPL_NEVENTS'] = max_events
        params['TEMPL_TASKDIR'] = task_conf.task_dir
        params['TEMPL_TASKCONFDIR'] = '{}/conf'.format(task_conf.task_dir)
        params['TEMPL_ABSTASKCONFDIR'] = os.path.join(os.environ["PWD"], params['TEMPL_TASKCONFDIR'])
        params['TEMPL_OUTFILE'] = task_conf.output_file_name
        params['TEMPL_OUTDIR'] = task_conf.output_dir
        params['TEMPL_JOBFLAVOR'] = task_conf.job_flavor
        params['TEMPL_NCPU'] = task_conf.ncpu
        params['TEMPL_SPLITGRANULARITY'] = task_conf.splitting_granularity
        params['TEMPL_SPLITTINGMODE'] = task_conf.splitting_mode
        params['TEMPL_REQUESTNAME'] = task_conf.task_name
        params['TEMPL_INPUTDATASET'] = task_conf.input_dataset
        params['TEMPL_DATASETTAG'] = '{}_{}'.format(task_conf.task_name, task_conf.version)
        params['TEMPL_CRABOUTDIR'] = task_conf.output_dir_base.split('/eos/cms')[1].replace('/cmst3/', '/group/cmst3/')


    else:
        print 'Mode: {} is not implemented! Exiting...'.format(mode)
        sys.exit(4)
    return params


def formatFileList(input_files):
    input_file_names = ['\'{}\''.format(file_name) for file_name in input_files]
    return ',\n'.join(input_file_names)


def createJobConfig(mode, params):
    custom_template_filename = 'templates/jobCustomization_{}_cfg.py'.format(mode)
    default_template_filename = 'templates/jobCustomization_{}_cfg.py'.format('DEFAULT')
    if not os.path.isfile(custom_template_filename):
        custom_template_filename = default_template_filename
    for job_idx in range(0, params['NJOBS']):
        custom_template_file = open(custom_template_filename)
        custom_template = custom_template_file.read()
        custom_template_file.close()
        # input files
        file_list = formatFileList(params['INFILES'][job_idx])
        custom_template = custom_template.replace('TEMPL_INFILES', file_list)
        # pu files

        if len(params['PUFILES']) != 0:
            pu_file_list = formatFileList(params['PUFILES'][job_idx])
            custom_template = custom_template.replace('TEMPL_PUFILELIST', pu_file_list)

        if len(params['SPLIT']) != 0:
            job_logic = params['SPLIT'][job_idx]
            custom_template += 'process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange("{}")\n'.format(job_logic)

        custom_template = custom_template.replace('TEMPL_SEED', str(params['SEEDS'][job_idx]))

        templs_keys = [key for key in params.keys() if 'TEMPL_' in key]
        for key in templs_keys:
            custom_template = custom_template.replace(key, str(params[key]))

        # we now check that all templated arguments have been addressed
        if('TEMPL_') in custom_template:
            print "*** ERROR: not all the templated arguments of file {} have been addressed!".format(custom_template_filename)
            for line in custom_template.split('\n'):
                if 'TEMPL_' in line:
                    print line
            sys.exit(20)

        job_config_file = open(os.path.join(params['TEMPL_TASKCONFDIR'], 'job_config_{}.py'.format(job_idx)), 'w')
        job_config_file.write(custom_template)
        job_config_file.close()


def createCondorConfig(mode, params):
    condor_template_name = 'templates/condorSubmit_{}.sub'.format(mode)
    default_template_name = 'templates/condorSubmit_{}.sub'.format('DEFAULT')
    if not os.path.isfile(condor_template_name):
        condor_template_name = default_template_name
    condor_template_file = open(condor_template_name)
    condor_template = condor_template_file.read()
    condor_template_file.close()
    condor_template = condor_template.replace('TEMPL_NJOBS', str(params['NJOBS']))
    templs_keys = [key for key in params.keys() if 'TEMPL_' in key]
    for key in templs_keys:
        condor_template = condor_template.replace(key, str(params[key]))

    condor_file = open(os.path.join(params['TEMPL_TASKCONFDIR'], 'condorSubmit.sub'), 'w')
    condor_file.write(condor_template)
    condor_file.close()


def createJobExecutable(mode, params):
    run_template_name = 'templates/run_{}.sh'.format(mode)
    default_template_name = 'templates/run_{}.sh'.format('DEFAULT')
    if not os.path.isfile(run_template_name):
        run_template_name = default_template_name
    shutil.copy(run_template_name, '{}/run.sh'.format(params['TEMPL_TASKCONFDIR']))
    shutil.copy('templates/copy_files.sh', '{}/copy_files.sh'.format(params['TEMPL_TASKDIR']))
    os.chmod(os.path.join(params['TEMPL_TASKDIR'], 'copy_files.sh'),  0754)
    params_file = open(os.path.join(params['TEMPL_TASKCONFDIR'], 'params.sh'), 'w')
    templs_keys = [key for key in params.keys() if 'TEMPL_' in key]
    for key in templs_keys:
        params_file.write('{}={}\n'.format(key.split('_')[1], str(params[key])))
    params_file.close()


def createCrabConfig(mode, params):
    crab_template_name = 'templates/crab_{}.py'.format(mode)
    default_template_name = 'templates/crab_{}.py'.format('DEFAULT')
    if not os.path.isfile(crab_template_name):
        crab_template_name = default_template_name
    crab_template_file = open(crab_template_name)
    crab_template = crab_template_file.read()
    crab_template_file.close()
    templs_keys = [key for key in params.keys() if 'TEMPL_' in key]
    for key in templs_keys:
        crab_template = crab_template.replace(key, str(params[key]))

    crab_file = open(os.path.join(params['TEMPL_TASKCONFDIR'], 'crab.py'), 'w')
    crab_file.write(crab_template)
    crab_file.close()


def createTaskSetup(task_config, config_file):
    mode = config_file.get('Common', 'mode')
    pwd = os.environ["PWD"]
    if not os.path.exists(task_config.task_dir):
        print "   creating task directory {}".format(task_config.task_dir)
        os.makedirs(task_config.task_dir)
        os.mkdir(task_config.task_dir+'/conf/')
        os.mkdir(task_config.task_dir+'/logs/')

    if not os.path.exists(task_config.output_dir):
        try:
            os.makedirs(task_config.output_dir)
        except:
            print '   ERROR: output dir {} doesn\'t exist: please create it first!'.format(task_config.output_dir)
            print "Unexpected error:", sys.exc_info()[0]
            print sys.exit(2)

    shutil.copy(task_config.cmssw_config, '{}/conf/input_cfg.py'.format(task_config.task_dir))
    shutil.copy("process_pickler.py", '{}/conf/process_pickler.py'.format(task_config.task_dir))

    params = getJobParams(mode, task_config)
    if not task_config.crab:
        createJobConfig(mode, params)
        createCondorConfig(mode, params)
        createJobExecutable(mode, params)
    else:
        createCrabConfig(mode, params)
    return


def submitTask(sub_name, task_config):
    submit_cmd = 'condor_submit {}/conf/condorSubmit.sub -batch-name {}_{}'.format(task_config.task_dir, sub_name, task_config.task_name)
    if task_config.crab:
        submit_cmd = 'crab submit {}/conf/crab.py'.format(task_config.task_dir)
    try:
        print subprocess.check_output(submit_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print 'Command: {} FAILED!'.format(submit_cmd)
        print e.output


def getCondorCluster(task_config):
    # clusterId = 529700
    condorLogs = [x for x in os.listdir(os.path.join(task_config.task_dir, 'logs')) if x.endswith('.log')]
    condorLogs.sort()
    clusterId = condorLogs[-1].split('.')[1]
    # print condorLogs
    return clusterId


def printStatus(clusterId):
    condor_cmd = 'condor_q {}'.format(clusterId)
    try:
        print subprocess.check_output(condor_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print 'Command: {} FAILED!'.format(condor_cmd)
        print e.output

def printWait(task_conf, clusterId):
    condor_cmd = 'condor_wait -wait 30 -status {}/logs/condor.{}.log'.format(task_conf.task_dir, clusterId)
    try:
        print subprocess.check_output(condor_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print 'Command: {} FAILED!'.format(condor_cmd)
        print e.output


def main():
    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    parser.add_option('-f', '--file', dest='CONFIGFILE', help='specify the ini configuration file')
    parser.add_option("--create", action="store_true", dest="CREATE", default=False, help="create the job configuration")
    parser.add_option("--submit", action="store_true", dest="SUBMIT", default=False, help="submit the jobs to condor")
    parser.add_option("--status", action="store_true", dest="STATUS", default=False, help="check the status of the condor tasks")

    global opt, args
    (opt, args) = parser.parse_args()

    cfgfile = ConfigParser.ConfigParser()
    cfgfile.optionxform = str

    cfgfile.read(opt.CONFIGFILE)
    sub_name = cfgfile.get('Common', 'name')
    tasks = [task.strip() for task in cfgfile.get('Common', 'tasks').split(',') if task != '']
    task_configs = []
    print tasks
    for task in tasks:
        task_configs.append(TaskConfig(task, cfgfile))

    for task_conf in task_configs:
        print task_conf

    if opt.CREATE:
        for task_conf in task_configs:
            print '-- Creating task {}'.format(task_conf.task_name)
            # 1 create local dir
            createTaskSetup(task_conf, cfgfile)
    elif opt.SUBMIT:
        for task_conf in task_configs:
            print '-- Submitting task {}'.format(task_conf.task_name)
            # 1 create local dir
            submitTask(sub_name, task_conf)
    elif opt.STATUS:
        for task_conf in task_configs:
            print '-- Status of task {}'.format(task_conf.task_name)
            clusterId = getCondorCluster(task_conf)
            printStatus(clusterId)
            printWait(task_conf, clusterId)
            print '   out dir: {}'.format(task_conf.output_dir)


if __name__ == "__main__":
    main()
