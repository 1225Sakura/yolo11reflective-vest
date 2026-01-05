#!/bin/bash
# 评估脚本

echo "========================================="
echo "  反光衣检测 - 模型评估"
echo "========================================="

# 进入项目目录
cd "$(dirname "$0")/.."

# 检查模型是否存在
if [ ! -f "models/checkpoints/best_model.pth" ] && [ ! -f "models/checkpoints/final_model.pth" ]; then
    echo "错误: 未找到训练好的模型"
    echo "请先运行训练: bash scripts/train.sh"
    exit 1
fi

# 运行评估
echo "开始评估..."
python3 src/eval/evaluate.py

echo "========================================="
echo "评估完成！"
echo "========================================="
