import os
import cv2
import numpy as np
import face_recognition as fr
import pandas as pd
from datetime import datetime, date
import pyttsx3
import threading

def load_image(folder="imgtraining"):
    encodings, names = [], []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        image = cv2.imread(path)
        if image is None:
            continue
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        enc = fr.face_encodings(rgb)
        if enc:
            encodings.append(enc[0])
            names.append(os.path.splitext(file)[0])
    return encodings, names

def detect_faces(frame, known_encodings, known_names, tolerance=0.45):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = fr.face_locations(rgb)
    new_encodings = fr.face_encodings(rgb, locations)

    results = []
    for enc, loc in zip(new_encodings, locations):
        distance = fr.face_distance(known_encodings, enc)
        if len(distance) > 0:
            best_match = np.argmin(distance)
            if distance[best_match] < tolerance:
                results.append(known_names[best_match])
            else:
                results.append("Unknown")
    return results

def speak_text(text):
    def run():
        engine = pyttsx3.init()
        engine.setProperty("Rate", 150)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

def setup_excel():
    filename = "attendance.xlsx"
    today = date.today().strftime("%Y-%m-%d")
    sheet = f"attendance_{today}"

    if not os.path.exists(filename):
        df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
        with pd.ExcelWriter(filename, mode='w') as writer:
            df.to_excel(writer, sheet_name=sheet, index=False)
    else:
        try:
            df = pd.read_excel(filename, sheet_name=sheet)
        except:
            df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
    return filename, sheet, df

def save_excel(filename, sheet, df):
    with pd.ExcelWriter(filename, mode='a', if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=sheet, index=False)

def main():
    encodings_list, name_list = load_image("imgtraining")

    excel_file, sheet_name, df_today = setup_excel()
    attended_names = set(df_today["Name"].tolist())

    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        results = detect_faces(frame, encodings_list, name_list)

        for name in results:
            cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            if name != "Unknown" and name not in attended_names:
                now = datetime.now()
                date_str, time_str = now.strftime("%y-%m-%d"), now.strftime("%H:%M:%S")
                status = "Late" if now.hour >= 7 else "On Time"

                new_row = pd.DataFrame([[name, date_str, time_str, status]],
                                       columns=df_today.columns)
                df_today = pd.concat([df_today, new_row], ignore_index=True)
                attended_names.add(name)
                print(f"{name} attend at {time_str} - {status}")
                speak_text(f"{name} attend, status{status}")

        cv2.putText(frame, f"Total present: {len(attended_names)}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 255), 2)
        cv2.imshow("system attendance faces", frame)

        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    
    camera.release()
    cv2.destroyAllWindows()
    save_excel(excel_file, sheet_name, df_today)

if __name__ == "__main__":
    main()

