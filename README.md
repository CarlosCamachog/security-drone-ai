# Security Drone AI — Fire Detection

This project develops and compares two AI models for fire detection in images, 
designed for future integration into a **modular security drone**.

## Summary
- **TM Model:** Fast, easy to implement, but less sensitive.
- **Colab Model:** Custom MobileNetV2 with higher precision and recall, suitable for real-world deployment.

## Key Results
| Metric | TM Model | Colab Model |
|---------|----------|-------------|
| Accuracy | 87.5% | **93.2%** |
| Precision | 0.82 | **0.85** |
| Recall (Sensitivity) | 0.78 | **0.91** |
| F1-Score | 0.80 | **0.88** |
| FPS (CPU i5) | 17.1 | 17.6 |

## Requirements
- Python 3.10+
- Install:
```bash
pip install -r requirements.txt


## Usage (no hardware, video demo)

- Download / place a small test video into docs/samples/ (e.g., fire_test.mp4).

- Place or export an ONNX model into models/ (e.g., fire.onnx).

- Run:

- python src/infer.py --model models/fire.onnx --video docs/samples/fire_test.mp4 --save docs/results/demo.mp4 --threshold 0.5


- src/infer.py provides a minimal ONNXRuntime inference loop and saves an annotated video to docs/results/.



## Repository Structure
security-drone-ai/
├─ src/            # Inference/training scripts
├─ models/         # Exported models (.onnx / .tflite) - large files via links or LFS
├─ hardware/       # Drone schematics / BOM (future)
├─ docs/           # Paper, certificate, images, results
│  ├─ 2025_MHTC_IA_Humo.pdf
│  ├─ results/
│  └─ samples/
└─ datasets/       # Links or download scripts (do not commit raw datasets)


## Certification & Paper
Presented at the **IEEE Mexican Humanitarian Technology Conference 2025**.

![Certificate](docs/IEEE_MHTC2025_Certificate.png)

[**View Full Paper (PDF)**](docs/2025_MHTC_IA_Humo.pdf)

## Limitations

- False negatives can occur with low light or heavy smoke coverage.

- Current repo focuses on software/inference; embedded hardware integration is WIP.

- Performance varies by CPU/GPU; embedded benchmarks pending.

- Dataset scope still limited; needs more smoke and complex scenes.

## Roadmap
- v0.1: Reproducible inference + basic benchmark on CPU (this repo).

- v0.2: Export to ONNX/TFLite + INT8 quantization.

- v0.3: ROS node + MQTT alerts + embedded (Raspberry Pi / Jetson).

## Future Work
- Optimize models for embedded devices like Raspberry Pi or Jetson Nano.
- Expand datasets to include smoke and environmental factors.
- Integrate fire detection with other drone security features.
