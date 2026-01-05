# 大文件清单 - 需要上传到百度网盘

## 文件位置说明

所有大文件都在 `reflective_vest_detection/` 目录下,**不要移动到GitHub仓库**。

---

## 需要上传到百度网盘的文件

### 方案一: 推荐方案 (约10GB)

#### 1. 数据集 (9.8GB)
**文件**: `reflective_vest_detection/data/fgy.rar`
**说明**: 原始数据集压缩包

#### 2. 最佳训练模型 (110MB)
**文件**: `reflective_vest_detection/yolo_runs/yolo11x_vest_final/train/weights/best.pt`
**说明**: 训练100轮后的最佳模型

---

### 方案二: 完整版 (约10GB)

包含方案一的所有文件,另外添加:

#### 3. 最后checkpoint (110MB)
**文件**: `reflective_vest_detection/yolo_runs/yolo11x_vest_final/train/weights/last.pt`
**说明**: 最后一个epoch的模型

#### 4. 预训练权重 (110MB, 可选)
**文件**: `reflective_vest_detection/yolo11x.pt`
**说明**: YOLO11x预训练权重 (可从Ultralytics官方下载,不上传也可以)

---

## 百度网盘目录结构建议

```
reflective-vest-detection/
├── dataset/
│   └── fgy.rar                    # 9.8GB 原始数据集
├── models/
│   ├── best.pt                    # 110MB 最佳训练模型 ⭐
│   └── last.pt                    # 110MB 最后checkpoint (可选)
└── 下载说明.txt
```

---

## 下载说明.txt 模板

```
反光衣检测项目 - 数据集和模型下载说明

【文件说明】
1. dataset/fgy.rar (9.8GB)
   - 反光衣数据集,包含训练/验证/测试集
   - YOLO格式标注

2. models/best.pt (110MB)
   - YOLO11m训练的最佳模型
   - 在vest_merged数据集上训练100轮

3. models/last.pt (110MB, 可选)
   - 训练最后一轮的模型

【使用方法】
1. Clone GitHub仓库:
   git clone https://github.com/你的用户名/仓库名.git
   cd 仓库名

2. 下载并解压数据集:
   - 下载 dataset/fgy.rar
   - 解压到项目的 data/ 目录
   - 确保解压后路径为: data/vest_merged/

3. 下载模型文件:
   - 下载 models/best.pt
   - 放置到项目的 models/ 目录

4. 安装依赖:
   pip install -r requirements.txt

5. 开始使用:
   - 训练: python train_yolo11.py
   - 推理: python evaluate_test.py
   - 两阶段检测: python two_stage_detection_fixed.py

【详细文档】
请查看 GitHub 仓库的 README.md

项目地址: https://github.com/你的用户名/仓库名
```

---

## 不需要上传的大文件

以下文件较大但不需要上传(训练过程文件):

- ❌ `reflective_vest_detection/yolo_runs/*/weights/epoch*.pt` - 训练中间checkpoint
- ❌ `reflective_vest_detection/*.log` - 训练日志文件
- ❌ `reflective_vest_detection/logs*/` - 日志目录
- ❌ `reflective_vest_detection/results/` - 训练结果
- ❌ `reflective_vest_detection/runs/` - YOLO运行结果
- ❌ `reflective_vest_detection/two_stage_results*/` - 两阶段检测结果

---

## 文件大小汇总

| 文件 | 大小 | 是否上传 |
|------|------|---------|
| fgy.rar | 9.8GB | ✅ 必须 |
| best.pt | 110MB | ✅ 必须 |
| last.pt | 110MB | ⚠️ 可选 |
| yolo11x.pt | 110MB | ⚠️ 可选(官方可下载) |
| **总计** | **~10GB** | |

---

## 快速上传命令 (Windows)

如果要将文件复制到统一目录准备上传:

```bash
# 创建上传目录
mkdir upload_to_baidu

# 复制数据集
copy reflective_vest_detection\data\fgy.rar upload_to_baidu\

# 创建models子目录
mkdir upload_to_baidu\models

# 复制最佳模型
copy reflective_vest_detection\yolo_runs\yolo11x_vest_final\train\weights\best.pt upload_to_baidu\models\

# (可选) 复制last.pt
copy reflective_vest_detection\yolo_runs\yolo11x_vest_final\train\weights\last.pt upload_to_baidu\models\
```

然后将 `upload_to_baidu` 目录上传到百度网盘即可。
