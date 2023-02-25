import cv2
import numpy as np
import os
import sys
import streamlit as st

#arrayにした画像(frame)が引数
def detect_object(frame):
    cfg_path = os.path.abspath('yolo/yolov4.cfg')
    weights_path = os.path.abspath('yolo/yolov4.weights')
    names_path = os.path.abspath('yolo/coco.names')

    # モデルの作成
    net = cv2.dnn_DetectionModel(cfg_path, weights_path)
    net.setInputSize(704, 704)
    net.setInputScale(1.0 / 255)
    net.setInputSwapRB(True)

    #入力のサイズを調整
    frame = cv2.resize(frame, dsize=(704, 704), interpolation=cv2.INTER_AREA)

    # yolo/coco.namesを読み込む
    with open(names_path, 'rt') as f:
        names = f.read().rstrip('\n').split('\n')

    #classes: 検出された物体のクラスID
    #confidences: 精度(確率)
    #boxes: ボックス(左上x座標、左上y座標、幅、高さ)
    classes, confidences, boxes = net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)

    # for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
    #     print(classId, confidence, box)
    #     label = '%.2f' % confidence
    #     label = '%s: %s' % (names[classId], label)
    #     labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1) # fontScale: 0.5, thickness: 1
    #     # print(labelSize, baseLine)
    #     left, top, width, height = box
    #     # print("T:", top)
    #     top = max(top, labelSize[1])
    #     # print("MT:", top)
    #     cv2.rectangle(frame, box, color=(0, 255, 0), thickness=3)
    #     # Draw rectangle for labels
    #     cv2.rectangle(frame, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine),
    #                   (255, 255, 255), cv2.FILLED)
    #     cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    # return frame
    return classes, confidences, boxes


# def track_objects(frames):
#     #trackerの作成
#     print(cv2.__version__)
#     tracker = cv2.TrackerCSRT_create()

#     detections = {}
#     #trackするもんに関して足してく
#     current_id = 0
#     fps = 0

# #ここでframesの長さを渡したい
#     for i in range(10):
#         tracked_boxes = []
#         frame = frames[i]
#         classes, confidences, boxes = detect_object(frame)
#         for box in boxes:
#             tracked = False
#             for id, detection in detections.items():
#                 # 過去の検出結果と現在の検出結果を比較して、物体を追跡
#                 iou = intersection_over_union(box, detection["box"])
#                 if iou > 0.5:
#                     tracker.update(frame)
#                     tracked = True
#                     tracker_box = tracker.getObjects()[-1]
#                     tracked_boxes.append(tracker_box)
#                     detections[id]["box"] = tracker_box
#                     detections[id]["confidence"] = confidences[boxes.index(box)]
#                     detections[id]["age"] += 1
#                     break
#                 if not tracked:
#                 # 新規検出結果を追加
#                     id = current_id
#                     current_id += 1
#                     tracker.add(cv2.TrackerKCF_create(), frame, box)
#                     detections[id] = {"box": box, "confidence": confidences[boxes.index(box)], "age": 1}
#                     tracked_boxes.append(box)

#         # # 古い検出結果を削除
#         # #ここがよく分からない
#         # deleted_ids = []
#         # for id, detection in detections.items():
#         #     if detection["age"] > max_age:
#         #         deleted_ids.append(id)
#         # for id in deleted_ids:
#         #     del detections[id]

#         # 検出結果を表示
#         for id, detection in detections.items():
#             x, y, w, h = detection["box"]
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#             text = f"{classes[classes[boxes.index(detection['box'])]]}: {detection['confidence']:.2f}"
#             cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

#         # framesをボックスがついてるバージョンに入れ替え
#         frames[i] = frame

#     # 後処理
#     cv2.destroyAllWindows()
#     return frames

