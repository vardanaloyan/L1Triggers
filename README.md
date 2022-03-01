# Trigger Rate calculations

Plan

1. Rate calculation MC
2. Rate calculation DATA
   - NTuple making
   - Rate calculation
    

## Rate calculation MC

Using [HowToL1TriggerMenu](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HowToL1TriggerMenu#4_2_Set_up_your_system_and_confi)
instructions.

```bash
ssh -XY your_name@lxplus.cern.ch

# 1. Setting up the environment 
cmsrel CMSSW_12_3_0_pre1
cd CMSSW_12_3_0_pre1/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline l1t-integration-CMSSW_12_3_0
git cms-merge-topic -u cms-l1t-offline:l1t-integration-v119.0
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TCalorimeter.git L1Trigger/L1TCalorimeter/data
git cms-checkdeps -A -a
scram b -j 8

# 2. Setting up the MenuTools environment (NOTE: logout and then go back to CMSSW_12_3_0_pre1/src; no cmsenv)
git clone --depth 1 https://github.com/cms-l1-dpg/L1MenuTools.git
cd L1MenuTools/rate-estimation

# 3. Translating a menu XML file into C++ code
wget https://raw.githubusercontent.com/cms-l1-dpg/L1MenuRun3/master/development/L1Menu_Collisions2022_v0_1_2/L1Menu_Collisions2022_v0_1_2.xml . # alternatively: place your custom menu XML here
bash configure.sh L1Menu_Collisions2022_v0_1_2.xml  # alternatively: provide your custom menu XML

# 4. Compile the rate estimation framework with your custom menulib.* files
cmsenv
mkdir -p objs/include
make -j 8

Every time you modify your menu, run:

#Assume the user is at L1MenuTools/rate-estimation/

#1. Translating a menu XML file into C++ code
bash configure.sh L1Menu_Collisions2022_v0_1_2.xml # alternatively: provide your custom menu XML

# 2. Compile the rate estimation framework with your custom menulib.* files
cmsenv
mkdir -p objs/include
make -j 8
```



##  Every time you modify your menu, run: 

```bash
# Assume the user is at L1MenuTools/rate-estimation/

#1. Translating a menu XML file into C++ code
bash configure.sh L1Menu_Collisions2022_v0_1_2.xml # alternatively: provide your custom menu XML

# 2. Compile the rate estimation framework with your custom menulib.* files
cmsenv
mkdir -p objs/include
make -j 8
```

After running the command
```bash
./testMenu2016 -m menu/Prescale_2022_v0_1_2.csv -l ntuple/Run3_NuGun_MC_ntuples.list -o testoutput -b 2544 --doPlotRate --doPlotEff --maxEvent 20000 --SelectCol 2E+34 --doPrintPU --allPileUp --doReweightingRun3
```

I get the following results (Wrapped)

```text
...
357       L1_DoubleJet_110_35_DoubleJet35_Mass_Min620                     1         17538.1    +/- 5042.31             3545.32        7957.98        16             
358       L1_DoubleJet_115_40_DoubleJet40_Mass_Min620                     1         12970.4    +/- 4336.27             0              3901.5         10             
359       L1_DoubleJet_120_45_DoubleJet45_Mass_Min620                     1         6524.15    +/- 3075.4              0              1301.97        7              
360       L1_DoubleJet_115_40_DoubleJet40_Mass_Min620_Jet60TT28           1         7478.65    +/- 3292.69             0              1641.69        5              
361       L1_DoubleJet_120_45_DoubleJet45_Mass_Min620_Jet60TT28           1         3737       +/- 2327.56             0              394.478        3              
363       L1_DoubleJet35_Mass_Min450_IsoTau45_RmOvlp                      0         0          +/- 0                   0              0              0              
364       L1_DoubleJet_80_30_Mass_Min420_IsoTau40_RmOvlp                  0         0          +/- 0                   0              0              0              
365       L1_DoubleJet_80_30_Mass_Min420_Mu8                              0         0          +/- 0                   0              0              0              
366       L1_DoubleJet_80_30_Mass_Min420_DoubleMu0_SQ                     0         0          +/- 0                   0              0              0              
372       L1_TripleJet_95_75_65_DoubleJet_75_65_er2p5                     1         1398.32    +/- 1423.78             372.349        796.451        3              
373       L1_TripleJet_100_80_70_DoubleJet_80_70_er2p5                    1         0          +/- 0                   0              0              0              
374       L1_TripleJet_105_85_75_DoubleJet_85_75_er2p5                    1         0          +/- 0                   0              0              0              
376       L1_QuadJet_95_75_65_20_DoubleJet_75_65_er2p5_Jet20_FWD3p0       1         1025.97    +/- 1219.57             0              424.101        2              
382       L1_QuadJet60er2p5                                               0         0          +/- 0                   0              0              0              
...
```

## Rate calculation DATA

### NTuple making


### 1 Ntuple making process

This step was done according to twiki [SWGuideL1TStage2Instructions](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TStage2Instructions) documentation

#### 1.1 Environment setup
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


#### 1.2 Processing script generation
Navigate to

	 -> L1T Cookbook: current recipes -> Re-emulating 2018 data with the new 2018 CaloParams and conditions 
	 
Following command used to generate processing script

```
cmsDriver.py l1Ntuple -s RAW2DIGI --python_filename=data.py -n -1 --no_output --era=Run2_2018 --data --conditions=112X_dataRun2_v7 --customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleRAWEMU --filein=file:/eos/cms/store/data/Run2018D/store/data/Run2018D/ZeroBias/RAW/v1/000/325/240/00000/4E953DE3-A07E-6F45-94F4-E530035D3757.root
```

This will generate [data.py](./src/data.py) file.
Do not pay attention if the command would not execute successfully due to some networking issues. Important to have generated `data.py` file.

#### 1.3 Submiting crab jobs for making NTuples

For crab jobs we are using this [`Crab_TrgEff_Data.py`](./src/Crab_TrgEff_Data.py) file. 
In this configuration we are using following dataset

`/EphemeralZeroBias1/Run2018D-v1/RAW`

After getting the NTuples, I prepared simple script to gather the filepaths of those NTuples.
I saved this as `llist` file

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

The usage of the script is the following (for example my Ntuples are in `"/eos/user/a/aloyan/2021/trigger/crab_projects/crab_Run2018D-v1/results/*.root" >> ~/files.txt`)

I will run the command to get the filenames

`llist "/eos/user/a/aloyan/2021/trigger/crab_projects/crab_Run2018D-v1/results/*.root" >> ~/files.txt`

Then You need to move the `files.txt` file into `CMSSW_12_3_0_pre1/src/L1MenuTools` directory and run the the command 
for rate calculation mentioned in the first part of this doc.

`./testMenu2016 -m menu/Prescale_2022_v0_1_2.csv -l ntuple/files.txt -o testoutput -b 2544 --doPlotRate --doPlotEff --maxEvent 20000 --SelectCol 2E+34 --doPrintPU --allPileUp`


Unfortunately results are still unsatisfying due to the -1 values in `results/?_PU.csv` file.

