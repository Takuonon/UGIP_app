import streamlit as st
import time
import tempfile
import numpy as np
import cv2
from PIL import Image, ImageOps
from detection.object_detection import track_object2, get_first_frame, convert_frame
from warning.warning import warning_line

#赤
color = (255, 0, 0) 

def main():
    st.title("モックアップ")
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



        # 選択されたモードに応じて動作を変更
        if mode == "線":
        # モード1の処理
            st.sidebar.write("「線」を描画して下さい")
            line_mode = st.sidebar.radio("線タイプ",["垂直","水平","その他"])
            if line_mode == "垂直":
                x = st.sidebar.slider('位置', 0, 100, 50)
                first_frame = get_first_frame(cap)
                # resized_first_frame = convert_frame(first_frame,)
                h, w= first_frame.shape[:2]
                x_actual = int(w * x /100)
                print("x_actual",x_actual)
                first_frame = first_frame.astype(np.uint8)
                # first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB) 
                cv2.line(first_frame, (x_actual, 0), (x_actual, h), color, thickness=2)
                left_column.image(first_frame,use_column_width=True)


                
            if line_mode == "水平":  
                y = st.sidebar.slider('位置', 0, 100, disabled=True)
            if line_mode == "その他":
                x_move = st.sidebar.slider('x方向へ移動', 0, 100, disabled=True) 
                y_move = st.sidebar.slider('y方向へ移動', 0, 100, disabled=True)  
                arg = st.sidebar.slider('角度', 0, 180, disabled=True)

        elif mode == "長方形":
        # モード2の処理
            st.sidebar.write("領域は「長方形」で指定できます")
        else:
        # モード3の処理
            st.sidebar.write("領域タイプを選択して下さい")
        
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
                    warning_line(line_mode,x_actual,boxes,i ,initial_size,judge_space)
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



if __name__ == '__main__':
    main()
