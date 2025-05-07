import cv2
import base64
import requests
import time
import re

API_KEY = "AIzaSyDFsF6jEulqvot31qbi8kTHe66YRm5ApAQ"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

HEADERS = {
    "Content-Type": "application/json"
}

def encode_frame_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def query_gemini_for_box_position(base64_image_cam1, base64_image_cam2):
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64_image_cam1
                        }
                    },
                    {
                        "text": (
                            "This is Camera 1. It shows a front view of the scene. "
                            "Use this image to determine the **x and y pixel coordinates** of the center of a rectangular box, if present."
                        )
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64_image_cam2
                        }
                    },
                    {
                        "text": (
                            "This is Camera 2. It shows a side/depth view of the same scene. "
                            "Use this image to determine the **z pixel coordinate** of the same box.\n\n"
                            "If a box is detected, respond with its center coordinates (in pixel units) strictly in the following format:\n"
                            "`x=..., y=..., z=...`\n"
                            "If no box is found, respond exactly: `No box found.`"
                        )
                    }
                ]
            }
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=body)
    if response.ok:
        try:
            content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            print("Gemini response:", content)
            match = re.search(r"x\s*=\s*(\d+),\s*y\s*=\s*(\d+),\s*z\s*=\s*(\d+)", content)
            if match:
                x, y, z = map(int, match.groups())
                return x, y, z
        except Exception as e:
            print("Parsing error:", e)
    else:
        print("Gemini API error:", response.text)
    return None



def main():
    cam1 = cv2.VideoCapture(2)  # x, y view
    cam2 = cv2.VideoCapture(1)  # z axis view
    last_call = time.time()
    box_position = None

    while cam1.isOpened() and cam2.isOpened():
        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()
        if not ret1 or not ret2:
            break

        frame1 = cv2.flip(frame1, 1)
        frame2 = cv2.flip(frame2, 1)

        if time.time() - last_call > 5:  # Query every 5 seconds
            img1_b64 = encode_frame_to_base64(frame1)
            img2_b64 = encode_frame_to_base64(frame2)
            result = query_gemini_for_box_position(img1_b64, img2_b64)
            if result:
                box_position = result
            else:
                box_position = None
            last_call = time.time()

        # Display both frames
        if box_position:
            x, y, z = box_position
            cv2.circle(frame1, (x, y), 10, (255, 0, 0), -1)
            cv2.putText(frame1, f"Box: ({x}, {y}, {z})", (x + 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        cv2.imshow("Camera 1 - XY View", frame1)
        cv2.imshow("Camera 2 - Z View", frame2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
