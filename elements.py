import numpy as np
import pandas as pd
import time
from datetime import datetime
import xlsxwriter

def coincidences_excel(total_times, module_tracking, sample_time):

    # DataFrame for the times
    timestamps = np.arange(0,len(module_tracking)*sample_time, sample_time)
    dict_totalpermodule = {'module': np.arange(16), 'time(s)': total_times}
    dict_tracking = {'time(s)': timestamps, 'module': module_tracking}
    df_timeper_module = pd.DataFrame(dict_totalpermodule)
    df_time_track_together = pd.DataFrame(dict_tracking)

    # Export dataframes to excel
    writer = pd.ExcelWriter('coincidences_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.xlsx', engine='xlsxwriter')
    frames = {'total_by_module': df_timeper_module.round(2), 'module_coincidences_tracking': df_time_track_together.round(2)}
    for sheet, frame in frames.items():
      frame.to_excel(writer, sheet_name = sheet, index = False)
    writer.save()


class tunnel():

    def __init__(self, tunnel_n, now_time, speed):
        self.tunnel_number = tunnel_n
        self.total_time = datetime.now() - datetime.now()
        self.paused_time = datetime.now() - datetime.now()
        self.record_start_time = now_time
        self.times = []
        self.speed = speed


    def set_number(self, t_n):
        self.tunnel_number = t_n

    def set_position(self, t_pos):
        self.position = t_pos # (x,y) coordinates

    def set_size(self, t_size):
        self.size = t_size # height * width

    def set_place(self, position):
        self.position = position
        #self.y = y

    def start_time(self):
        self.init_time = datetime.now()

    def pause_time(self, resume, now_time):
        if (resume == False):
            self.begin_paused_time = now_time
        else:
            self.paused_time = self.paused_time + (now_time - self.begin_paused_time)

    def stop_time(self):
        current_time = datetime.now()
        passed_time = current_time - self.init_time
        abs_start_time = self.init_time - self.paused_time - self.record_start_time
        self.times.append((self.tunnel_number, abs_start_time.total_seconds()*self.speed,
                            passed_time.total_seconds()*self.speed))
        a = 0

    def finish_recording(self, now_time):
        self.total_time = (now_time - self.record_start_time).total_seconds()*self.speed
        self.calc_stats()

    def calc_stats(self):
        if not self.times:
            self.stats = [self.tunnel_number, 0, 0, 0, 0, 0, 0]
        else:
            times_a = np.asarray(self.times)
            first_time = times_a[0][1] # first time the animal enters the tunnel
            uses = np.size(times_a[:,1]) # number of times the animal entered the tunnel
            max_dur = max(times_a[:,2]) # max duration
            av_time = times_a[:,2].mean(axis=0) # average time spent in the tunnel
            sd_time = times_a[:,2].std(axis=0)
            sum_time = times_a[:,2].sum(axis=0)
            self.stats = [self.tunnel_number, first_time, uses, av_time, sd_time, max_dur, sum_time]
