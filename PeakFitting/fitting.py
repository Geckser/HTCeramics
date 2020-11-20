
# TODO doc comments
class FindPeaks:
    """
    Logic for finding peaks
    """
    def __init__(self):
        self.two_theta = None
        self.intensity = None
        self.base_intensity = None
        self.is_fit = False

    def fit(self, two_theta, intensity):
        """
        :param two_theta: numpy array of ...
        :param intensity:
        :return:
        """
        self.two_theta = two_theta
        self.intensity = intensity
        self.base_intensity = 2 * intensity.mean()
        self.is_fit = True

    def find_peaks(self, base_intensity=None):

        """
        :param base_intensity:
        :return:
        """
        if not self.is_fit:
            raise ValueError("Data set must be loaded with FindPeaks.fit(two_theta,intensity) before find_peaks is called")
        if base_intensity is None:
            base_intensity = self.base_intensity
        peaks = []


    def _find_peak_from_end_pt(self, end_last_peak):
        """
        :param: end_last_peak, the index where the previous peak ends
        :return: index of highest y value in range from end_last_peak to the end of the next peak
        """
        peak_start = self.__find_peak_start(end_last_peak)

        # TODO raise better error
        if peak_start is None:
            raise IndexError("Could not find next peak start")

        peak_apex = self.__find_peak_apex(peak_start)
        peak_end = self.__find_peak_end(peak_apex)

        return peak_start, peak_apex, peak_end

    def __find_peak_start(self, end_last_peak):
        peak_start = None
        for i in range(end_last_peak, len(self.intensity) - 2):
            if self.intensity[i] >= self.base_intensity and self.intensity[i + 1] >= self.base_intensity and \
                    self.intensity[i + 2] >= self.base_intensity:
                peak_start = i
                break
        return peak_start

    def __find_peak_apex(self, peak_start):
        delta_intensity = self.intensity.diff()
        for i in range(peak_start, len(delta_intensity) - 3):  # finds max peaks
            if delta_intensity[i] <= 0 and delta_intensity[i + 1] <= 0 and delta_intensity[i + 2] <= 0 and\
                    delta_intensity[i + 3] <= 0:
                return i
            else:
                continue

    def __find_peak_end(self, peak_apex):
        for i in range(peak_apex, len(self.intensity)):  # finds the end of the peak
            if self.intensity[i] < self.base_intensity and self.base_intensity[i + 1] < self.base_intensity and\
                    self.base_intensity[i + 2] < self.base_intensity:
                return i




import pandas as pd
data = pd.read_csv('xrdData/ware_pzt/pzt1Num.csv')
two_theta = data['Angle']
intensity = data['Intensity']

peak_finder = FindPeaks()
peak_finder.fit(two_theta, intensity)
peaks = peak_finder.find_peaks()
print('_')
