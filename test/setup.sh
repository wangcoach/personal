#!/bin/bash

echo "正在设置 OVLX/OVLY 分析系统..."
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "1. 创建虚拟环境..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "创建虚拟环境失败"
    exit 1
fi

echo "2. 激活虚拟环境..."
source venv/bin/activate

echo "3. 安装依赖包..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "安装依赖失败"
    exit 1
fi

echo "4. 生成示例数据..."
cd data
python create_sample_data.py
cd ..

echo
echo "✅ 安装完成！"
echo
echo "运行应用请执行:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo
