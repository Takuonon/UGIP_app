import streamlit as st
import time
import tempfile
import numpy as np
import cv2
from PIL import Image, ImageOps
from detection.object_detection import track_object2, get_first_frame, convert_frame
from warning.warning import warning_line
import matplotlib.pyplot as plt

#赤
color = (255, 0, 0) 

def get_style():
    with open("./css/design.css") as f:
        return f.read()

#cssで装飾
css = get_style()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

points = []


def main():

    with st.container():
        st.header("モックアップ")
    status_space = st.sidebar.empty()
    status_space.subheader("動画をアップロードして下さい")
    
    cap = upload_video_ui()
    print(cap)
    
    if cap is not None:
        status_space.subheader("動画のアップロードが完了しました")

        left_column, right_column = st.columns(2)

        mode = st.sidebar.radio("モード選択",["線","長方形"])

        #warningで使うために宣言
        line_mode = ""
        x_actual = 0
        y_actual = 0
        x1 = 0
        y1 = 0



        # 選択されたモードに応じて動作を変更
        if mode == "線":
        # モード1の処理
            st.sidebar.write("「線」を描画して下さい")
            line_mode = st.sidebar.radio("線タイプ",["垂直","水平","その他"])

            if line_mode == "垂直":
                x = st.sidebar.slider('位置', 0, 100, 50)
                first_frame = get_first_frame(cap)
                h, w= first_frame.shape[:2]
                x_actual = int(w * x /100)
                first_frame = first_frame.astype(np.uint8)
                cv2.line(first_frame, (x_actual, 0), (x_actual, h), color, thickness=2)
                left_column.image(first_frame,use_column_width=True)

            if line_mode == "水平":  
                y = st.sidebar.slider('位置', 0, 100, 50)
                first_frame = get_first_frame(cap)
                h, w= first_frame.shape[:2]
                y_actual = int(h * y /100)
                first_frame = first_frame.astype(np.uint8)
                cv2.line(first_frame, (0, y_actual), (w, y_actual), color, thickness=2)
                left_column.image(first_frame,use_column_width=True)


            if line_mode == "その他":
                x = st.sidebar.slider('位置', 0, 100, 50)  
                arg = st.sidebar.slider('角度', -180, 0, -125)
                #視覚的なわかりやすさのためにこうした
                arg += 180
                #arg == 90 の時は垂直と同じ操作
                if arg == 90:
                    first_frame = get_first_frame(cap)
                    h, w= first_frame.shape[:2]
                    x_actual = int(w * x /100)
                    first_frame = first_frame.astype(np.uint8)
                    cv2.line(first_frame, (x_actual, 0), (x_actual, h), color, thickness=2)
                    left_column.image(first_frame,use_column_width=True)
                    x1 = x_actual
                    y1 = h
                
                #arg == 0,180 の時は水平と同じ操作
                elif arg == 0 or arg == 180:
                    first_frame = get_first_frame(cap)
                    h, w= first_frame.shape[:2]
                    y_actual = int(h * x /100)
                    first_frame = first_frame.astype(np.uint8)
                    cv2.line(first_frame, (0, y_actual), (w, y_actual), color, thickness=2)
                    left_column.image(first_frame,use_column_width=True)
                    x1 = w
                    y1 = y_actual

                elif arg < 90:
                    first_frame = get_first_frame(cap)
                    h, w= first_frame.shape[:2]
                    #実際のx切片
                    x_actual = int(w * x /100)
                    first_frame = first_frame.astype(np.uint8)
                    y_intercept = int(np.tan(np.radians(arg)) * x_actual)
                    cv2.line(first_frame, (0, y_intercept), (x_actual, 0), color, thickness=2)
                    y1 = y_intercept
                    left_column.image(first_frame,use_column_width=True)

                elif arg > 90:
                    first_frame = get_first_frame(cap)
                    h, w= first_frame.shape[:2]
                    #実際のx切片
                    x_actual = int(w * x /100)
                    first_frame = first_frame.astype(np.uint8)
                    y_intercept = int(-np.tan(np.radians(arg))*w+np.tan(np.radians(arg)) * x_actual)
                    print("here")
                    cv2.line(first_frame, (w, y_intercept), (x_actual, 0), color, thickness=2)
                    left_column.image(first_frame,use_column_width=True)
                    x1 = w
                    y1 = y_intercept

                print(x1)
                print(y1)
                # while True:
                #     time.sleep(1)


        elif mode == "長方形":
        # モード2の処理
            st.sidebar.write("領域は「長方形」で指定できます")
            first_frame = get_first_frame(cap)
            h, w= first_frame.shape[:2]
            # x_actual = int(w * x /100)
            first_frame = first_frame.astype(np.uint8)

            # Matplotlibのイベントを有効にし、画像上でマウスクリックイベントを取得する
            fig = plt.figure()
            plt.imshow(np.array(first_frame))
            plt.axis('off')
            cid = fig.canvas.mpl_connect('button_press_event', onclick)

            # MatplotlibのFigureオブジェクトをStreamlitのUIに表示する
            st.pyplot(fig)
            
             
        image_space = right_column.empty()
        frames, frames_len ,initial_size, boxes= track_object2(cap,image_space)

        st.subheader("判定")
        judge_space = st.empty()
        for i in range (frames_len):

            #画像を連続で出力
            frame = frames[i]
            resized_frame = convert_frame(frame,initial_size)
            image_space.image(resized_frame/255,use_column_width=True)

            if i !=0:
                if mode == "線":
                    if line_mode == "垂直":
                        warning_line(line_mode,x_actual,None,boxes,i ,initial_size,judge_space,None,None)

                    if line_mode == "水平":
                        warning_line(line_mode,None,y_actual,boxes,i ,initial_size,judge_space,None,None)

                    else:
                        warning_line(line_mode,x_actual,y_actual,boxes,i ,initial_size,judge_space,x1,y1)

                        


            time.sleep(0.05)


        # フレームサイズを取得する
        height, width, channels = frames[0].shape
        print(height,width)

        # 動画ファイルの書き込み準備
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, 10.0, (width, height))

        #TODO rectangleは単純に倍率かければいける

        # フレームを動画ファイルに書き込む
        for i in range(frames_len):
            frame = (frames[i])
            frame = cv2.convertScaleAbs(frame)
            out.write(frame)

        # 動画ファイルを閉じる
        out.release()

        #TODO output.mp4をダウンロード
        st.download_button('Download file', data = "output.mp4", mime="video/mp4")


def upload_video_ui():
    uploaded_video = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"], key="file_uploader")
    
    # while uploaded_video is None:
    #     time.sleep(1)


    if uploaded_video is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_video.read())
                file_path = tmp_file.name

                cap = cv2.VideoCapture(file_path)
          
        except Exception as e:
            st.write("Error: {}".format(str(e)))
            st.error("Error: Invalid video")
        #tryブロックでエラーが発生しなかった場合はelseが実行される

        else:
            return cap

# マウスイベント用のコールバック関数
def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONUP:
        # マウスの左ボタンが離された場合、クリックした座標を取得
        points.append((x, y))
        if len(points) == 4:
            # 4点が選択された場合、4点の座標を表示
            st.write("Selected points:", points)

# 画像上でマウスをクリックしたときのイベントを処理する関数を作成する
def onclick(event):
    if len(points) < 4:
        points.append((event.xdata, event.ydata))
        plt.plot(event.xdata, event.ydata, 'ro')
        plt.draw()
        # 座標を表示する
        st.text(points)


if __name__ == '__main__':
    main()
