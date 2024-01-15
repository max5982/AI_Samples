import cv2

def show_ip_camera(url):
    cap = cv2.VideoCapture(url)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("IP Camera Stream", frame)

        # Press 'q' on the keyboard to exit the stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Replace with your IP camera URL
ip_camera_url = 'http://10.10.15.102:5000/video'
show_ip_camera(ip_camera_url)

