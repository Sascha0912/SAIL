def defaultParamSet():
    class P(self):
        # MAP-Elites Parameters
        self.nChildren = 2**7
        self.mutSigma  = 0.1
        self.nGens     = 2**8

        # Infill Parameters
        self.nInitialSamples    = 50
        self.nAdditionalSamples = 10
        self.nTotalSamples      = 1000
        self.trainingMod        = 2

        # Display Parameters
        self.display_figs    = False
        self.display_gifs    = False
        self.display_illu    = False
        self.display_illuMod = self.nGens

        # Data Gathering Parameters
        self.data_outSave = True
        self.data_outMod  = 50
        self.data_mapEval = False
        self.data_mapEvalMod = self.nTotalSamples
        self.data_outPath = ''

    return P()
