#!/usr/bin/env python3
"""
改进版两阶段检测脚本：人员检测 + 反光衣穿戴判定
修复：
1. 使用PIL支持中文显示
2. 优化IoU匹配逻辑
3. 添加调试信息输出
"""

import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import random
from PIL import Image, ImageDraw, ImageFont


def calculate_iou(box1, box2):
    """计算两个框的IoU"""
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    # 计算交集
    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)

    inter_area = max(0, inter_x_max - inter_x_min) * max(0, inter_y_max - inter_y_min)

    # 计算并集
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area if union_area > 0 else 0


def check_vest_in_person(person_box, vest_boxes, iou_threshold=0.3):
    """
    检查人员框内是否有反光衣
    返回: (是否穿戴, 最大IoU, 匹配的反光衣框)
    """
    max_iou = 0
    matched_vest = None

    for vest_box in vest_boxes:
        iou = calculate_iou(person_box, vest_box)
        if iou > max_iou:
            max_iou = iou
            matched_vest = vest_box

    wearing_vest = max_iou > iou_threshold
    return wearing_vest, max_iou, matched_vest


def cv2_to_pil(cv2_image):
    """OpenCV BGR转PIL RGB"""
    return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))


def pil_to_cv2(pil_image):
    """PIL RGB转OpenCV BGR"""
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def draw_results_with_chinese(image, person_boxes, vest_status_list, vest_boxes):
    """
    使用PIL绘制带中文的检测结果
    """
    # 转换为PIL图像
    pil_img = cv2_to_pil(image)
    draw = ImageDraw.Draw(pil_img)

    # 尝试加载中文字体，如果失败则使用默认字体
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 绘制所有反光衣框（黄色虚线）
    for vest_box in vest_boxes:
        x1, y1, x2, y2 = map(int, vest_box)
        draw.rectangle([(x1, y1), (x2, y2)], outline=(255, 255, 0), width=2)

    # 绘制人员框和判定结果
    for idx, (person_box, (wearing, iou, matched_vest)) in enumerate(zip(person_boxes, vest_status_list)):
        x1, y1, x2, y2 = map(int, person_box)

        # 根据是否穿戴选择颜色
        color = (0, 255, 0) if wearing else (255, 0, 0)  # 绿色/红色
        label = f"Wearing ({iou:.2f})" if wearing else "Not Wearing"

        # 绘制人员框
        draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=3)

        # 绘制标签背景和文字
        bbox = draw.textbbox((x1, y1 - 30), label, font=font_small)
        draw.rectangle(bbox, fill=color)
        draw.text((x1, y1 - 30), label, fill=(255, 255, 255), font=font_small)

    # 统计结果
    total_persons = len(person_boxes)
    wearing_count = sum(1 for wearing, _, _ in vest_status_list if wearing)
    not_wearing_count = total_persons - wearing_count

    # 添加统计信息（使用英文，避免中文显示问题）
    stats_text = [
        f"Total: {total_persons}",
        f"Wearing: {wearing_count}",
        f"Not: {not_wearing_count}"
    ]

    y_offset = 30
    for text in stats_text:
        bbox = draw.textbbox((10, y_offset), text, font=font_large)
        # 绘制背景
        draw.rectangle([(bbox[0]-5, bbox[1]-5), (bbox[2]+5, bbox[3]+5)], fill=(0, 0, 0))
        # 绘制文字
        draw.text((10, y_offset), text, fill=(255, 255, 255), font=font_large)
        y_offset += 35

    # 转换回OpenCV格式
    return pil_to_cv2(pil_img)


