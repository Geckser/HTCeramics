
# CONSTANT VARIABLES
PWHMA = 0.4  # peak width half max a?
PWHMB = 0.2  # peak width half max b?
FIT = 5  # constant to ensure ball is slightly wider than the peaks
C_ENERGY = 4.123  # Energy calibration constant?
M_ENERGY = 0.0204  # Energy calibration  gradient?


# Arrays are created as arrays indexed from 1 to 1024 (inclusive) of real numbers
peaks = []

spec = []
back = []
peak = []
espc = []

# files "Text" type in pascal
# TODO it is initially unclear how files are used in pascal determine file usage as translated
# after going through the whole program these files are not used I think it is supposed to be implied that these are the files that
# data is read from and written to. I will speculate about their usage next to them
input_file = None  # some kind of input. Is it intensity? is it angle is it both? only god knows
back_file = None  # maybe file to write calculated background noise too?
spec_file = None  # spec = spectrum ? 
peak_file = None  # write peaks here?
error_file = None  # error logging

def fit_back():
    # integers
    i = None
    j = None
    width = None

    # more arrays indexed from 1 to 1024 of real numbers
    # TODO figure out what any of these variables do
    T1 = []  
    T2 = []
    T3 = []
    count = []
    
    # create two real variables used in the nested procedure
    energy = None 
    width_e = None
    def set_width(k):
        # TODO what does k do?
        """
        param k: integer
        """
        energy = k * M_ENERGY + C_ENERGY  # convert channels to energy <-- seems important but wtf does that mean
        width_e = energy * PWHMA + PWHMB  # set width in energy scale <-- also seems important
        width = round((((width_e - C_ENERGY) / M_ENERGY) + FIT) / 2)  # convert to channels

    # loop form 1 to 1024 to loop through an array
    # this loop initializes arrays in the most monkey way possible
    for i in range(1, 1025):
        T1[i] = 32767  # this value is the max integer storable in pascal int should replace with sys.maxint
        T2[i] = 0
        T3[i] = 0
        count[i] = 0

    
    # minimize? what are we minimizing. Do you write papers to be understood? or just to gloat?
    for i in range(1, 1025):
        set_width(i) # each time this is called it modifies the global width variable because these dickheads didn't know what return did or that pascal had it
        for j in range(-width, width + 1):
            if (i + j) > 0 and (i + j) < 1025:  # range check to index array
                if T1[i] < spec[i + j]:
                    T1[i] = spec[i + j]
    
    # maximize? again the only comment with the loop completely unexplained otherwise very epic
    for i in range(1, 1025):
        set_width(i)
        for j in range(-width, width + 1):
            if (i + j) > 0 and (i + j) < 1025:
                if T1[i] < spec[i + j]:
                    T1[i] = spec[i + j]


    # smooth? 
    for i in range(1, 1025):
        set_width(i)
        for j in range(-width, width + 1):
            if (i + j) > 0 and (i + j) < 1025:
                T3[i] = T3[i] + T2[i + j]  # sum, thank you for the insightful comment
                count[i] = count[i] + 1

        back[i] = round(T3[i] / count[i])  # average



# some sudo code at the bottom because they couldn't be bothered to write the code to run this algorithm
open_files()
initialize()  # ??????????????
repeat:
    try:
        fit_back()
        fit_peaks()
        minimize_error() # ???????????????? what is this 
    except Error e:
        print('it threw an error were probably done finding signal')
        break
    if FIT_IS_GOOD:  # this variable is never defined or explained
        break

write_results() 