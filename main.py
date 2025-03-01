import cv2
import webbrowser
from pyzbar.pyzbar import decode
import numpy as np

def scan_qr():
    cap = cv2.VideoCapture(0)  # Open webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")

            # Open link if QR contains a URL
            if qr_data.startswith(("http://", "https://")):
                print("Opening URL...")
                webbrowser.open(qr_data)
                cap.release()
                cv2.destroyAllWindows()
                return  # Exit after opening the URL

            # Draw rectangle around the QR code
            points = obj.polygon
            if len(points) == 4:
                pts = np.array([(point.x, point.y) for point in points], dtype=np.int32)
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=3)

        cv2.imshow("QR Code Scanner", frame)

        # If QR code detected, exit the loop
        if decoded_objects:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr()
