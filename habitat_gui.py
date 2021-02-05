
import os
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import xlrd

#import statsmodels.api as sm
#from statsmodels.formula.api import ols
#from statsmodels.stats.anova import anova_lm
#from statsmodels.stats.weightstats import ttest_ind as wttest
#import time

from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QFileDialog, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QPushButton, QErrorMessage
from PyQt5.QtCore import pyqtSlot

from habitat_tracking import *
from elements import tunnel, coincidences_excel

#import matplotlib.pyplot as plt
#import matplotlib.backends.backend_pdf
from datetime import datetime

#import xlrd

#from pathlib import Path


class MyForm(QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_Habitat_tracking()
    self.ui.setupUi(self)
    # Timer
    self.flag_timer = False
    self.timer = QtCore.QTimer(self)
    self.time = QtCore.QTime(0,0,0,0)
    # Tunnels and other buttons
    self.ui.pb_tunnel_1.clicked.connect(self.tunnel_1)
    self.ui.pb_tunnel_2.clicked.connect(self.tunnel_2)
    self.ui.pb_tunnel_3.clicked.connect(self.tunnel_3)
    self.ui.pb_tunnel_4.clicked.connect(self.tunnel_4)
    self.ui.pb_tunnel_5.clicked.connect(self.tunnel_5)
    self.ui.pb_tunnel_6.clicked.connect(self.tunnel_6)
    self.ui.pb_tunnel_7.clicked.connect(self.tunnel_7)
    self.ui.pb_tunnel_8.clicked.connect(self.tunnel_8)
    self.ui.pb_tunnel_9.clicked.connect(self.tunnel_9)
    self.ui.pb_start.clicked.connect(self.start_time)
    self.ui.pb_pause.clicked.connect(self.pause_time)
    self.ui.pb_stop.clicked.connect(self.finish_recording)
    self.ui.pb_export_excel.clicked.connect(self.export_excel)

    # Tracking pannel
    self.ui.ButtonAddFirstExcel.clicked.connect(self.selectFirstFile)
    self.ui.ButtonDeleteFirstExcel.clicked.connect(self.delFirstFile)
    self.ui.ButtonAddSecondExcel.clicked.connect(self.selectSecondFile)
    self.ui.ButtonDeleteSecondExcel.clicked.connect(self.delSecondFile)

    self.ui.ButtonRunAll.clicked.connect(self.runTrackingAnalysis)
    #self.ui.ButtonClearFigures.clicked.connect(self.closeFigures)
    #self.ui.Button2PDF.clicked.connect(self.print2pdf)
    #self.ui.Button2PNG.clicked.connect(self.print2png)
    self.freq_list_results = []

    # Error message (it is necessary to initialize it too)
    self.error_msg = QErrorMessage()
    self.error_msg.setWindowTitle("Error")
    self.show()

    self.sample_time = 0.05
    self.sampling_freq = 1/self.sample_time

  def selectFirstFile(self):
    file_name, _ = QFileDialog.getOpenFileName(self,
                                     'Select file',
                                     './',
                                     'Excel Files (*.xls *.xlsx)')
    if file_name:
      self.ui.labelFirstFile.setText(file_name)
    else:
      self.error_msg.showMessage("It is necessary to select a file")

  def delFirstFile(self):
    self.ui.labelFirstFile.clear()

  def selectSecondFile(self):
    file_name, _ = QFileDialog.getOpenFileName(self,
                                     'Select file',
                                     './',
                                     'Excel Files (*.xls *.xlsx)')
    if file_name:
      self.ui.labelSecondFile.setText(file_name)
    else:
      self.error_msg.showMessage("It is necessary to select a file")

  def delSecondFile(self):
    self.ui.labelSecondFile.clear()

  def runTrackingAnalysis(self):
    self.resamp_data1, self.time_l1 = self.load_tracking_data(self.ui.labelFirstFile.text())
    self.resamp_data2, self.time_l2 = self.load_tracking_data(self.ui.labelSecondFile.text())
    self.calc_tracking_coinc()

  def load_tracking_data(self, file_name):
    df_track = pd.read_excel(file_name, 'Tracking', usecols = 'D,E', header = 1)
    df_track.dropna(how ='any', inplace = True)
    print(df_track)
    df_track['Accumulated Time'] = df_track['Accumulated Time']*self.sampling_freq
    df_track['Accumulated Time'] = df_track['Accumulated Time'].round(0)*self.sample_time
    df_track['T0'] = df_track['Accumulated Time'].shift(1)
    df_track['T1'] = df_track['Accumulated Time']
    df_track.fillna(0, inplace = True)
    print(df_track)
    df_track['Ttotal'] = df_track['T1'] - df_track['T0']
    df_track['Samples'] = df_track['Ttotal']*self.sampling_freq
    df_track['Samples'] = df_track['Samples'].astype(int)
    df_track['Module #'] = df_track['Module #'].astype(int)
    print(df_track)
    mod_arr = df_track['Module #'].to_numpy()
    samp_arr = df_track['Samples'].to_numpy()
    mod_samp = np.vstack((mod_arr, samp_arr)).T

    resamp_data = []
    time_list = []
    t_time = self.sample_time
    for (x,y) in mod_samp:
      for i in range(y):
        resamp_data.append(x)
        time_list.append(t_time)
        t_time = t_time + self.sample_time

    return resamp_data, time_list

  def calc_tracking_coinc(self):
    # making recordings of the same lenght
    if np.size(self.resamp_data2) < np.size(self.resamp_data1):
      rat1_data = self.resamp_data1[:np.size(self.resamp_data2)]
      rat2_data = self.resamp_data2
    else:
      rat2_data = self.resamp_data2[:np.size(self.resamp_data1)]
      rat1_data = self.resamp_data1
    # obtaining the coincidences
    equal_module = []
    for pos, module in enumerate(rat1_data):
      if module == rat2_data[pos]:
        equal_module.append(module)
      else:
        equal_module.append('none')

    number_of_coinc = []

    for n in range(16):
      # it is in samples, we want it in seconds
      number_of_coinc.append(equal_module.count(n)*self.sample_time)

    # plotting colormap and bars plot together
    # https://stackoverflow.com/questions/18266642/multiple-imshow-subplots-each-with-colorbar/18278607
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18,9))

    ax1.bar(range(16), number_of_coinc)
    ax1.set_title('Shared time (s) in each module')
    ax1.set_xticks(np.arange(0, 16, 1))
    ax1.set_ylabel('Time (s)')
    ax1.set_xlabel('module number')
    # export coincidencies to excel
    coincidences_excel(number_of_coinc, equal_module, self.sample_time)

    # Heat map for times per module
    times_matrix = np.array(number_of_coinc).reshape(4, 4)
    ax2.set_title('Shared time (s) in each module')
    locations = (0, 1, 2, 3)
    xlabels = ('4', '3', '2', '1')
    plt.xticks(locations, xlabels)
    ylabels = ('A', 'B', 'C', 'D')
    plt.yticks(locations, ylabels)
    cell_map = ax2.imshow(times_matrix, cmap='hot')
    cbar = plt.colorbar(cell_map)
    plt.draw()
    plt.show()

  def timepassed(self):
    #time = QtCore.QTime.currentTime()
    if self.flag_timer:
      self.time = self.time.addMSecs(self.ui.sb_speed.value()*1000)
    text = self.time.toString('h:mm:ss:z')
    self.ui.lcdTime.display(text)

  def tunnel_1(self):
    if self.tunnel_1:
      self.ui.pb_tunnel_1.setStyleSheet("background-color: rgb(193, 193, 193)")
      self.tunnel_1 = False
      self.all_tunnels[0].stop_time()
      self.enable_buttons()
    else:
      self.ui.pb_tunnel_1.setStyleSheet("background-color: red")
      self.tunnel_1 = True
      self.all_tunnels[0].start_time()
      self.disable_buttons()
      self.ui.pb_tunnel_1.setEnabled(True)

  def tunnel_2(self):
    if self.tunnel_2:
      self.ui.pb_tunnel_2.setStyleSheet("background-color: rgb(193, 193, 193)")
      self.tunnel_2 = False
      self.all_tunnels[1].stop_time()
      self.enable_buttons()
    else:
      self.ui.pb_tunnel_2.setStyleSheet("background-color: red")
      self.tunnel_2 = True
      self.all_tunnels[1].start_time()
      self.disable_buttons()
      self.ui.pb_tunnel_2.setEnabled(True)

  def tunnel_3(self):
    if self.tunnel_3:
      self.ui.pb_tunnel_3.setStyleSheet("background-color: rgb(193, 193, 193)")
      self.tunnel_3 = False
      self.all_tunnels[2].stop_time()
      self.enable_buttons()
    else:
      self.ui.pb_tunnel_3.setStyleSheet("background-color: red")
      self.tunnel_3 = True
      self.all_tunnels[2].start_time()
      self.disable_buttons()
      self.ui.pb_tunnel_3.setEnabled(True)

  def tunnel_4(self):
    if self.tunnel_4:
      self.ui.pb_tunnel_4.setStyleSheet("background-color: rgb(193, 193, 193)")
      self.tunnel_4 = False
      self.all_tunnels[3].stop_time()
      self.enable_buttons()
    else:
      self.ui.pb_tunnel_4.setStyleSheet("background-color: red")
      self.tunnel_4 = True
      self.all_tunnels[3].start_time()
      self.disable_buttons()
      self.ui.pb_tunnel_4.setEnabled(True)

  def tunnel_5(self):
    if self.tunnel_5:
      self.ui.pb_tunnel_5.setStyleSheet("background-color: rgb(193, 193, 193)")
      self.tunnel_5 = False
      self.all_tunnels[4].stop_time()
      self.enable_buttons()
    else:
      self.ui.pb_tunnel_5.setStyleSheet("background-color: red")
      self.tunnel_5 = True
      self.all_tunnels[4].start_time()
      self.disable_buttons()
      self.ui.pb_tunnel_5.setEnabled(True)

  def tunnel_6(self):
    if self.tunnel_6:
      self.ui.pb_tunnel_6.setStyleSheet("background-color: rgb(193, 193, 193)")
      self.tunnel_6 = False
      self.all_tunnels[5].stop_time()
      self.enable_buttons()
    else:
      self.ui.pb_tunnel_6.setStyleSheet("background-color: red")
      self.tunnel_6 = True
      self.all_tunnels[5].start_time()
      self.disable_buttons()
      self.ui.pb_tunnel_6.setEnabled(True)

  def tunnel_7(self):
    if self.tunnel_7:
      self.ui.pb_tunnel_7.setStyleSheet("background-color: rgb(193, 193, 193)")
      self.tunnel_7 = False
      self.all_tunnels[6].stop_time()
      self.enable_buttons()
    else:
      self.ui.pb_tunnel_7.setStyleSheet("background-color: red")
      self.tunnel_7 = True
      self.all_tunnels[6].start_time()
      self.disable_buttons()
      self.ui.pb_tunnel_7.setEnabled(True)

  def tunnel_8(self):
    if self.tunnel_8:
      self.ui.pb_tunnel_8.setStyleSheet("background-color: rgb(193, 193, 193)")
      self.tunnel_8 = False
      self.all_tunnels[7].stop_time()
      self.enable_buttons()
    else:
      self.ui.pb_tunnel_8.setStyleSheet("background-color: red")
      self.tunnel_8 = True
      self.all_tunnels[7].start_time()
      self.disable_buttons()
      self.ui.pb_tunnel_8.setEnabled(True)

  def tunnel_9(self):
    if self.tunnel_9:
      self.ui.pb_tunnel_9.setStyleSheet("background-color: rgb(193, 193, 193)")
      self.tunnel_9 = False
      self.all_tunnels[8].stop_time()
      self.enable_buttons()
    else:
      self.ui.pb_tunnel_9.setStyleSheet("background-color: red")
      self.tunnel_9 = True
      self.all_tunnels[8].start_time()
      self.disable_buttons()
      self.ui.pb_tunnel_9.setEnabled(True)


  def start_time(self):
    self.enable_buttons()
    self.ui.pb_start.setDisabled(True)

    self.flag_timer = True
    self.timer.timeout.connect(self.timepassed)
    self.timer.start(1000)


    self.tunnel_1 = False
    self.tunnel_2 = False
    self.tunnel_3 = False
    self.tunnel_4 = False
    self.tunnel_5 = False
    self.tunnel_6 = False
    self.tunnel_7 = False
    self.tunnel_8 = False
    self.tunnel_9 = False
    self.resume = False

    # Creating tunnel instances and putting them all together in a list
    self.all_tunnels = []
    now_time = datetime.now()
    for i in range(9):
      tunnel_i = tunnel(i+1, now_time, self.ui.sb_speed.value())
      self.all_tunnels.append(tunnel_i)

  def finish_recording(self):
    self.flag_timer = False
    self.disable_buttons()
    now_time = datetime.now()
    for tunnel_i in self.all_tunnels:
      tunnel_i.finish_recording(now_time)
    self.ui.pb_export_excel.setEnabled(True)
    self.ui.pb_export_excel.setStyleSheet("background-color: green")

  def pause_time(self):
    now_time = datetime.now()
    # Pausing
    if (self.resume == False):
      self.flag_timer = False
      self.disable_buttons()
      self.ui.pb_pause.setEnabled(True)
      self.ui.pb_pause.setText("RESUME")
      self.ui.pb_pause.setStyleSheet("background-color: green")
      for tunnel_i in self.all_tunnels:
        tunnel_i.pause_time(self.resume, now_time)
      self.resume = True
    # Resuming
    else:
      self.flag_timer = True
      self.enable_buttons()
      self.ui.pb_pause.setText("PAUSE")
      self.ui.pb_pause.setStyleSheet("background-color: rgb(193, 193, 193)")
      for tunnel_i in self.all_tunnels:
        tunnel_i.pause_time(self.resume, now_time)
      self.resume = False

  def export_excel(self):
    file_name = self.ui.txt_animal_id.toPlainText()
    if file_name == '' :
      self.error_msg.showMessage("Please, select an Animal ID")

    else:
      # DataFrame for the times
      tun = []
      t_start = []
      dura = []
      for tunnel_i in self.all_tunnels:
        for one_time in tunnel_i.times:
          tun.append(one_time[0])
          t_start.append(one_time[1])
          dura.append(one_time[2])

      dict_times = {'tunnel': tun, 'time (s)': t_start, 'duration': dura}
      df_times = pd.DataFrame(dict_times)
      #print(df_times.round(1))
      df_t_sorted = df_times.sort_values(by=['time (s)'], ascending = True)
      #print(' ')
      #print(df_t_sorted.round(1))

      # DataFrames for the stats
      tun = []
      f_t = []
      uses = []
      av_t = []
      sd_t = []
      max_t = []
      sum_t = []
      for tunnel_i in self.all_tunnels:
        tun.append(tunnel_i.stats[0])
        f_t.append(tunnel_i.stats[1])
        uses.append(tunnel_i.stats[2])
        av_t.append(tunnel_i.stats[3])
        sd_t.append(tunnel_i.stats[4])
        max_t.append(tunnel_i.stats[5])
        sum_t.append(tunnel_i.stats[6])

      dict_stats = {'tunnel': tun, '1st_time': f_t, 'uses': uses,
                    'av_dur': av_t, 'sd_time': sd_t, 'max_dur': max_t,
                    'total_dur': sum_t}
      df_stats = pd.DataFrame(dict_stats)
      #print(' ')
      #print(df_stats.round(1))
      #print(' ')

      # Export dataframes to excel
      writer = pd.ExcelWriter(file_name + '.xlsx', engine='xlsxwriter')

      frames = {'times_by_tunnel': df_times.round(1), 'times_by_start': df_t_sorted.round(1),
                'stats': df_stats.round(1)}
      for sheet, frame in frames.items():
        frame.to_excel(writer, sheet_name = sheet, index = False)

      writer.save()


  def disable_buttons(self):
    self.ui.pb_pause.setDisabled(True)
    self.ui.pb_stop.setDisabled(True)
    self.ui.pb_start.setDisabled(True)
    self.ui.pb_tunnel_1.setDisabled(True)
    self.ui.pb_tunnel_2.setDisabled(True)
    self.ui.pb_tunnel_3.setDisabled(True)
    self.ui.pb_tunnel_4.setDisabled(True)
    self.ui.pb_tunnel_5.setDisabled(True)
    self.ui.pb_tunnel_6.setDisabled(True)
    self.ui.pb_tunnel_7.setDisabled(True)
    self.ui.pb_tunnel_8.setDisabled(True)
    self.ui.pb_tunnel_9.setDisabled(True)
    self.ui.sb_speed.setDisabled(True)

  def enable_buttons(self):
    self.ui.pb_pause.setEnabled(True)
    self.ui.pb_stop.setEnabled(True)
    self.ui.pb_tunnel_1.setEnabled(True)
    self.ui.pb_tunnel_2.setEnabled(True)
    self.ui.pb_tunnel_3.setEnabled(True)
    self.ui.pb_tunnel_4.setEnabled(True)
    self.ui.pb_tunnel_5.setEnabled(True)
    self.ui.pb_tunnel_6.setEnabled(True)
    self.ui.pb_tunnel_7.setEnabled(True)
    self.ui.pb_tunnel_8.setEnabled(True)
    self.ui.pb_tunnel_9.setEnabled(True)



if __name__=="__main__":
     app = QApplication(sys.argv)
     w = MyForm()
     w.show

     sys.exit(app.exec())
