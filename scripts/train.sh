#!/bin/bash
# 训练脚本

echo "========================================="
echo "  反光衣检测 - 开始训练"
echo "========================================="

# 进入项目目录
cd "$(dirname "$0")"

# 检查环境
echo "检查 Python 环境..."
python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')" || {
    echo "错误: PyTorch 未正确安装"
    exit 1
}

# 检查数据集
echo "检查数据集..."
if [ ! -d "data/fgy/images/train" ]; then
    echo "错误: 训练数据集不存在"
    exit 1
fi

# 创建必要的目录
mkdir -p models/checkpoints
mkdir -p logs
mkdir -p results

# 开始训练
echo "========================================="
echo "开始训练..."
echo "========================================="

python3 src/train/train.py

echo "========================================="
echo "训练完成！"
echo "========================================="
echo "检查点保存在: models/checkpoints/"
echo "日志保存在: logs/"
echo ""
echo "运行评估: bash scripts/evaluate.sh"