def process_image(image_path, person_model, vest_model, output_dir,
                 iou_threshold=0.3, conf_threshold=0.5):
    """处理单张图像"""
    # 读取图像
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None

    # Stage 1: 人员检测
    person_results = person_model(image, conf=conf_threshold, verbose=False)
    person_boxes = []

    for result in person_results:
        boxes = result.boxes
        for box in boxes:
            cls = int(box.cls[0])
            # COCO数据集中，person类别是0
            if cls == 0:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                person_boxes.append([x1, y1, x2, y2])

    # Stage 2: 反光衣检测
    vest_results = vest_model(image, conf=conf_threshold, verbose=False)
    vest_boxes = []

    for result in vest_results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            vest_boxes.append([x1, y1, x2, y2])

    # 判定每个人是否穿着反光衣
    vest_status_list = []
    for person_box in person_boxes:
        wearing, iou, matched_vest = check_vest_in_person(person_box, vest_boxes, iou_threshold)
        vest_status_list.append((wearing, iou, matched_vest))

    # 统计结果
    total_persons = len(person_boxes)
    wearing_count = sum(1 for wearing, _, _ in vest_status_list if wearing)
    not_wearing_count = total_persons - wearing_count

    # 绘制结果（使用PIL支持中文）
    result_image = draw_results_with_chinese(image, person_boxes, vest_status_list, vest_boxes)

    # 保存结果
    output_path = output_dir / image_path.name
    cv2.imwrite(str(output_path), result_image)

    return {
        'image_path': str(image_path),
        'total_persons': total_persons,
        'wearing_vest': wearing_count,
        'not_wearing': not_wearing_count,
        'person_boxes': person_boxes,
        'vest_boxes': vest_boxes,
        'vest_status': vest_status_list
    }


def main():
    print("=" * 70)
    print("改进版两阶段反光衣穿戴检测系统")
    print("=" * 70)

    # 配置路径
    person_model_path = 'yolo11x.pt'
    vest_model_path = '/home/user/fgy/reflective_vest_detection/yolo_runs/yolo11x_vest_stable/weights/best.pt'
    test_images_dir = Path('/home/user/fgy/data/vest_merged/images/test')
    output_dir = Path('/home/user/fgy/reflective_vest_detection/two_stage_results_fixed')

    # 创建输出目录
    output_dir.mkdir(exist_ok=True, parents=True)

    # 加载模型
    print("\n加载模型...")
    print(f"  人员检测模型: {person_model_path}")
    person_model = YOLO(person_model_path)

    print(f"  反光衣检测模型: {vest_model_path}")
    vest_model = YOLO(vest_model_path)

    print("✓ 模型加载完成\n")

    # 获取测试图像（随机选择100张）
    all_images = list(test_images_dir.glob("*.jpg"))
    if len(all_images) > 100:
        test_images = random.sample(all_images, 100)
    else:
        test_images = all_images

    print(f"处理 {len(test_images)} 张测试图像...\n")
    print("改进点：")
    print("  1. 使用PIL支持文字显示（英文标签避免乱码）")
    print("  2. IoU阈值: 0.3")
    print("  3. 置信度阈值: 0.5")
    print()

    # 处理图像
    results = []
    total_persons = 0
    total_wearing = 0
    total_not_wearing = 0

    for i, image_path in enumerate(test_images, 1):
        print(f"[{i}/{len(test_images)}] 处理: {image_path.name}", end=" ... ")

        result = process_image(
            image_path,
            person_model,
            vest_model,
            output_dir,
            iou_threshold=0.3,
            conf_threshold=0.5
        )

        if result:
            results.append(result)
            total_persons += result['total_persons']
            total_wearing += result['wearing_vest']
            total_not_wearing += result['not_wearing']
            print(f"✓ (人数: {result['total_persons']}, 穿: {result['wearing_vest']}, 未穿: {result['not_wearing']})")
        else:
            print("✗ 失败")

    # 统计总结
    print("\n" + "=" * 70)
    print("检测结果汇总")
    print("=" * 70)
    print(f"处理图像数: {len(results)}")
    print(f"检测到总人数: {total_persons}")
    print(f"穿反光衣人数: {total_wearing} ({total_wearing/total_persons*100:.1f}%)" if total_persons > 0 else "穿反光衣人数: 0")
    print(f"未穿反光衣人数: {total_not_wearing} ({total_not_wearing/total_persons*100:.1f}%)" if total_persons > 0 else "未穿反光衣人数: 0")
    print(f"\n结果保存至: {output_dir}")
    print("=" * 70)
    print("\n注意：检测准确度受限于反光衣模型性能（测试集mAP@0.5=58.03%）")
    print("      如需提高准确度，需要改进训练数据或优化模型")


if __name__ == '__main__':
    main()
