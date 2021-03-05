import sys
import os
import platform
import glob
import re as re
import numpy as np
import random
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import xlsxwriter

from w_coincidencies import *
from coincidences_classes import *

from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QFileDialog, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QPushButton, QErrorMessage
from PyQt5.QtCore import pyqtSlot


import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

from datetime import datetime

sampling_freq = 1000
sampling_time = 1/sampling_freq
# translating modules tunnels into numbers because calculations are faster that way
# modules 511 refers to sample not recorded
modules_dict = {"A1":32,"A2":33, "A3":34, "A4":35, "B1":36, "B2":37, "B3":38, "B4":39, \
               "C1":40,"C2":41, "C3":42, "C4":43, "D1":44,"D2":45, "D3":46, "D4":47, \
                "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "11":11, "12":12, "13":13, \
                "tC":14, "tD":15, "Norec":511}

# d.items() >> d.keys() >> d.values() to use it and recover the keys.



class MyForm(QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_w_coincidencies()
    self.ui.setupUi(self)

    self.ui.ButtonSelectFolder.clicked.connect(self.selectFolder)
    self.ui.ButDelFolder.clicked.connect(self.delFolder)
    self.ui.ButtonResultFolder.clicked.connect(self.selectResultFolder)
    self.ui.ButDelResultFolder.clicked.connect(self.delResultFolder)
    self.ui.ButtonSelectFile.clicked.connect(self.selectFile)
    self.ui.ButDelFile.clicked.connect(self.delFile)
    self.ui.ButtonRunAll.clicked.connect(self.runAll)
    
    # Error message (it is necessary to initialize it too)
    self.error_msg = QErrorMessage()
    self.error_msg.setWindowTitle("Error")
    self.show()


  def selectFolder(self):
    DataFolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    if DataFolder:
      self.ui.labelFolderPath.setText(DataFolder)
      self.delFile()
    else:
      self.error_msg.showMessage("It is necessary to select a folder")

  def delFolder(self):
    self.ui.labelFolderPath.clear()

  def selectResultFolder(self):
    self.ResultsFolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    if self.ResultsFolder:
      self.ui.labelResultFolderPath.setText(self.ResultsFolder)
    else:
      self.error_msg.showMessage("It is necessary to select a folder")
  
  def delResultFolder(self):
    self.ui.labelResultFolderPath.clear()
  
  def selectFile(self):
    options = QFileDialog.Options()
    self.filename, _ = QFileDialog.getOpenFileName(self,"Select Spreadsheet", "", "Excel files (*.xlsx)", options=options)
    if self.filename:
      self.ui.labelFilePath.setText(self.filename)
      self.delFolder()
  
  def delFile(self):
    self.ui.labelFilePath.clear()

  def runAll(self):
    if str(self.ui.labelResultFolderPath.text()) == '':
      self.error_msg.showMessage("It is necessary to select an empty results folder")
    else:
      if str(self.ui.labelFolderPath.text()) != '' : 
        # A folder path is given
        os.chdir(str(self.ui.labelFolderPath.text()))
      elif str(self.ui.labelFilePath.text()) != '' :
        # A file path is given and the file contains several sheets
        xls = pd.ExcelFile(self.filename)
        os.chdir(str(self.ui.labelResultFolderPath.text()))
        for n, sheet in enumerate(xls.sheet_names):
          df = pd.DataFrame()
          df = pd.read_excel(self.filename, sheet_name=sheet)
          filename_out = 'rat_' + str(n+1) +'.xlsx' 
          df.to_excel(filename_out, index = 0)

      
      if platform.system() == 'Windows':
        d = os.getcwd() + "\\" # windows 
      else:
        d = os.getcwd() + "/" # linux & MacOS

      matching_files = sorted(glob.glob(r'*xlsx')) # not sorted by name by default
      l_xlsx_files = []
      self.rats = []
      self.rats_ids = []
      last_samples = []

      for matching_file in matching_files:
        file_route = d + matching_file
        l_xlsx_files.append(file_route)

        rat_n = rat()

        rat_n.read_excel(file_route, modules_dict)
        if not rat_n.consistency:
          error_message = "time errors in rat: " + str(rat_n.rat_id) + " columns: " + np.array2string(rat_n.excel_locations)
          self.error_msg.showMessage(error_message)
          
        rat_n.add_sampling(sampling_freq, sampling_time)
        #print(rat_n.rat_location)
        #print(rat_n.starting_time)
        #print(rat_n.rat_times)
        self.rats.append(rat_n)
        self.rats_ids.append(rat_n.rat_id)

        last_samples.append(rat_n.last_sample)

      # for comparison, all the rats should have the same tracking time, the minimun
      self.max_time = min(last_samples)
      for rat_n in (self.rats):
        rat_n.chop_times(self.max_time)
        rat_n.basic_stats(modules_dict)
        #print('modules or tunnels: ', rat_n.uniqueplaces)
        #print('Modules names:', rat_n.unique_places_names)
        #print('number of times: ', rat_n.uniquenumbertimes)


      #print ("Data and figures correctly exported to excel")
      self.calc_tracking_coinc()
      self.export_coincidences_to_excel()

  def export_coincidences_to_excel(self):
    workbook = xlsxwriter.Workbook('coincidencies.xlsx')
    for rat_n in (self.rats):
      worksheet_rat= workbook.add_worksheet(str(rat_n.rat_id))
      worksheet_rat.write(0, 0, "Number of companions per module")
      worksheet_rat.write(2, 0, "Module")
      worksheet_rat.write(2, 1, "Number of companions")
      worksheet_rat.write(2, 2, "Seconds")
      for n, mod in enumerate(rat_n.l_companions_times_per_module):
        if mod[0] in np.arange(16):
          module = "T" + str(mod[0])
        else:
          module = mod[0]
        worksheet_rat.write(n+3, 0, module)
        i = 0
        for item in mod[1].items():
          #companions_number = int(*item.keys())
          #samples_number = int(*item.values())
          worksheet_rat.write(n+3, i+1, item[0])
          worksheet_rat.write(n+3, i+2, item[1])
          i = i + 2
    workbook.close()

    # for clarity, another loop to export the coincidences per module per rat
    writer = pd.ExcelWriter('coincident_time_per_module_per_rat.xlsx', engine='xlsxwriter')
    for rat_n in (self.rats):
      #the_other_rats = list(filter((rat_n.rat_id).__ne__, self.rats_ids)) # excludes the current rat from the list
      list_modules = list(modules_dict.keys())
      rat_df = pd.DataFrame(rat_n.shared_time_per_module_per_rat, \
                            columns=self.rats_ids, index=list_modules)
      # adding averages per column (animals) and rows (modules&tunnels)
      rat_df.loc['Totals',:] = rat_df.sum(axis=0) - rat_df.loc['Norec']
      #cols_to_sum = rat_df.columns[ : rat_df.shape[1]]
      #rat_df['Totals'] = rat_df[cols_to_sum].sum(axis=1) - rat_df[rat_n.rat_id]

      #print(rat_df)
      
      rat_df.to_excel(writer, sheet_name=str(rat_n.rat_id))

    writer.save()

  def closeFigures(self):
    plt.close('all')


  def print2pdf(self, filename = ''):
    if filename:
      filename2 = '/' + filename + '.pdf'
      pdf = matplotlib.backends.backend_pdf.PdfPages(str(self.ui.labelFileSelected.text()) + filename2)
      figs = [plt.figure(n) for n in plt.get_fignums()]
      for fig in figs:
        fig.savefig(pdf, format='pdf')
      pdf.close()
    else:
      self.error_msg.showMessage("It is necessary to select a folder")


  def print2png(self):
    figFolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    if figFolder:
         prefix = '/' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
         for i in plt.get_fignums():
              plt.figure(i)
              plt.savefig(figFolder + prefix +'figure%d.png' % i)
    else:
         self.error_msg.showMessage("It is necessary to select a folder")

  def calc_tracking_coinc(self):
    allrats_locations = []
    for rat_n in self.rats:
      allrats_locations.append(rat_n.rat_location)

    # matrix with all rats and their location per sample
    all_rats_locations = np.transpose(np.asarray(allrats_locations)).astype(int)
    for r, rat_n in enumerate(self.rats):
      rat_n.calculate_coincidences(r, all_rats_locations, modules_dict)
    
    

  ## making recordings of the same lenght
  #if np.size(self.resamp_data2) < np.size(self.resamp_data1):
  #  rat1_data = self.resamp_data1[:np.size(self.resamp_data2)]
  #  rat2_data = self.resamp_data2
  #else:
  #  rat2_data = self.resamp_data2[:np.size(self.resamp_data1)]
  #  rat1_data = self.resamp_data1
  ## obtaining the coincidences
  #equal_module = []
  #for pos, module in enumerate(rat1_data):
  #  if module == rat2_data[pos]:
  #    equal_module.append(module)
  #  else:
  #    equal_module.append('none')
#
  #number_of_coinc = []
#
  #for n in range(16):
  #  # it is in samples, we want it in seconds
  #  number_of_coinc.append(equal_module.count(n)*self.sample_time)
#
#
#
  #de#f load_tracking_data(self, dframe, sampling_freq):
#
  #  df_track['Accumulated Time'] = df_track['Accumulated Time']*self.sampling_freq
  #  df_track['Accumulated Time'] = df_track['Accumulated Time'].round(0)*self.sample_time
  #  df_track['T0'] = df_track['Accumulated Time'].shift(1)
  #  df_track['T1'] = df_track['Accumulated Time']
  #  df_track.fillna(0, inplace = True)
  #  print(df_track)
  #  df_track['Ttotal'] = df_track['T1'] - df_track['T0']
  #  df_track['Samples'] = df_track['Ttotal']*self.sampling_freq
  #  df_track['Samples'] = df_track['Samples'].astype(int)
  #  df_track['Module #'] = df_track['Module #'].astype(int)
  #  print(df_track)
  #  mod_arr = df_track['Module #'].to_numpy()
  #  samp_arr = df_track['Samples'].to_numpy()
  #  mod_samp = np.vstack((mod_arr, samp_arr)).T



if __name__=="__main__":
     app = QApplication(sys.argv)
     w = MyForm()
     w.show

     sys.exit(app.exec())

