import os
import sys
import tempfile
import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from det_box import run

def detect_object2(frame):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    confidence = 0

    #画像を一時ファイルに保存
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        plt.imsave(tmp_file.name, frame)
        tmp_file.flush()
        det = run(source=tmp_file.name) 
    
    if det is None:   
        return None 

    x1 = det[0][0]
    y1 = det[0][1]
    x2 = det[0][2]
    y2 = det[0][3]
    confidence = det[0][4]

    # 一時ファイルを削除
    os.unlink(tmp_file.name)

    box = np.array([x1, y1, x2 - x1, y2 - y1])
    label = '%.2f' % confidence
    label = '%s: %s' % ("wheelchair", label)
    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1) # fontScale: 0.5, thickness: 1
    left, top, width_, height_ = box
    top = max(top, labelSize[1])

    cv2.rectangle(frame, (int(box[0]), int(box[1])),(int(x2),int(y2)), color=(0, 255, 0), thickness=3)
    cv2.rectangle(frame, (int(left), int(top - labelSize[1])), (int(left + labelSize[0]), int(top + baseLine)),(255, 255, 255), cv2.FILLED)
    cv2.putText(frame, label, (int(left), int(top)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    return confidence, box, frame

def get_first_frame(cap):
    #TODO このせいでtrack_objectで読み込むフレームのスタート位置がズレてる
    if not cap.isOpened():
        print ("Could not open video")
        sys.exit()
    ok, frame = cap.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
    detected_object = detect_object2(frame)

    #車椅子を検出できなかったときの例外処理
    if detected_object is None:
        st.write("<p style='font-size: 20px; color: red; font-weight: bold; text-align: center;'>車椅子が検出されませんでした</p>", unsafe_allow_html=True)
        sys.exit()

    resized_frame = convert_frame(detected_object[2], frame.shape)
    return resized_frame
    
def track_object2(cap, space):
    tracker = cv2.TrackerMIL_create()
    # Exit if video not opened.
    if not cap.isOpened():
        print ("Could not open video")
        sys.exit()
 
    #Read first frame.
    ok, frame = cap.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()

    #箱付きのimageを格納する配列
    frames = np.empty((50000,704, 704, 3))
    boxes_result = np.empty((50000,4))

    #サイズの取得
    initial_size = frame.shape

    #入力のサイズを調整   
    frame_initial = cv2.resize(frame, dsize=(704, 704), interpolation=cv2.INTER_AREA)

    detected_object = detect_object2(frame_initial)

    #車椅子が検出できなかった際の例外処理
    #これ以前に実行されるエラー処理でコードが終了するため、実際には到達しない。
    if detected_object is None:
        return None

    box = detected_object[1]
    ok = tracker.init(frame_initial, (int(box[0]),int(box[1]),int(box[2]),int(box[3])))
    i = 0

    while True:
        # Read a new frame
        ok, frame = cap.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        frame = cv2.resize(frame, dsize=(704, 704), interpolation=cv2.INTER_AREA)
        ok, bbox = tracker.update(frame)
        print (ok)
        print (bbox)
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,255,0), thickness=3)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, "KCF" + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

        frames[i] = frame
        boxes_result[i] = np.array(bbox)

        if i%4 == 0:
            space.write("処理中です")
        if i%4 == 1:
            space.write("処理中です・")
        if i%4 == 2:
            space.write("処理中です・・")  
        if i%4 == 3:
            space.write("処理中です・・・") 
        i +=1

    return frames, i, initial_size, boxes_result

def convert_frame(frame, initial_size):
    # float64の場合、ビット深度を変換(if文は念のため)
    if frame.dtype == np.float64:
        if np.max(frame) <= 1.0:
            frame = (frame * 255.0).astype(np.uint8)
        else:
            frame = frame.astype(np.uint8)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   
    resized_frame = cv2.resize(frame, (initial_size[1],initial_size[0]), interpolation=cv2.INTER_AREA)
    return resized_frame    