def track_objects(frames):
    print(cv2.__version__)

    # # 追跡対象の初期位置を取得
    # bbox_initial = cv2.selectROI("Tracking", frames[0], False)

    #箱付きのiamgeを格納してく配列
    results_image = np.empty((len(frames),704, 704, 3))

    #入力のサイズを調整   
    frame = cv2.resize(frames[0], dsize=(704, 704), interpolation=cv2.INTER_AREA)


   
    classes, confidences, boxes = detect_object(frame)
    
    # 追跡器を作成し、最初の位置で初期化
    tracker = cv2.TrackerKCF_create()
    bbox_init = tuple(map(int, boxes[0]))
    # print(bbox_init)
    tracker.init(frame, bbox_init)

    cv2.rectangle(frame, bbox_init, color=(0, 255, 0), thickness=3)
    results_image[0] = frame
    
    print(frame)
    print(results_image[0])

    
    # 追跡結果を保存するリスト
    #resultsはboxの座標を格納する配列
    results = []
    results.append(bbox_init)
    
    # # iouのしきい値
    # iou_threshold = 0.5

    print(len(frames))
    
    # # フレームごとに処理を実行
    # for i in range(1, 5):
        
    #     print(i)

    #     # 検出器で物体検出を実行
    #     classes, confidences, boxes = detect_object(frames[i])

    #     print(boxes)
    #     print("len_boxes", len(boxes))
        
    #     # 検出がなければ、前回の追跡結果を使用する
    #     if len(boxes) == 0:
    #         bbox = results[i - 1]
    #     else:
    #         # iouが最も高い検出を選択
    #         bbox = None
    #         max_iou = 0
            
    #         for box in boxes:
    #             iou = intersection_over_union(results[i - 1], box)
                
    #             if iou > max_iou and iou > iou_threshold:
    #                 bbox = box

    #                 max_iou = iou
            
    #         # iouがしきい値未満の場合は前回の追跡結果を使用する
    #         if bbox is None:
    #             bbox = results[i - 1]

    #         print(bbox)

    for i in range(1, 5):
        # 追跡器で位置を更新し、結果を保存する
        ok, bbox = tracker.update(frames[i])
        print(ok)
        print(bbox)
        if ok:
            results.append(bbox)
            print("here")
        else:
            results.append(results[i - 1])
    
        # 追跡結果をフレームに描画する
        bbox = tuple(map(int, bbox))
        frame_new = cv2.resize(frames[i], dsize=(704, 704), interpolation=cv2.INTER_AREA)
        print(bbox)
        cv2.rectangle(frame_new, bbox, color=(0, 255, 0), thickness=3)
        results_image[i] = frame_new

    return results, results_image

def get_first_frame(cap):
    #TODO このせいでtrack_objectで読み込むフレームのスタート位置がズレてるかも
    if not cap.isOpened():
        print ("Could not open video")
        sys.exit()
    ok, frame = cap.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
    return frame
    




def track_object2(cap):
    tracker = cv2.TrackerKCF_create()
        # Exit if video not opened.
    if not cap.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = cap.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()

    #箱付きのiamgeを格納してく配列
    #TODO このmax_framesはどっかでわかりやすく定義するのがいいかも
    frames = np.empty((50000,704, 704, 3))

    #サイズの取得
    initial_size = frame.shape
    

    #入力のサイズを調整   
    frame_initial = cv2.resize(frame, dsize=(704, 704), interpolation=cv2.INTER_AREA)

    classes, confidences, boxes = detect_object(frame_initial)
    bbox = boxes[0]
    ok = tracker.init(frame_initial, bbox)
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
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, "ooo" + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

        frames[i] = frame
        i +=1
 


        # # Display result
        # cv2.imshow("Tracking", frame)

    return frames, i, initial_size

    





def intersection_over_union(boxA, boxB):
    # 左上座標と右下座標の算出
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
    yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

    # 重なっている面積の計算
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # 各バウンディングボックスの面積を計算し、IoUを算出
    boxAArea = boxA[2] * boxA[3]
    boxBArea = boxB[2] * boxB[3]
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # intersection over union を返す
    return iou