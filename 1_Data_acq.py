# CAN 데이터 및 Camera 영상처리 raw data를 수집
# UDP 소켓통신을 이용하여 raw data 수집 및 가공

import numpy as np
import socket
import pandas as pd

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("127.0.0.1", 1234))
# 수집되는 데이터의 순서에 따라 indexing
index = {"left", "right", "bottom", "top", "lat", "long", "heading", "angle", "width", "ground truth"}

while True:
    data, addr = sock.recvfrom(10240)
    
#     left - bounding box 좌측변의 x좌표(-1.00,1.00)
#     right - bounding box 우측변의 x좌표(-1.00,1.00)
#     top - bounding box 상측변의 y좌표(-1.00,1.00)
#     bottom - bounding box 하측변의 y좌표(-1.00,1.00)
#     - 이에, UDP packet 전송을 위하여 uint8 변환시 데이터 손실 최소화를 위하여 (기초데이터+1)*100로 가공되어 (0,255)범위에서 1byte로
#     전송되는 상황임
#     - 수신된 각각 1byte 데이터인 영상 내 bounding box의 x좌표(for left & right), y좌표(for top & bottom)를 원신호로 재가공
    left, right, bottom, top = data[0] / 100 - 1, data[1] / 100 - 1, data[2] / 100 - 1, data[3] / 100 - 1
    left, right, bottom, top = round(left, 2), round(right, 2), round(bottom, 2), round(top, 2)
    
    
    lat = (data[4] * 256*256*256 + data[5] * 65536 + data[6] * 256 + data[7]) - 1000
    long = (data[8] * 256*256*256 + data[9] * 65536 + data[10] * 256 + data[11]) - 1000
    heading = (data[12] * 256*256*256 + data[13] * 65536 + data[14] * 256 + data[15]) - 1000
    width = data[16] * 256*256*256 + data[17] * 65536 + data[18] * 256 + data[19]
    angle = data[20]
    
    gt = (data[21] * 256*256*256 + data[22] * 65536 + data[23] * 256 + data[24]) / 100
    frame = [left, right, bottom, top, lat, long, heading, angle, width, gt]
    df = pd.DataFrame(frame)
    df = np.transpose(df)
    df.to_csv("C:/Users/JHYim/PycharmProjects/KSAE_2019_2/data/0_rawdata-1.csv", mode='a', index=False, header=False)





