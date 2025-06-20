# Top-View Multi-View Cattle-ID (YOLOv7-based)

Implementation of **Top-View / Multi-View Cattle Identification**  
基於 YOLOv7 之「俯拍 + 多視角」牛隻身分辨識模型

[![Papers With Code](https://img.shields.io/badge/PaperswithCode-ComingSoon-informational)](#)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Guichou227/top-view-cattle-id/blob/main/notebooks/demo.ipynb)

<div align="center">
  <img src="./figs/pipeline.png" width="80%">
</div>

---

## 1. 特色 (Why this repo?)

| 功能 | 說明 |
|------|------|
| **多視角融合** | 同時支援俯拍、側拍與斜 45° 角度影像，透過 *view-aware* head 融合特徵。 |
| **輕量化部署** | 提供 *ONNX / TensorRT* 匯出腳本，可於邊緣 GPU (Jetson AGX) 即時推論。 |
| **ID re-mapping** | 僅需對照毛色及花紋影像即可快速辨識牛隻 ID。 |
| **擴充性** | 支援 Key-points、行為偵測 (mounting / lying) 之多任務 joint-training。 |

---

## 2. 效能 (Cattle-ID-2024 dataset)

| Model | Input | mAP<sub>ID</sub> | Top-1 ID Acc | FPS (b1) | Avg-latency (b32) |
|-------|------:|-----------------:|-------------:|---------:|------------------:|
| **Ours-P5** | 640 | **93.5 %** | **95.1 %** | 142 | 3.1 ms |
| **Ours-P6** | 1280 | **95.8 %** | **97.0 %** | 68 | 8.4 ms |

*訓練集：12 牧場 / 18 萬張影像 測試集：3 牧場 / 2 萬張影像*

---

## 3. 安裝 (Docker 推薦)

```bash
# create container (share-memory 可依需求修改)
docker run --gpus all -it --shm-size=32g \
  -v $(pwd):/workspace/topview-cattle-id \
  --name cattle-id nvcr.io/nvidia/pytorch:22.06-py3

apt update && apt install -y zip htop libgl1-mesa-glx
pip install -r requirements.txt      # torch, opencv, thop ...

## 4. 推論 (Inference)

```bash
python detect.py \
  --weights weights/cattle-id-p5.pt \
  --source data/test/video.mp4 \
  --img 640 --conf 0.30 --view-merge
輸出示意

<div align="center"><img src="./figs/demo.gif" width="65%"/></div>
## 5. 訓練 (Custom Training)
bash
複製
編輯
python train.py --workers 8 --device 0 \
  --batch-size 16 --data data/cattle-id.yaml \
  --img 640 640 \
  --cfg cfg/training/cattle-id-p5.yaml \
  --weights '' --name cattle-id-p5
data/cattle-id.yaml 範例：

yaml
複製
編輯
train: /path/to/images/train
val:   /path/to/images/val
names: [cow]
## 6. 匯出 (Export)
bash
複製
編輯
python export.py --weights cattle-id-p5.pt \
  --grid --simplify --end2end \
  --img-size 640 640 --topk-all 200
## 7. 引用 (Citation)
bibtex
複製
編輯
@misc{Guichou2025cattleID,
  title   = {Top-View Multi-View Cattle Identification},
  author  = {Liang, Gui-Chou and others},
  year    = {2025},
  note    = {GitHub repository},
  url     = {https://github.com/Guichou227/top-view-cattle-id}
}
## 8. 致謝 (Acknowledgements)
本專案基於 YOLOv7，並參考以下開源成果：

ultralytics/yolov5

Megvii-BaseDetection/YOLOX

AlexeyAB/darknet

感謝所有貢獻者！
