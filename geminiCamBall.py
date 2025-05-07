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

def query_gemini_for_ball_position(base64_image):
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64_image
                        }
                    },
                    {
                        "text": "Is there a ball in this image? If yes, respond with its center coordinates (x, y) and approximate radius in this format: x=..., y=..., r=.... If no ball is found, say 'No ball found.'"
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
            match = re.search(r"x\s*=\s*(\d+),\s*y\s*=\s*(\d+),\s*r\s*=\s*(\d+)", content)
            if match:
                x, y, r = map(int, match.groups())
                return x, y, r
        except Exception as e:
            print("Parsing error:", e)

    else:
        print("Gemini API error:", response.text)
    return None

def main():
    cap = cv2.VideoCapture(2)
    last_call = time.time()
    ball_position = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Optional: mirror view

        if time.time() - last_call > 5:  # Query every 5 seconds
            base64_img = encode_frame_to_base64(frame)
            result = query_gemini_for_ball_position(base64_img)
            if result:
                ball_position = result
            else:
                ball_position = None
            last_call = time.time()

        if ball_position:
            x, y, r = ball_position
            cv2.circle(frame, (x, y), r, (0, 255, 0), 3)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            cv2.putText(frame, "Ball", (x - 10, y - r - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Gemini Ball Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
