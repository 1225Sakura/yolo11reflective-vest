#!/bin/bash
# 推理脚本

echo "========================================="
echo "  反光衣检测 - 批量推理"
echo "========================================="

# 进入项目目录
cd "$(dirname "$0")/.."

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: bash scripts/inference.sh <图片路径或文件夹>"
    echo ""
    echo "示例:"
    echo "  单张图片: bash scripts/inference.sh data/fgy/images/val/000009.jpg"
    echo "  文件夹:   bash scripts/inference.sh data/fgy/images/val"
    exit 1
fi

INPUT=$1
OUTPUT=${2:-"results/predictions"}
CONF_THRESHOLD=${3:-0.5}

# 检查输入
if [ ! -e "$INPUT" ]; then
    echo "错误: 输入路径不存在: $INPUT"
    exit 1
fi

# 检查模型
if [ ! -f "models/checkpoints/best_model.pth" ] && [ ! -f "models/checkpoints/final_model.pth" ]; then
    echo "错误: 未找到训练好的模型"
    exit 1
fi

# 判断是文件还是目录
if [ -f "$INPUT" ]; then
    echo "推理单张图片: $INPUT"
    python3 src/eval/inference.py \
        --image "$INPUT" \
        --output "$OUTPUT" \
        --conf_threshold "$CONF_THRESHOLD"
elif [ -d "$INPUT" ]; then
    echo "批量推理文件夹: $INPUT"
    python3 src/eval/inference.py \
        --image_dir "$INPUT" \
        --output "$OUTPUT" \
        --conf_threshold "$CONF_THRESHOLD"
fi

echo "========================================="
echo "推理完成！"
echo "========================================="
echo "结果保存在: $OUTPUT"
