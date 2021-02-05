import numpy as np
import pandas as pd
import xlsxwriter


class rat():
  def __init__(self):
    name = ""
    rat_id = ""
    rat_group = ""
    starting_time = 0
    sampling_f = 1

  def read_excel(self, file_route, codes_dict):
    dfrat = pd.read_excel(file_route, sheet_name=0, dtype={'location':str}) # reads the first sheet
    self.rat_id = dfrat.iloc[0]['Subject']
    #self.rat_group = dfrat.iloc[0]['Description']
    self.dfnew = dfrat[["Behavior", "location", "Start (s)", "Stop (s)", "Duration (s)"]]
    # Changes modules names to numbers to make calculations faster
    self.dfnew["location"] = self.dfnew["location"].map(codes_dict)
    #print(self.dfnew)


  def add_sampling(self, samp_freq, samp_time):
    self.sampling_f = samp_freq
    self.starting_time = self.dfnew["Start (s)"][0]*samp_freq
    self.dfnew['samples'] = self.dfnew['Duration (s)']*samp_freq
    self.dfnew.round({'samples' : 0})
    self.dfnew['samples'] = self.dfnew['samples'].astype(int)
    #file_name = "output" + str(self.rat_id) + '.xlsx'
    #self.dfnew.to_excel(file_name)
    modifiers_ar = self.dfnew['location'].to_numpy().astype(int)
    samples_ar = self.dfnew['samples'].to_numpy()
    mod_samp = np.vstack((modifiers_ar, samples_ar)).T
    resamp_data = []
    time_list = []
    t_time = int(self.starting_time)

    # First we fill samples from time zero until the start of recording
    for t in np.arange(t_time):
      resamp_data.append(511) # location 511 means it is nowhere
      time_list.append(int(t))
    # Then the rest of the samples
    for (x,y) in mod_samp:
      for i in range(y):
        resamp_data.append(x)
        time_list.append(t_time)
        t_time = t_time + 1 # one sample, whatever the sample time is

    self.rat_times = np.rint(np.asarray(time_list)).astype(int)
    self.rat_location = np.asarray(resamp_data).astype(int)
    self.last_sample = t_time

  def chop_times(self, chop_time):
    temp_times = self.rat_times[:chop_time]
    temp_locations = self.rat_location[:chop_time]
    self.rat_times = temp_times
    self.rat_location = temp_locations
    self.last_sample = self.rat_times[-1]

  def basic_stats(self, mod_d):
    # says all the modules where the rat has been, when arrived for the first time
    # and the total number of samples it has stayed in each module
    self.uniqueplaces, self.uniquefirsttimes, self.uniquenumbertimes = \
            np.unique(self.rat_location, return_index = True, return_counts = True)

    self.unique_places_names = []
    print('basic stats, rat number: ', self.rat_id)
    for place in self.uniqueplaces:
      self.unique_places_names.append(list(mod_d.keys())[list(mod_d.values()).index(place)])


  def calculate_coincidences(self, base_colum, location_matrix, modules_d):
    # first delete the colum of this rat
    location_matrix = np.delete(location_matrix, base_colum, 1)
    this_rat_locations = np.transpose(self.rat_location)
    # matrix with zeros where there is a coincidence
    substracted_matrix = location_matrix - this_rat_locations[:,None]
    truth_matrix = (substracted_matrix == 0)

    # Overall coincidences. Number of times with 1 or more other animals.
    sum_truth_matrix = np.sum(truth_matrix, axis = 1)
    sum_matrix_downsampled = sum_truth_matrix[::1000].copy()
    rat_locations_downsampled = self.rat_location[::1000].copy()
    
    sort_idx = np.argsort(list(modules_d.values()))
    idx = np.searchsorted(list(modules_d.values()),rat_locations_downsampled,sorter = sort_idx)
    out = np.asarray(list(modules_d.keys()))[sort_idx][idx]
    
    dfcoinc = pd.DataFrame()
    dfcoinc['location'] = out
    dfcoinc['coinc n#'] = sum_matrix_downsampled
    filename = 'coincidencesbysecond_rat' + str(self.rat_id) + '.xlsx'
    dfcoinc.to_excel(filename)
    unique, counts = np.unique(sum_truth_matrix, return_counts=True)
    self.companions_times = dict(zip(unique, counts))

    # Per module or tunnel
    self.l_companions_times_per_module= []
    for (mod_name, mod_value) in (modules_d.items()):
      mod_truth_matrix = truth_matrix[this_rat_locations == mod_value, :]
      sum_truth_matrix_mod = np.sum(mod_truth_matrix, axis = 1)
      unique, counts = np.unique(sum_truth_matrix_mod, return_counts=True)
      companions_times = dict(zip(unique, counts/self.sampling_f))
      self.l_companions_times_per_module.append((mod_name, companions_times))

    #print("Id: ", self.rat_id, ' Number of companions per module: ', self.l_companions_times_per_module)

    # now compares one rat at a time with each of the other rats to get the 
    # total amount of time shared with each rat in each module or tunnel
    # we already have the matrix with all the differences (truth_matrix)
    # we are going to export a matrix with the modules as rows and the other rats as columns
    self.shared_time_per_module_per_rat = np.zeros((len(modules_d), truth_matrix.shape[1]))
    # loop through every module
    for n, (mod_name, mod_value) in enumerate(modules_d.items()):
      # loope through every rat
      for rat_column in truth_matrix.shape[1]:
        mod_truth_rat = truth_matrix[this_rat_locations == mod_value, rat_column]
        self.shared_time_per_module_per_rat[n][rat_column] = np.sum(mod_truth_rat)




# No estoy seguro de querer la matriz de non zeros. La matriz de nonzeros sirve para saber el tiempo total que
# el animal ha pasado en compania. Ni siquiera, porque hay muchas columnas.
#
#  Haz algo simple con la matriz de coincidencias. Usar la booleana para sumar zeros en cada columna.
# Me va a faltar el nombre de la rata.