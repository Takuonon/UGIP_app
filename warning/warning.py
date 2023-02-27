import numpy as np
import streamlit as st
import time

def warning_line(line_mode,x_actual,y_actual,boxes,i,initial_size,judge_space,x1,y1):
    # print(initial_size)
    x_scale = initial_size[1]/704
    y_scale = initial_size[0]/704
    box_prev = np.array([boxes[i-1][0]* x_scale, boxes[i-1][1]* y_scale,boxes[i-1][2]* x_scale,boxes[i-1][3]* y_scale])
    box_after = np.array([boxes[i][0]* x_scale, boxes[i][1]* y_scale,boxes[i][2]* x_scale,boxes[i][3]* y_scale ])

    if line_mode == "垂直":
        if (x_actual - (box_prev[0]+ box_prev[2]/2) )*(x_actual - (box_after[0]+box_prev[2]/2 )) <= 0:
            judge_space.write("<font color='red'>設定した線を超えました</font>", unsafe_allow_html=True)
            time.sleep(3)
        else:
            judge_space.write("異常はありません")

    elif line_mode == "水平":
        if (y_actual - (box_prev[1]+ box_prev[3]/2) )*(y_actual - (box_after[1]+box_prev[3]/2 )) <= 0:
            judge_space.write("<font color='red'>設定した線を超えました</font>", unsafe_allow_html=True)
            time.sleep(3)
        else:
            judge_space.write("異常はありません") 

    else:
        middle_x_prev = box_prev[0]+ box_prev[2]/2
        middle_y_prev = box_prev[1]+ box_prev[3]/2
        middle_x_after = box_after[0]+box_prev[2]/2
        middle_y_after = box_after[1]+box_prev[3]/2

        if (middle_y_prev-line(x1,y1,x_actual,0,middle_x_prev))* (middle_y_after-line(x1,y1,x_actual,0,middle_x_after))<= 0:
            judge_space.write("<font color='red'>設定した線を超えました</font>", unsafe_allow_html=True)
            time.sleep(3)
        else:
            judge_space.write("異常はありません")         
        

def line(x1,y1,x2,y2,x):
    print(x1)
    print(y1)
    print(x2)
    print(y2)
    if (x2-x1) != 0:
        y = (y2-y1)*x/(x2-x1)-(y2-y1)*x1/(x2-x1) + y1
    else:
        y = y1 
    return y
