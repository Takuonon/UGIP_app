import streamlit as st
import time
import tempfile
import numpy as np
import cv2
from detection.object_detection import track_object2, get_first_frame, convert_frame
from warning.warning import warning_line, warning_rectangle

#赤
color = (255, 0, 0) 

def main():

    # print("OpenCV version : ", cv2.__version__)

    with st.container():
        st.header("RailSentry")
    status_space = st.sidebar.empty()
    status_space.write("動画をアップロードして下さい")
    
    cap = upload_video_ui()
    
    if cap is not None:
        status_space.subheader("動画のアップロードが完了しました")

        left_column, right_column = st.columns(2)

        mode = st.sidebar.radio("モード選択",["線","長方形"])

        #warningで使うために宣言
        line_mode = ""
        x_actual = 0
        y_actual = 0
        width_actual = 0
        height_actual = 0
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
                cv2.line(first_frame, (x_actual, 0), (x_actual, h), color, thickness=5)
                left_column.image(first_frame,use_column_width=True)

            if line_mode == "水平":  
                y = st.sidebar.slider('位置', 0, 100, 50)
                first_frame = get_first_frame(cap)
                h, w= first_frame.shape[:2]
                y_actual = int(h * y /100)
                first_frame = first_frame.astype(np.uint8)
                cv2.line(first_frame, (0, y_actual), (w, y_actual), color, thickness=5)
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
                    cv2.line(first_frame, (x_actual, 0), (x_actual, h), color, thickness=5)
                    left_column.image(first_frame,use_column_width=True)
                    x1 = x_actual
                    y1 = h
                
                #arg == 0,180 の時は水平と同じ操作
                elif arg == 0 or arg == 180:
                    first_frame = get_first_frame(cap)
                    h, w= first_frame.shape[:2]
                    y_actual = int(h * x /100)
                    first_frame = first_frame.astype(np.uint8)
                    cv2.line(first_frame, (0, y_actual), (w, y_actual), color, thickness=5)
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
                    cv2.line(first_frame, (0, y_intercept), (x_actual, 0), color, thickness=5)
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
                    cv2.line(first_frame, (w, y_intercept), (x_actual, 0), color, thickness=5)
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
            x = st.sidebar.slider('位置(横)', 0, 100, 50)
            y = st.sidebar.slider('位置(縦)', 0, 100, 20)
            width = st.sidebar.slider('長方形の横幅', 0, 100, 40)
            height = st.sidebar.slider('長方形の高さ', 0, 100, 40)
            first_frame = get_first_frame(cap)
            h, w= first_frame.shape[:2]
            x_actual = int(w * x /100)
            y_actual = int(h * y/100)
            width_actual = int (w * width/100)
            height_actual = int (h * height/100)

            first_frame = first_frame.astype(np.uint8)
            cv2.rectangle(first_frame, (x_actual, y_actual), (x_actual + width_actual, y_actual + height_actual), color, thickness=2)


            # 黒画像を生成します。
            black = np.zeros_like(first_frame)
            cv2.rectangle(black, (x_actual, y_actual), (x_actual + width_actual, y_actual + height_actual), (255, 255, 255), -1)

            # 2値化します。
            gray = cv2.cvtColor(black, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

            # 元の画像と黒画像を重ね合わせます。
            result = cv2.bitwise_and(first_frame, black, mask=thresh)

            # 元の画像と黒で塗りつぶされた画像を重ね合わせます。
            alpha = 0.6
            beta = 1 - alpha
            result = cv2.addWeighted(first_frame, alpha, result, beta, 0)

            left_column.image(result,use_column_width=True)
        
            


             
        image_space = right_column.empty()
        frames, frames_len ,initial_size, boxes= track_object2(cap,image_space)

        st.subheader("判定")
        judge_space = st.empty()
        

        for y in range(30):
            crossed = False
            for i in range (frames_len):

                #画像を連続で出力
                frame = frames[i]
                resized_frame = convert_frame(frame,initial_size)
                image_space.image(resized_frame/255,use_column_width=True)

                if i !=0:
                    if mode == "線":
                        if line_mode == "垂直":
                            warning_line(line_mode,x_actual,None,boxes,i ,initial_size,judge_space,None,None,crossed)

                        if line_mode == "水平":
                            warning_line(line_mode,None,y_actual,boxes,i ,initial_size,judge_space,None,None,crossed)

                        else:
                            if crossed == False:
                                crossed = warning_line(line_mode,x_actual,y_actual,boxes,i ,initial_size,judge_space,x1,y1,crossed)
                            else :
                                judge_space.write("<p style='font-size: 20px; color: red; font-weight: bold; text-align: center;'>⚠️設定した線を超えました⚠️</p>", unsafe_allow_html=True)
                    
                    if mode == "長方形":
                        warning_rectangle(x_actual,y_actual,width_actual,height_actual,boxes,i ,initial_size,judge_space)

                time.sleep(0.003)

    #bounding boxをつけた動画を保存する機能(コメントアウトを外せば多分動きます)
        # # フレームサイズを取得する
        # height, width, channels = frames[0].shape
        # print(height,width)

        # # 動画ファイルの書き込み準備
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # out = cv2.VideoWriter('output.mp4', fourcc, 10.0, (width, height))

        # #TODO rectangleは単純に倍率かければいける

        # # フレームを動画ファイルに書き込む
        # for i in range(frames_len):
        #     frame = (frames[i])
        #     frame = cv2.convertScaleAbs(frame)
        #     out.write(frame)

        # # 動画ファイルを閉じる
        # out.release()

        # #TODO output.mp4をダウンロード
        # st.download_button('Download file', data = "output.mp4", mime="video/mp4")


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
