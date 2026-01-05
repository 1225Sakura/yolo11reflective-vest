#!/usr/bin/env python3
"""
YOLOv11反光衣检测训练脚本 - 稳定版
使用YOLOv11x（最大最准确的版本）
目标：mAP@0.5 >= 85%, Precision >= 85%

修复内容：
1. 禁用AMP混合精度，避免数值溢出
2. 降低学习率，增强训练稳定性
3. 减小batch size，降低内存压力
4. 延迟mosaic关闭时机，平滑过渡
5. 禁用激进的数据增强
"""

from ultralytics import YOLO
import torch

def main():
    print("=" * 60)
    print("YOLOv11 反光衣检测训练 - 稳定版")
    print("=" * 60)

    # 检查GPU
    print(f"\n可用GPU数量: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")

    # 加载YOLOv11x模型（最大最准确的版本）
    print("\n加载YOLOv11x预训练模型...")
    model = YOLO('yolo11x.pt')

    # 训练参数
    print("\n开始训练...")
    print("训练配置（稳定版）:")
    print("  - 模型: YOLOv11x")
    print("  - 图像尺寸: 640x640")
    print("  - Batch size: 32 (降低以提高稳定性)")
    print("  - Epochs: 100")
    print("  - 数据集: vest_merged")
    print("  - GPU: 4x RTX 4090")
    print("  - 优化器: AdamW")
    print("  - 学习率: 0.001 (降低10倍)")
    print("  - 混合精度: 禁用 (避免数值溢出)")
    print()

    # 开始训练
    results = model.train(
        # 数据配置
        data='/home/user/fgy/data/vest_merged/vest_data.yaml',

        # 训练参数
        epochs=100,              # 训练轮数
        imgsz=640,               # 输入图像尺寸
        batch=32,                # 修改1: 降低batch size (64->32)

        # 硬件配置
        device=[0, 1, 2, 3],     # 使用4个GPU
        workers=8,               # 数据加载线程数

        # 优化器配置
        optimizer='AdamW',       # 优化器
        lr0=0.001,               # 修改2: 降低初始学习率 (0.01->0.001)
        lrf=0.01,                # 最终学习率（相对于lr0）
        momentum=0.937,          # SGD momentum/Adam beta1
        weight_decay=0.0005,     # 权重衰减
        warmup_epochs=5,         # 修改3: 增加warmup轮数 (3->5)
        warmup_momentum=0.8,     # warmup初始momentum

        # 数据增强（温和设置）
        hsv_h=0.01,              # 修改4: 降低色调增强 (0.015->0.01)
        hsv_s=0.5,               # 修改5: 降低饱和度增强 (0.7->0.5)
        hsv_v=0.3,               # 修改6: 降低亮度增强 (0.4->0.3)
        degrees=0.0,             # 旋转角度
        translate=0.1,           # 平移
        scale=0.5,               # 缩放
        shear=0.0,               # 剪切
        perspective=0.0,         # 透视
        flipud=0.0,              # 上下翻转概率
        fliplr=0.5,              # 左右翻转概率
        mosaic=1.0,              # mosaic增强概率
        mixup=0.0,               # mixup增强概率
        copy_paste=0.0,          # copy-paste增强概率
        auto_augment=None,       # 修改7: 禁用auto_augment
        erasing=0.0,             # 修改8: 禁用random erasing (0.4->0.0)
        close_mosaic=50,         # 修改9: 延迟mosaic关闭 (10->50)

        # 训练控制
        patience=30,             # 修改10: 增加早停patience (20->30)
        save=True,               # 保存检查点
        save_period=5,           # 每5个epoch保存一次

        # 验证配置
        val=True,                # 启用验证

        # 输出配置
        project='/home/user/fgy/reflective_vest_detection/yolo_runs',
        name='yolo11x_vest_stable',
        exist_ok=True,

        # 可视化
        plots=True,              # 生成训练图表
        verbose=True,            # 详细输出

        # 性能优化
        amp=False,               # 修改11: 禁用混合精度 (True->False)
        fraction=1.0,            # 使用全部数据

        # 其他
        seed=42,                 # 随机种子
        deterministic=True,      # 确定性训练
    )

    print("\n" + "=" * 60)
    print("训练完成！")
    print("=" * 60)

    # 打印最佳结果
    print(f"\n最佳模型保存路径: {model.trainer.best}")
    print(f"最后模型保存路径: {model.trainer.last}")

    # 验证最佳模型
    print("\n使用最佳模型进行验证...")
    best_model = YOLO(model.trainer.best)
    metrics = best_model.val()

    print("\n最终性能指标:")
    print(f"  mAP@0.5: {metrics.box.map50:.4f} ({metrics.box.map50*100:.2f}%)")
    print(f"  mAP@0.5:0.95: {metrics.box.map:.4f} ({metrics.box.map*100:.2f}%)")
    print(f"  Precision: {metrics.box.p.mean():.4f} ({metrics.box.p.mean()*100:.2f}%)")
    print(f"  Recall: {metrics.box.r.mean():.4f} ({metrics.box.r.mean()*100:.2f}%)")

    # 检查是否达到目标
    if metrics.box.map50 >= 0.85:
        print(f"\n达到目标！mAP@0.5 = {metrics.box.map50*100:.2f}% >= 85%")
    else:
        print(f"\n未达目标。mAP@0.5 = {metrics.box.map50*100:.2f}% < 85%")

    if metrics.box.p.mean() >= 0.85:
        print(f"达到目标！Precision = {metrics.box.p.mean()*100:.2f}% >= 85%")
    else:
        print(f"未达目标。Precision = {metrics.box.p.mean()*100:.2f}% < 85%")

if __name__ == '__main__':
    main()
