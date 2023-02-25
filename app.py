import streamlit as st
import time
import tempfile
import numpy as np
import cv2
from PIL import Image, ImageOps
from detection.object_detection import track_object2, get_first_frame

#赤
color = (0, 0, 255) 

def main():
    st.title("モックアップ")
    status_space = st.sidebar.empty()
    status_space.subheader("動画をアップロードして下さい")
    
    cap = upload_video_ui()
    if cap is not None:
        status_space.subheader("動画をのアップロードが完了しました")

    left_column, right_column = st.columns(2)
    # otameshi(left_column)

    mode = st.sidebar.radio("モード選択",["線","長方形"])
    # 選択されたモードに応じて動作を変更
    if mode == "線":
    # モード1の処理
        st.sidebar.write("「線」を描画して下さい")
        line_mode = st.sidebar.radio("線タイプ",["垂直","水平","その他"])
        if line_mode == "垂直":
            x = st.sidebar.slider('位置', 0, 100)
            first_frame = get_first_frame(cap)
            h, w= first_frame.shape[:2]
            x_actual = int(w * x /100)
            print("x_actual",x_actual)
            first_frame = first_frame.astype(np.uint8)
            first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB) 
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
    
    
    frames, frames_len ,initial_size= track_object2(cap)


    image_space = right_column.empty()

    for i in range (frames_len):

        #入力のサイズを調整
        frame = frames[i]

        #frameの色反転・縮尺を元に戻す
        resized_frame = convert_frame(frame,initial_size)
        image_space.image(resized_frame/255,use_column_width=True)
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
    if uploaded_video is None:
        print("fairu")

    if uploaded_video is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_video.read())
                file_path = tmp_file.name

                cap = cv2.VideoCapture(file_path)

            # n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            # n_channels = 3  # assume color video, so 3 channels

            # frames = np.empty((n_frames, height, width, n_channels), dtype=np.uint8)
            # for i in range(frames.shape[0]):
            #     ret, frame = cap.read()
            #     if not ret:
            #         break


    # 画像を処理して、NumPy配列に格納する
    # 例えば、画像をグレースケールに変換する場合は、以下のようになります。
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # frames[i] = frame

            # cap.release()
          
        except Exception as e:
            st.write("Error: {}".format(str(e)))
            st.error("Error: Invalid video")
        #tryブロックでエラーが発生しなかった場合はelseが実行される

        else:
            return cap

# def ndarray_to_streamlit_video(ndarray):
#     # 動画のフレームサイズとFPSを設定
#     print(ndarray.shape)
#     len,height, width, channels = ndarray.shape
#     fps = 30

#     # VideoCaptureオブジェクトを作成
#     cap = cv2.VideoCapture(0)

#     # Streamlitで動画を表示
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         st.image(frame, channels="RGB")

#     # VideoCaptureオブジェクトを解放
#     cap.release()
def otameshi(a):
    a.title("hoge")

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

if __name__ == '__main__':
    main()
