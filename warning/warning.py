import numpy as np
import streamlit as st
import time

def warning_line(line_mode,x_actual,boxes,i,initial_size,judge_space):
    # print(initial_size)
    if line_mode == "垂直":
        x_scale = initial_size[1]/704
        y_scale = initial_size[0]/704
        box_prev = np.array([boxes[i-1][0]* x_scale, boxes[i-1][1]* y_scale,boxes[i-1][2]* x_scale,boxes[i-1][3]* y_scale])
        box_after = np.array([boxes[i][0]* x_scale, boxes[i][1]* y_scale,boxes[i][2]* x_scale,boxes[i][3]* y_scale ])

        if (x_actual - (box_prev[0]+ box_prev[2]/2) )*(x_actual - (box_after[0]+box_prev[2]/2 )) <= 0:
            judge_space.write("<font color='red'>設定した線を超えました</font>", unsafe_allow_html=True)
            time.sleep(5)
        else:
            judge_space.write("異常はありません")





