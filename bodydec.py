import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_pose = mp.solutions.pose                      # mediapipe 姿勢偵測
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)
#肩膀前舉 肩膀側舉 手肘運動
#左肩11 左手肘13 左手腕15
#右肩12 右手肘14 右手腕16

# 啟用姿勢偵測

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, img = cap.read() #cap.read()總共回傳兩個值 ret為bool 判斷有無成功取得影片下一貞 img為下一貞的圖片
    if not ret:
        print("Cannot receive frame")
        break
    img = cv2.resize(img,(1920,1080))   # 縮小尺寸，加快演算速度
    img = cv2.flip(img, 1)
    imgdec = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # 將 BGR 轉換成 RGB
    results = pose.process(imgdec)                  # 取得姿勢偵測結果
    # 根據姿勢偵測結果，標記身體節點和骨架
    if results.pose_landmarks is not None:
        right_shoulder = (results.pose_landmarks.landmark[11].x, results.pose_landmarks.landmark[11].y)
        right_elbow = (results.pose_landmarks.landmark[13].x, results.pose_landmarks.landmark[13].y)
        right_wrist = (results.pose_landmarks.landmark[15].x, results.pose_landmarks.landmark[15].y)
        left_shoulder = (results.pose_landmarks.landmark[12].x, results.pose_landmarks.landmark[12].y)
        left_elbow = (results.pose_landmarks.landmark[14].x, results.pose_landmarks.landmark[14].y)
        left_wrist = (results.pose_landmarks.landmark[16].x, results.pose_landmarks.landmark[16].y)
        #肩膀側舉
        if abs(right_wrist[0] - right_shoulder[0]) > 0.48 or abs(left_wrist[0] - left_shoulder[0]) > 0.48: 
            # rehab_status = "True"
            pre = "肩膀側舉"
            # print("肩膀側舉")
        #手肘彎曲
        if (abs(right_wrist[1] - right_elbow[1])<0.36 and abs(right_wrist[0] - right_shoulder[0])<0.023) or (abs(left_wrist[1] - left_elbow[1])<0.36 and abs(left_wrist[0] - left_shoulder[0])<0.023): 
            # rehab_status = "True"
            pre = "手肘彎曲"
            # print("手肘彎曲")
        #手肘前伸
        if (abs(right_shoulder[1] - right_elbow[1])<0.25 and abs(left_shoulder[1] - left_elbow[1])<0.25): 
            # rehab_status = "True"
            pre = "手肘前伸"
            # print("手肘前伸")
            

        if pre is not None:
            print("pre")
        else:
            print("False")

    mp_drawing.draw_landmarks(
        img,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        
    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'): #waitKey(1)等待鍵盤按鍵訊號 等待1ms
        break     # 按下 q 鍵停止
cap.release()
cv2.destroyAllWindows()