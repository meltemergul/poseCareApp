from flask import Flask, request, jsonify
from ultralytics import YOLO
import base64
import io
from PIL import Image
import numpy as np

app = Flask(__name__)
model = YOLO("yolo11n-pose.pt")

@app.before_request
def log_request_info():
    print(f"📩 Flask: API'ye istek geldi! Route: {request.path}")

# Eşik değerleri
DOWN_THRESHOLD = 150.0
UP_THRESHOLD = 165.0

class Session:
    def __init__(self):
        self.correct = 0
        self.incorrect = 0
        self.last_status = "⏳ Bekleniyor..."
        self.stage = 'up'
        self.lowest = 180.0
        self.filtered_angle = 180.0
        self.alpha = 0.4
        self.up_frame_count = 0

    def reset(self):
        self.correct = 0
        self.incorrect = 0
        self.last_status = "⏳ Bekleniyor..."

squat_session = Session()
bridge_session = Session()

def calculate_angle(p1, p2, p3):
    a, b, c = map(np.array, (p1, p2, p3))
    ba, bc = a - b, c - b
    nb, nc = np.linalg.norm(ba), np.linalg.norm(bc)
    if nb == 0 or nc == 0:
        return 180.0
    cos = np.dot(ba, bc) / (nb * nc)
    cos = np.clip(cos, -1.0, 1.0)
    return float(np.degrees(np.arccos(cos)))

def analyze_squat(kpts, session: Session):
    right_angle = calculate_angle(kpts[11], kpts[13], kpts[15])
    left_angle = calculate_angle(kpts[12], kpts[14], kpts[16])
    angle = min(right_angle, left_angle)

    session.filtered_angle = session.alpha * angle + (1 - session.alpha) * session.filtered_angle
    filtered = session.filtered_angle

    if session.stage == 'up':
        session.up_frame_count = 0
        if filtered < DOWN_THRESHOLD:
            session.stage = 'down'
            session.lowest = filtered
            session.last_status = "⬇️ Çömeliyor"
        else:
            session.last_status = "⏳ Bekleniyor..."
    else:
        if filtered < session.lowest:
            session.lowest = filtered
        if angle > UP_THRESHOLD:
            session.up_frame_count += 1
            if session.up_frame_count >= 1:
                if session.lowest < DOWN_THRESHOLD:
                    session.correct += 1
                    session.last_status = "✔️ Doğru squat"
                else:
                    session.incorrect += 1
                    session.last_status = "❌ Yanlış squat"
                session.stage = 'up'
                session.lowest = 180.0
                session.up_frame_count = 0
        else:
            session.last_status = "⏳ Yukarı kalkmasını bekliyor"

    return angle, session.last_status

def analyze_bridge(kpts, session: Session):
    # örnek: shoulder (6), hip (12), knee (14)
    angle = calculate_angle(kpts[6], kpts[12], kpts[14])
    if angle > 160:
        session.correct += 1
        session.last_status = "✔️ Doğru bridge"
    else:
        session.incorrect += 1
        session.last_status = "❌ Yanlış bridge"
    return angle, session.last_status

@app.route('/pose', methods=['POST'])
def pose():
    data = request.get_json(force=True)
    exercise = data.get("exercise", "squat")  # default squat

    if not data or 'image' not in data:
        return jsonify({"angle": None, "status": "Görsel alınamadı", "correct": 0, "incorrect": 0})

    try:
        img = Image.open(io.BytesIO(base64.b64decode(data['image']))).convert("RGB")
        frame = np.array(img)
        res = model.predict(source=frame, save=False, conf=0.3)[0]
        kp = res.keypoints

        if kp is None or not hasattr(kp, 'xy') or len(kp.xy) == 0:
            return jsonify({"angle": None, "status": "Kişi tespit edilemedi", "correct": 0, "incorrect": 0})

        persons = [x for x in kp.xy if x.shape[0] >= 16]
        if not persons:
            return jsonify({"angle": None, "status": "Kişi bulunamadı", "correct": 0, "incorrect": 0})

        kpts = max(persons, key=lambda t: t[:,1].max() - t[:,1].min()).cpu().numpy()

        if exercise == "bridge":
            angle, status = analyze_bridge(kpts, bridge_session)
            return jsonify({
                "angle": angle,
                "status": status,
                "correct": bridge_session.correct,
                "incorrect": bridge_session.incorrect
            })
        else:
            angle, status = analyze_squat(kpts, squat_session)
            return jsonify({
                "angle": angle,
                "status": status,
                "correct": squat_session.correct,
                "incorrect": squat_session.incorrect
            })

    except Exception as e:
        return jsonify({"angle": None, "status": f"Hata: {str(e)}", "correct": 0, "incorrect": 0})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
