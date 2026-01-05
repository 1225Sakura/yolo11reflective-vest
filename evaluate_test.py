#!/usr/bin/env python3
"""
测试集评估脚本
使用最佳模型在测试集上进行评估
"""

from ultralytics import YOLO
import sys

def main():
    print("=" * 60)
    print("测试集评估 - YOLOv11x 最佳模型")
    print("=" * 60)

    # 加载最佳模型
    model_path = '/home/user/fgy/reflective_vest_detection/yolo_runs/yolo11x_vest_stable/weights/best.pt'
    print(f"\n加载模型: {model_path}")

    try:
        model = YOLO(model_path)
        print("模型加载成功！")
    except Exception as e:
        print(f"模型加载失败: {e}")
        sys.exit(1)

    # 在测试集上评估
    print("\n" + "=" * 60)
    print("开始测试集评估...")
    print("=" * 60)
    print(f"测试集: 9,994 张图像")
    print()

    # 评估参数
    metrics = model.val(
        data='/home/user/fgy/data/vest_merged/vest_data.yaml',
        split='test',  # 使用测试集
        batch=32,
        imgsz=640,
        device=[0, 1, 2, 3],  # 使用4个GPU
        verbose=True,
        plots=True,
        save_json=False,
    )

    print("\n" + "=" * 60)
    print("测试集评估结果")
    print("=" * 60)

    # 提取指标
    precision = metrics.box.p.mean()
    recall = metrics.box.r.mean()
    map50 = metrics.box.map50
    map50_95 = metrics.box.map

    print(f"\n核心指标:")
    print(f"  Precision:       {precision:.4f} ({precision*100:.2f}%)")
    print(f"  Recall:          {recall:.4f} ({recall*100:.2f}%)")
    print(f"  mAP@0.5:         {map50:.4f} ({map50*100:.2f}%)")
    print(f"  mAP@0.5:0.95:    {map50_95:.4f} ({map50_95*100:.2f}%)")

    # 检查目标达成
    print("\n目标达成情况:")
    if map50 >= 0.85:
        print(f"  ✓ mAP@0.5 = {map50*100:.2f}% >= 85% (超出 {(map50-0.85)*100:.2f}%)")
    else:
        print(f"  ✗ mAP@0.5 = {map50*100:.2f}% < 85% (差距 {(0.85-map50)*100:.2f}%)")

    if precision >= 0.85:
        print(f"  ✓ Precision = {precision*100:.2f}% >= 85% (超出 {(precision-0.85)*100:.2f}%)")
    else:
        print(f"  ✗ Precision = {precision*100:.2f}% < 85% (差距 {(0.85-precision)*100:.2f}%)")

    print("\n" + "=" * 60)
    print("评估完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
