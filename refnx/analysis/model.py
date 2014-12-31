from __future__ import division
import refnx.dataset.reflectdataset as reflectdataset
import numpy as np
import refnx.analysis.reflect as reflect
import matplotlib.artist as artist
import os.path
import os
import string


class Model(object):

    def __init__(self, parameters, **kwds):
        __members = {'file': None,
                     'parameters': None,
                     'fitted_parameters': None,
                     'uncertainties': None,
                     'covariance': None,
                     'limits': None,
                     'usedq': True,
                     'fitPlugin': None,
                     'useerrors': True,
                     'quad_order': 17}

        self.__members = __members

        if 'file' in kwds:
            self.load(kwds['file'])
        else:
            for key in __members:
                if key in kwds:
                    setattr(self, key, kwds[key])
                else:
                    setattr(self, key, __members[key])

            if parameters is None:
                self.parameters = np.array([], dtype='float64')
            else:
                self.parameters = parameters

            if self.fitted_parameters is None:
                self.fitted_parameters = np.array([], dtype='int')

            if self.uncertainties is None:
                self.uncertainties = np.array(
                    [np.nan] * self.parameters.size,
                    dtype='float64')

            if self.covariance is None:
                self.covariance = np.zeros(
                    (self.parameters.size, self.parameters.size))

            if self.limits is None:
                self.default_limits(True)

    def __getitem__(self, key):
        if key in self.__members:
            return self.key

    def __setitem__(self, key, value):
        if key in self.__members:
            setattr(self, key, value)

    def save(self, f):
        f.write(f.name + '\n')
        f.write(str(self.parameters.size) + '\n')
        f.write('parameter\thold\tlowlin\thilim\tuncertainty\n')
        holdvector = np.ones_like(self.parameters, dtype='int')
        holdvector[self.fitted_parameters] = 0

        if self.limits is None or self.limits.ndim != 2 or np.size(self.limits, 1) != np.size(self.parameters):
            self.default_limits(True)

        # go through and write parameters to file
        np.savetxt(
            f,
            np.column_stack((self.parameters,
                             holdvector,
                             self.limits.T,
                             self.uncertainties)))

        f.write('covariance matrix\n')
        np.savetxt(f, self.covariance)

    def load(self, f):
        h1 = f.readline()
        h2 = f.readline()
        h3 = f.readline()
        numparams = int(h2)

        array = np.fromfile(
            f,
            dtype='float64',
            sep='\t',
            count=numparams *
            5)
        array = array.reshape(numparams, 5)

        self.parameters, a2, lowlim, hilim, self.uncertainties = np.hsplit(
            array, 5)

        self.parameters = self.parameters.flatten()
        self.uncertainties = self.uncertainties.flatten()
        self.limits = np.column_stack((lowlim, hilim)).T

        a2 = a2.flatten()
        self.fitted_parameters = np.where(a2 == 0)[0]

        # now read covariance matrix
        h4 = f.readline()
        self.covariance = np.fromfile(
            f,
            dtype='float64',
            sep=' \t',
            count=numparams *
            numparams)
        self.covariance = self.covariance.reshape((numparams, numparams))

    def default_limits(self, set=False):
        defaultlimits = np.zeros((2, np.size(self.parameters)))

        for idx, val in enumerate(self.parameters):
            if val < 0:
                defaultlimits[0, idx] = 2 * val
            else:
                defaultlimits[1, idx] = 2 * val

        if set:
            self.limits = defaultlimits

        return defaultlimits