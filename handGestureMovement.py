import cv2
import mediapipe as mp
from pygame import mixer
# Inisialisasi Audio Pygame
mixer.init()
# Ganti dengan path file audio Anda
suara = mixer.Sound(r"D:\VSC\Belajar-Mediapipe\audio.wav")

# intialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

suara_sedang_diputar = False    

# fungsi untuk mengenali gerakan tangan
def recognize_hand_gesture(hand_landmarks):
    global suara_sedang_diputar

    #ambil posisi ujung jari
    ujung_jempol = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    ujung_tunjuk = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    ujung_tengah = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ujung_manis = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ujung_kelingking = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # ambil posisi pergelangan tangan
    pergelangan_tangan = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    #ambil posisi sendi jari
    sendi_tunjuk = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    sendi_tengah = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    sendi_manis = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    sendi_kelingking = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    if (ujung_jempol.y < ujung_tunjuk.y and
        ujung_jempol.y < ujung_tengah.y and
        ujung_jempol.y < ujung_manis.y and
        ujung_jempol.y < ujung_kelingking.y):
        # playsound(r"D:\VSC\Belajar-Mediapipe\audio.wav")
        if not suara_sedang_diputar:
            suara.play()
            suara_sedang_diputar = True
        print("Jempol Terangkat")
        return "Jempol Terangkat"

    else:
        suara_sedang_diputar = False
        print ("Tidak Ada Gerakan Tangan yang Dikenali")
    return "Tidak Ada Gerakan Tangan yang Dikenali"

# fungsi untuk mendeteksi gerakan tangan
def detect_hand_gesture(frame, hands):
    # mengubah warna frame ke RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # mendeteksi tangan pada frame
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #menampilkan gerakan tangan yang dikenali
            gesture = recognize_hand_gesture(hand_landmarks)
            # menggambar landmark tangan pada frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # menampilkan teks gerakan tangan pada frame
            cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return frame

# membuka kamera 1
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Kamera tidak dapat dibuka")
    exit()

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        print("Error: Tidak dapat membaca frame")
        break

    # mendeteksi gerakan tangan pada frame
    frame = detect_hand_gesture(frame, hands)

    # menampilkan frame
    cv2.imshow("HandGesture Movement", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# melepaskan kamera dan menutup jendela
cap.release()
cv2.destroyAllWindows()