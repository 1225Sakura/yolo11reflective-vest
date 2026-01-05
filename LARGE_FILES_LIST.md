# 百度网盘下载说明

## 分享信息

**百度网盘链接**: https://pan.baidu.com/s/5JiTmn3N_nYOVsue5l19Xjw

**来源**: 百度网盘超级会员v3分享

---

## 包含内容

### 1. 数据集 - fgy.rar
**文件名**: `fgy.rar`
**大小**: 9.8GB
**说明**: 反光衣数据集压缩包（YOLO格式）

**数据集信息**:
- 训练集: 27,414 张图片 (43,044 个标注)
- 验证集: 6,794 张图片 (10,330 个标注)
- 测试集: 9,994 张图片 (16,078 个标注)
- 总计: 44,202 张图片，69,452 个反光衣标注

**使用方法**:
1. 从百度网盘下载 `fgy.rar`
2. 解压到项目的 `data/` 目录
3. 确保解压后路径为: `data/vest_merged/`

---

### 2. 模型权重 - weights文件夹
**文件夹**: `weights/`
**大小**: 约7GB
**说明**: YOLO11m训练100轮的模型权重

**包含文件**:
- `best.pt` (110MB) - **最佳模型** ⭐
  - mAP@0.5: 98.95%
  - Precision: 97.48%
  - Recall: 96.91%
- `last.pt` (110MB) - 最后一个epoch的模型
- `epoch0.pt` ~ `epoch95.pt` (每个327MB) - 训练过程checkpoint

**使用方法**:
1. 从百度网盘下载 `weights/` 文件夹
2. 放置到项目的 `models/` 目录
3. 推理时使用: `models/weights/best.pt`

---

## 下载后的目录结构

```
fgy/
├── data/
│   └── vest_merged/              # 从 fgy.rar 解压得到
│       ├── images/
│       │   ├── train/            # 27,414张训练图片
│       │   ├── val/              # 6,794张验证图片
│       │   └── test/             # 9,994张测试图片
│       ├── labels/
│       │   ├── train/            # 训练标签
│       │   ├── val/              # 验证标签
│       │   └── test/             # 测试标签
│       └── data.yaml             # 数据集配置
│
└── models/
    └── weights/                  # 从百度网盘下载
        ├── best.pt              # ⭐ 用于推理
        ├── last.pt
        └── epoch*.pt            # 训练checkpoint
```

---

## 文件大小汇总

| 文件/文件夹 | 大小 | 说明 |
|------------|------|------|
| **fgy.rar** | **9.8GB** | 数据集压缩包 |
| **weights/** | **~7GB** | 模型权重文件夹 |
| ├─ best.pt | 110MB | 最佳模型 ⭐ |
| ├─ last.pt | 110MB | 最后checkpoint |
| └─ epoch*.pt | ~6.5GB | 训练过程checkpoint (可选) |
| **总计** | **~16GB** | |

---

## 快速开始

### 1. Clone 项目
```bash
git clone https://github.com/1225Sakura/yolo11reflective-vest.git
cd yolo11reflective-vest
```

### 2. 下载并配置数据
从百度网盘下载 `fgy.rar` 和 `weights/`

```bash
# 解压数据集
unrar x fgy.rar data/

# 复制模型权重
cp -r weights/ models/
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 开始使用
```bash
# 推理
python evaluate_test.py

# 两阶段检测（人员穿戴判定）
python two_stage_detection_fixed.py

# 重新训练
python train_yolo11_stable.py
```

---

## 注意事项

- 训练可视化结果（曲线图、混淆矩阵等）已包含在GitHub仓库的 `assets/training_results/` 目录中
- 推荐使用 `best.pt` 进行推理，性能最优
- 如需从头训练，建议使用 `train_yolo11_stable.py` 脚本
