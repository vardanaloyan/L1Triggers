# Trigger Rate and Efficiency calculations

Plan

1. Rate/Pure-Rate calculation with data
2. Rate/Pure-Rate calculation with mc (All)
3. Efficiency calculations with mc (signal)


## 1. Trigger Rate calculations with data

This part was done using twiki [HowToL1TriggerMenu](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToL1TriggerMenu) documentation and consists of two steps

* Ntuple making process
* Rate calculations (based on Ntuples, built in the first step)

### 1.1 Ntuple making process

This step was done according to twiki [SWGuideL1TStage2Instructions](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TStage2Instructions) documentation

#### 1.1.1 Environment setup
Navigate to

	 ->  Environment Setup with Integration Tags -> CMSSW_11_2_0 

and setup the environment

```
cmsrel CMSSW_11_2_0
cd CMSSW_11_2_0/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline l1t-integration-CMSSW_11_2_0
git cms-merge-topic -u cms-l1t-offline:l1t-integration-v105.20.1
git cms-addpkg L1Trigger/Configuration
git cms-addpkg L1Trigger/L1TMuon
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TMuon.git L1Trigger/L1TMuon/data
git cms-addpkg L1Trigger/L1TCalorimeter
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TCalorimeter.git L1Trigger/L1TCalorimeter/data

git cms-checkdeps -A -a


scram b -j 8

```

In case if you will have git related problems you should connect your local git with remote github account by adding `ssh-key` in your lxplus's ssh configs and in github account.

Recommended GlobalTag for run2 data reprocessing is `112X_dataRun2_v7`

#### 1.1.2 Processing script generation
Navigate to

	 -> L1T Cookbook: current recipes -> Re-emulating 2018 data with the new 2018 CaloParams and conditions 
	 
Following command used to generate processing script

```
cmsDriver.py l1Ntuple -s RAW2DIGI --python_filename=data.py -n -1 --no_output --era=Run2_2018 --data --conditions=112X_dataRun2_v7 --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleRAWEMU --customise=L1Trigger/Configuration/customiseSettings.L1TSettingsToCaloParams_2018_v1_3 --filein=file:/eos/cms/store/data/Run2018D/store/data/Run2018D/ZeroBias/RAW/v1/000/325/240/00000/4E953DE3-A07E-6F45-94F4-E530035D3757.root
```
This will generate [data.py](./src/data.py) file.
Do not pay attention if the command would not execute successfully due to some networking issues. Important to have generated `data.py` file.

#### 1.1.3 Submiting crab jobs for making NTuples

For crab jobs we are using this [`Crab_TrgEff_Data.py`](./src/Crab_TrgEff_Data.py) file. 
In this configuration we are using following dataset

`/ZeroBias/Run2018D-v1/RAW`

You can find information about datasets from [CMSWEB](https://cmsweb.cern.ch/das) site.

In this configuration we are using following [`Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt`](./src/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt) file for good lumis.

You can find more json files from [here](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/).


In order to submit Crab job you should:

* `cmsenv`
* Initialize crab environment `source /cvmfs/cms.cern.ch/common/crab-setup.sh`
* `python Crab_TrgEff_Data.py`

After submitting crab jobs you can check the status using fillowing command

`crab st -d crab_projects/crab_Run2018D-v1`

If ready you can get the output using following command

`crab out -d crab_projects/crab_Run2018D-v1 --jobids 500`


#### 1.1.4 Making the list of output files

If the previous step was successfully done, You can filelist of the filenames using following [script](./src/llist).

```python
#!/usr/bin/env python3
import sys
# print(sys.argv)
if len(sys.argv) != 2:
    info_str = """
	command to execute:
		llist "<path>/<glob_pattern>"
    """
    print(info_str)
    sys.exit(1)
    
import glob
import os

for i in glob.glob(sys.argv[1]):
    print(i)

```

In my case the command was

`llist "/eos/user/a/aloyan/2021/ntuple/crab_Run2018D-v1/results/L1Ntuple_*.root" > ntuple.txt`

Below you can find [ntuple.txt](./src/ntuple.txt) file.

This was the last step of Ntuple making process. 

In the next section we would need `ntuple.txt` file to be there.

### 1.2 Rate calculations

For rate calculations we should keep using [HowToL1TriggerMenu](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToL1TriggerMenu) documentation.

We are going to use `CMSSW_11_1_5` version.

This part consists of several steps:

* Setup an environment
* Copying `ntuple.txt` into working directory
* Prescale table making
* Copying menu.xml into working directory
* Compilation
* Running command for rate calculation

#### 1.2.1 Setup an environment

Navigate to

	 ->  3. Run 3 setting ->  3.2 Set up your system and prepare an existing menu for rate estimation 
	 
And setup the environment

```
ssh -XY your_name@lxplus.cern.ch

# 1. Setting up the environment and folder structure
cmsrel CMSSW_11_1_5
cd CMSSW_11_1_5/src/
git clone --depth 1 https://github.com/cms-l1-dpg/L1MenuTools.git
cd L1MenuTools/rate-estimation/

# 2. Translating a menu XML file into C++ code
wget https://raw.githubusercontent.com/cms-l1-dpg/L1MenuRun3/master/development/L1Menu_Collisions2022_v0_1_1/L1Menu_Collisions2022_v0_1_1.xml  # alternatively: place your custom menu XML here
bash configure.sh L1Menu_Collisions2022_v0_1_1.xml  # alternatively: provide your custom menu XML

# 3. Compile the rate estimation framework with your custom menulib.* files
cmsenv
mkdir -p objs/include
make -j 8

```

#### 1.2.2 Copying `ntuple.txt` into working directory

Now copy `ntuple.txt` file into `CMSSW_11_1_5/src/L1MenuTools/rate-estimation/ntuple` directory.


#### 1.2.3 Prescale table making

Navigate to

	 ->  3. Run 3 setting -> 3.3.3 Prescale table 
	 
```


cd L1MenuTools/pstools
bash run-ps-generate.sh \
  https://github.com/cms-l1-dpg/L1Menu2018/raw/master/official/PrescaleTables/PrescaleTable-1_L1Menu_Collisions2018_v2_1_0.xlsx \
  https://raw.githubusercontent.com/cms-l1-dpg/L1MenuRun3/master/development/L1Menu_Collisions2022_v0_1_1/L1Menu_Collisions2022_v0_1_1.xml \
  --output Prescale_2022_v0_1_1
``` 

#### 1.2.4 Copying menu.xml into working directory

In this documentation I will use default xml, which used in twiki documenatation

#### 1.2.5 Compilation

##### Every time you modify your menu, run:

```
#Assume the user is at L1MenuTools/rate-estimation/

#1. Translating a menu XML file into C++ code
bash configure.sh L1Menu_Collisions2022_v0_1_1.xml # alternatively: provide your custom menu XML

# 2. Compile the rate estimation framework with your custom menulib.* files
cmsenv
mkdir -p objs/include
make -j 8

```

#### 1.2.6 Running command for rate calculation

	./testMenu2016 -m menu/Prescale_2022_v0_1_1.csv -l ntuple/ntuple.txt -o testoutput -b 2544 --doPlotRate --doPlotEff --SelectCol 2E+34

You can find [here](./src/testoutput.txt) sample output of the above command.

### SUMMARY

Steps which need to repeat during the testings are:

* 1.2.3 
* 1.2.4
* 1.2.5
* 1.2.6

