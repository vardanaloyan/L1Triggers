from CRABClient.UserUtilities import config
config = config()

config.General.requestName = ''
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.outputFiles = ['L1Ntuple.root']
#config.JobType.outputFiles = ['l1Ntuple_RAW2DIGI.root']
config.JobType.psetName = 'data.py'

config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = ''
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'
#config.Data.unitsPerJob = 10
config.Data.splitting = 'Automatic'
config.Data.lumiMask = '/afs/cern.ch/user/a/aloyan/public/json_DCSONLY.txt'
config.Data.publication = False
config.Data.outputDatasetTag = 'CRAB3_Analaysis'

config.Site.storageSite = 'T2_RU_JINR'

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    for dataset in [
                    '/EphemeralZeroBias1/Run2018D-v1/RAW',
                   ]:
        config.Data.inputDataset = dataset
        config.General.requestName = dataset.split('/')[2]
        crabCommand('submit', config = config)
