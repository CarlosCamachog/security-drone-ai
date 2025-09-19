import argparse, cv2, time, numpy as np
import onnxruntime as ort

def load_model(p):
    sess = ort.InferenceSession(p, providers=["CPUExecutionProvider"])
    return sess, sess.get_inputs()[0].name

def preprocess(frame, size):
    h, w = frame.shape[:2]
    img = cv2.resize(frame, (size, size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)/255.0
    img = np.transpose(img, (2,0,1))[None, ...]
    return img

def annotate(frame, prob, th=0.5):
    if prob >= th:
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (int(0.1*w), int(0.1*h)), (int(0.6*w), int(0.6*h)), (0,255,0), 2)
        cv2.putText(frame, f"FIRE {prob:.2f}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    return frame

def main(a):
    sess, in_name = load_model(a.model)
    cap = cv2.VideoCapture(a.video); assert cap.isOpened(), f"Cannot open {a.video}"
    out = None
    if a.save:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(a.save, fourcc, cap.get(cv2.CAP_PROP_FPS) or 24.0,
                              (int(cap.get(3)), int(cap.get(4))))
    t0=time.time(); frames=0
    while True:
        ok, frame = cap.read()
        if not ok: break
        inp = preprocess(frame, a.size)
        # Demo: suponer salida con "probabilidad" en outputs[0][0]
        outputs = sess.run(None, {in_name: inp})
        prob = float(outputs[0].ravel()[0]) if isinstance(outputs, list) else 0.6
        frame = annotate(frame, prob, a.threshold)
        if out: out.write(frame)
        frames += 1
    cap.release()
    if out: out.release()
    dt=time.time()-t0
    print(f"Processed {frames} frames in {dt:.2f}s → {frames/max(dt,1e-6):.1f} FPS")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--save", default="docs/results/demo.mp4")
    ap.add_argument("--size", type=int, default=240)
    ap.add_argument("--threshold", type=float, default=0.5)
    main(ap.parse_args())
