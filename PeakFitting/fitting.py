from enum import Enum

class Trend(Enum):
    GREATER = 'greater'
    GREATER_EQ = 'less eq'
    LESS = 'less'
    LESS_EQ = 'less eq'


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

    def find_peaks(self, base_intensity=None, n_derivatives=1):
        """
        :param base_intensity:
        :return:
        """
        if not self.is_fit:
            raise ValueError("Data set must be loaded with FindPeaks.fit(two_theta,intensity) before find_peaks is called")
        if base_intensity is not None:
            self.base_intensity = base_intensity
        peaks = []
        peak_widths = []
        peak_end = 0
        derivatives = self.intensity.diff()
        for i in range(self.intensity):
                flip, direction, n_steps = self.__find_derivative_flip(i, derivatives)
                i += n_steps
                peaks.append((flip, direction, n_steps))

        return peaks

    def _find_peak_from_end_pt(self, end_last_peak, n_derivatives):
        """
        :param: end_last_peak, the index where the previous peak ends
        :return: index of highest y value in range from end_last_peak to the end of the next peak
        """
        peak_start = self.__find_peak_start(end_last_peak)
        # TODO raise better error
        if peak_start is None:
            raise AttributeError("Could not find next peak start")

        peak_apex = self.__find_peak_apex(peak_start)
        peak_end = self.__find_peak_end(peak_apex)

        return peak_start, peak_apex, peak_end

    # TODO logic for the three below helper functions can likely be combined
    def __find_peak_start(self, end_last_peak, n_derivatives):
        for i in range(end_last_peak, len(self.intensity) - 2):
            if self.intensity[i] >= self.base_intensity and self.intensity[i + 1] >= self.base_intensity and\
                    self.intensity[i + 2] >= self.base_intensity:
                return i

    def __find_peak_apex(self, peak_start, n_derivatives):
        delta_intensity = self.intensity.diff()
        for i in range(peak_start, len(delta_intensity) - 3):  # finds max peaks
            if delta_intensity[i] <= 0 and delta_intensity[i + 1] <= 0 and delta_intensity[i + 2] <= 0 and\
                    delta_intensity[i + 3] <= 0:
                return i

    def __find_peak_end(self, peak_apex):
        for i in range(peak_apex, len(self.intensity)):  # finds the end of the peak
            if self.intensity[i] < self.base_intensity and self.intensity[i + 1] < self.base_intensity and\
                    self.intensity[i + 2] < self.base_intensity:
                return i

    @staticmethod
    def __find_derivative_flip(self, start, derivatives):
        comparable = zip(range(start, len(derivatives) - 1), range(start + 1, len(derivatives)))
        flip = None
        direction = None
        n_steps = None
        for first, second in comparable:
            sign_derivative_one = derivatives[first] / derivatives[first]
            sign_derivative_two = derivatives[second] / derivatives[second]
            if sign_derivative_one != sign_derivative_two and flip is None and direction is None:
                flip = second
                direction = sign_derivative_two
            elif sign_derivative_one != sign_derivative_two:
                n_steps = second - flip
                break
        return flip, direction, n_steps





