import cv2
import mediapipe as mp

def main():
    # 1. 設定：カメラと手・顔の検出器の準備
    cap = cv2.VideoCapture(0) # 0は標準カメラ
    
    mp_hands = mp.solutions.hands
    mp_face_mesh = mp.solutions.face_mesh
    
    # 手の検出器
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    
    # 顔の検出器
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # アホな日本人バージョン
    # index_img_path = "imgs/index_finger.png"
    # middle_img_path = "imgs/middle_finger.png"
    # thumb_img_path = "imgs/thumb_up.png"
    # tongue_img_path = "imgs/tongue_out.png"
    
    # Memeバージョン
    index_img_path = "imgs/meme_index_finger.jpg"
    middle_img_path = "imgs/meme_middle_finger.jpg"
    thumb_img_path = "imgs/meme_thumb_up.jpeg"
    tongue_img_path = "imgs/meme_tongue_out.png"
    
    index_image = cv2.imread(index_img_path)
    middle_image = cv2.imread(middle_img_path)
    thumb_image = cv2.imread(thumb_img_path)
    tongue_image = cv2.imread(tongue_img_path)
    
    # 画像が読み込めなかった場合の安全装置
    if index_image is None:
        print(f"エラー: {index_img_path} が見つかりません。")
        return
    if middle_image is None:
        print(f"エラー: {middle_img_path} が見つかりません。")
        return
    if thumb_image is None:
        print(f"エラー: {thumb_img_path} が見つかりません。")
        return
    if tongue_image is None:
        print(f"警告: {tongue_img_path} が見つかりません。舌検出は無効化されます。")

    print("アプリを開始します。'q'キーで終了します。")

    while True:
        # カメラから1フレーム読み込む
        ret, frame = cap.read()
        if not ret:
            break

        # 鏡のように左右反転させる（使いやすくするため）
        frame = cv2.flip(frame, 1)
        
        # 画面のサイズを取得
        h, w, _ = frame.shape

        # MediaPipe用に色を変換 (BGR -> RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 手と顔を検出する
        hand_result = hands.process(rgb_frame)
        face_result = face_mesh.process(rgb_frame)

        # フラグ：どの画像を表示するか
        show_index = False
        show_middle = False
        show_thumb = False
        show_tongue = False

        # 手が見つかった場合の処理
        if hand_result.multi_hand_landmarks:
            for hand_landmarks in hand_result.multi_hand_landmarks:
                # 各指のY座標を取得
                thumb_tip_y = hand_landmarks.landmark[4].y
                thumb_ip_y = hand_landmarks.landmark[3].y
                
                index_tip_y = hand_landmarks.landmark[8].y
                index_pip_y = hand_landmarks.landmark[6].y
                
                middle_tip_y = hand_landmarks.landmark[12].y
                middle_pip_y = hand_landmarks.landmark[10].y
                
                ring_tip_y = hand_landmarks.landmark[16].y
                ring_pip_y = hand_landmarks.landmark[14].y
                
                pinky_tip_y = hand_landmarks.landmark[20].y
                pinky_pip_y = hand_landmarks.landmark[18].y

                # 各指が伸びているか判定
                is_thumb_open = thumb_tip_y < thumb_ip_y
                is_index_open = index_tip_y < index_pip_y
                is_middle_open = middle_tip_y < middle_pip_y
                is_ring_closed = ring_tip_y > ring_pip_y
                is_pinky_closed = pinky_tip_y > pinky_pip_y

                # 人差し指のみが立っている場合
                if is_index_open and not is_middle_open and is_ring_closed and is_pinky_closed and not is_thumb_open:
                    show_index = True
                
                # 中指のみが立っている場合
                elif is_middle_open and not is_index_open and is_ring_closed and is_pinky_closed and not is_thumb_open:
                    show_middle = True
                
                # サムアップ（親指のみが立っている場合）
                elif is_thumb_open and not is_index_open and not is_middle_open and is_ring_closed and is_pinky_closed:
                    show_thumb = True

        # 顔が見つかった場合の処理
        if face_result.multi_face_landmarks and tongue_image is not None:
            for face_landmarks in face_result.multi_face_landmarks:
                # 上唇と下唇の距離を計算
                upper_lip = face_landmarks.landmark[13].y
                lower_lip = face_landmarks.landmark[14].y
                mouth_open = abs(lower_lip - upper_lip)
                
                # 口が大きく開いている = 舌を出している可能性
                if mouth_open > 0.04:
                    show_tongue = True

        # ------------------------------------------------
        # 画面表示の切り替え（優先順位: 手 > 顔）
        # ------------------------------------------------
        if show_index:
            # 画像を表示用フレームに合わせてリサイズ
            resized_img = cv2.resize(index_image, (w, h))
            # 画面全体を画像で上書き
            cv2.imshow('Camera App', resized_img)
        elif show_middle:
            # 画像を表示用フレームに合わせてリサイズ
            resized_img = cv2.resize(middle_image, (w, h))
            # 画面全体を画像で上書き
            cv2.imshow('Camera App', resized_img)
        elif show_thumb:
            # 画像を表示用フレームに合わせてリサイズ
            resized_img = cv2.resize(thumb_image, (w, h))
            # 画面全体を画像で上書き
            cv2.imshow('Camera App', resized_img)
        elif show_tongue:
            # 画像を表示用フレームに合わせてリサイズ
            resized_img = cv2.resize(tongue_image, (w, h))
            # 画面全体を画像で上書き
            cv2.imshow('Camera App', resized_img)
        else:
            # 通常のカメラ映像を表示
            cv2.imshow('Camera App', frame)

        # 'q'キーが押されたら終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 終了処理
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()