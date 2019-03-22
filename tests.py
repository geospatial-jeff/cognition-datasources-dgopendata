from datasources import tests

from DGOpenData import DGOpenData

class DGOpenDataTestCases(tests.BaseTestCases):

    def _setUp(self):

        self.datasource = DGOpenData
        self.spatial = {
                        "type": "Polygon",
                        "coordinates": [
                          [
                            [
                              -120.673828125,
                              32.509761735919426
                            ],
                            [
                              -115.1806640625,
                              32.509761735919426
                            ],
                            [
                              -115.1806640625,
                              36.35052700542763
                            ],
                            [
                              -120.673828125,
                              36.35052700542763
                            ],
                            [
                              -120.673828125,
                              32.509761735919426
                            ]
                          ]
                        ]
                      }
        self.temporal = ("2018-11-01", "2018-11-20")
        self.properties = {'legacy:event_name': {'eq': 'california-wildfires'}}
        self.limit = 10