import os
import pandas as pd
import numpy as np
import openpyxl

TEAMS = ['TOR', 'BAL', 'TB', 'BOS', 'NYY', 
         'CLE', 'KC', 'DET', 'MIN', 'CWS', 
         'LAA', 'HOU', 'OAK', 'SEA', 'TEX',
         'ATL', 'MIA', 'NYM', 'WSH', 'PHI',
         'MIL', 'STL', 'CHC', 'PIT', 'CIN',
         'AZ', 'LAD', 'SF', 'SD', 'COL']

STATCAST_MEASURE_Y = 50
HOME_PLATE_Y = 17/12
RAD = 57.325

def release_param_calc(vx0, vy0, vz0, ax, ay, az, release_pos_y):
    vyR = -np.sqrt(vy0.to_numpy() ** 2 + 2 * ay.to_numpy() * (release_pos_y.to_numpy() - STATCAST_MEASURE_Y))
    tR = (vyR - vy0) / ay
    vxR = vx0 + ax * tR
    vzR = vz0 + az * tR
    release_angle = np.arctan(vzR / np.sqrt(vxR ** 2 + vyR ** 2)) * RAD
    release_direction = np.arctan(-vxR / vyR) * RAD
    return vxR, vyR, vzR, release_angle, release_direction

def flight_time_calc(ay, release_pos_y, vyR):
    return (-vyR - np.sqrt(vyR ** 2 + 2 * ay.to_numpy() * (release_pos_y.to_numpy() - HOME_PLATE_Y))) / ay.to_numpy()

def spin_calc(spin_rate, spin_axis, plate_x, plate_z, flight_time):
    gyro_spin = 
    back_spin = 
    side_spin = 
    return gyro_spin, back_spin, side_spin

def tunnel_point_calc(traj_calculator_excel, pitch_data_df):
    pass


if __name__ == '__main__':
    os.chdir("..")
    for team in TEAMS:
        for pitcher_csv in os.listdir(os.getcwd()+'/data/'+team):
            pitch_data = pd.read_csv(os.getcwd()+'/data/'+team+'/'+pitcher_csv)
            vx0, vy0, vz0, ax, ay, az, release_pos_y = pitch_data['vx0'], pitch_data['vy0'], pitch_data['vz0'], pitch_data['ax'], pitch_data['ay'], pitch_data['az'], pitch_data['release_pos_y']
            vxR, vyR, vzR, angleR, directionR = release_param_calc(vx0, vy0, vz0, ax, ay, az, release_pos_y)
            flight_time = flight_time_calc(ay, release_pos_y, vyR)
            spin_rate, spin_axis, plate_x, plate_z = pitch_data['release_spin_rate'], pitch_data['spin_axis'], pitch_data['plate_x'], pitch_data['plate_z']
            gyro_spin, back_spin, side_spin = spin_calc(spin_rate, spin_axis, plate_x, plate_z, flight_time)
            calculated_df = pd.DataFrame({'vxR': vxR,
                                    'vyR': vyR,
                                    'vzR': vzR,
                                    'angleR': angleR,
                                    'directionR': directionR,
                                    'flight_time': flight_time,
                                    'gyro_spin': gyro_spin,
                                    'back_spin': back_spin,
                                    'side_spin': side_spin})
            pitch_data = pd.concat([pitch_data, calculated_df], axis=1)
            traj_calculator = openpyxl.load_workbook('src/TrajectoryCalculator-new-3D-May2021.xlsx').worksheets[0]
            tunnel_point_calc(traj_calculator, pitch_data)
