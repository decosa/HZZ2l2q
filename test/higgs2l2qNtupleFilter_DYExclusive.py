import FWCore.ParameterSet.Config as cms

process = cms.Process("NTPFILT")

#### Simple cfg to apply event filter to ntuple

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource")

process.source.fileNames=cms.untracked.vstring('file:h2l2q_ntuple_99_1_1Be.root')

#### DY+0Jets filter
process.dyFilter = cms.EDFilter(
    "DYExclusiveFilter",
    src = cms.InputTag("LHENup","lheNup","TRIM")
    )

#### Event cleaning 
process.badEventFilter = cms.EDFilter(
    "HLTHighLevel",
    TriggerResultsTag = cms.InputTag("TriggerResults","","PAT"),
    HLTPaths = cms.vstring('primaryVertexFilterPath',
#                           'CSCTightHaloFilterPath',
#                           'EcalDeadCellTriggerPrimitiveFilterPath',
                           'EcalDeadCellBoundaryEnergyFilterPath',
                           'noscrapingFilterPath',          
#                           'hcalLaserEventFilterPath', ###it should not affect the datasample 
                           'HBHENoiseFilterPath'#,
#                           'totalKinematicsFilterPath' #only for Madgraph MC
                           ),
    eventSetupPathsKey = cms.string(''),
    # how to deal with multiple triggers: True (OR) accept if ANY is true, False
    # (AND) accept if ALL are true
    andOr = cms.bool(False),
    throw = cms.bool(True)  # throw exception on unknown path names
    )


### To comment in case of MC samples




process.cleaningPath = cms.Path(
    process.dyFilter
    )


process.edmNtuplesOut = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('h2l2q_ntuple_clean.root'),
    outputCommands = cms.untracked.vstring(
    "keep *",
    "drop *_TriggerResults_*_PAT",
    "drop *_TriggerResults_*_NTPFILT",
    )
    )

process.edmNtuplesOut.SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('cleaningPath')
    )

process.edmNtuplesOut.dropMetaData = cms.untracked.string('ALL')

process.endPath = cms.EndPath(process.edmNtuplesOut)

