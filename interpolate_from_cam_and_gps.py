import pandas as pd
from scipy.interpolate import splrep, splev
import numpy as np

gps_csv = pd.read_csv('gps.csv')
cam_csv = pd.read_csv('cam.csv')

gps_time = gps_csv['grabMsec'].values
nord = gps_csv['nord'].values
east = gps_csv['east'].values
alt = gps_csv['alt'].values
yaw = gps_csv['yaw'].values

nord_interp = []
east_interp = []
alt_interp = []
yaw_interp = []

# Интерполировать для каждой "времени" в файле cam_csv
for msec in cam_csv['grabMsec']:

    # Интерполяция с использованием splrep и splev
    tck_nord = splrep(gps_time, nord, s=0)
    tck_east = splrep(gps_time, east, s=0)
    tck_alt = splrep(gps_time, alt, s=0)
    tck_yaw = splrep(gps_time, yaw, s=0)

    nord_val = splev(msec, tck_nord)
    east_val = splev(msec, tck_east)
    alt_val = splev(msec, tck_alt)
    yaw_val = splev(msec, tck_yaw)

    nord_interp.append(nord_val if np.isfinite(nord_val) else None)
    east_interp.append(east_val if np.isfinite(east_val) else None)
    alt_interp.append(alt_val if np.isfinite(alt_val) else None)
    yaw_interp.append(yaw_val if np.isfinite(yaw_val) else None)

"""
SourceFile = []
SourceFilePath = "C:/Users/danil/Desktop/Project5/Videos/images/"
episode = cam_csv['episode'].values

j = 0
previous_episode = episode[0]
for i in range(len(cam_csv['grabNumber'])):
    if (previous_episode != episode[i]):
        j = 0
    SourceFile.append(SourceFilePath + episode[i] + str(j) + ".png")
    j += 1
    previous_episode = episode[i]
"""

SourceFile = []
SourceFilePath = "C:/Users/danil/Desktop/Project5/Videos/images/"
num = 100000

for i in range(len(cam_csv['grabNumber'])):
    img_num = str(num + i + 1)
    img_num = img_num[1:]
    SourceFile.append(SourceFilePath + img_num  +".png")


# новый csv с результатами
output_data = {
    'grabNumber': cam_csv['grabNumber'],
    'grabMsec': cam_csv['grabMsec'],
    'episode': cam_csv['episode'],
    'nord': nord_interp,
    'east': east_interp,
    'alt': alt_interp,
    'yaw': yaw_interp,
}

# csv для импорта metadata в картинки
exif_output_data = {
    'SourceFile': SourceFile,
    'GPSLatitude': nord_interp,
    'GPSLatitudeRef': nord_interp,
    'GPSLongitude': east_interp,
    'GPSLongitudeRef': east_interp,
    'GPSAltitude': alt_interp,
    'GPSAltitudeRef': alt_interp
}

output_df = pd.DataFrame(output_data)
output_df.to_csv('output.csv', index=False)

exif_output_df = pd.DataFrame(exif_output_data)
exif_output_df.to_csv('exif_output.csv', index=False)