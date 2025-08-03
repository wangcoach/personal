import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processor import parse_df_to_res, validate_dataframe
from utils.calculator import cal, generate_grid_and_calculate
from utils.visualizer import plot_heatmap, plot_scatter, create_summary_stats
import io

def main():
    st.set_page_config(
        page_title="OVLX/OVLY 分析系统",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 OVLX/OVLY 方程分析系统")
    st.markdown("---")
    
    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 配置参数")
        
        # 网格参数
        st.subheader("网格设置")
        x_min = st.number_input("X 最小值", value=0.0, step=0.1)
        x_max = st.number_input("X 最大值", value=1.0, step=0.1)
        y_min = st.number_input("Y 最小值", value=0.0, step=0.1)
        y_max = st.number_input("Y 最大值", value=1.0, step=0.1)
        
        grid_size = st.selectbox("网格密度", [20, 30, 50, 100], index=2)
        
        # 可视化参数
        st.subheader("可视化设置")
        plot_type = st.selectbox("图表类型", ["热力图", "散点图", "两者都显示"])
        colormap_ovlx = st.selectbox("OVLX 颜色主题", ["viridis", "plasma", "coolwarm", "RdYlBu"])
        colormap_ovly = st.selectbox("OVLY 颜色主题", ["plasma", "viridis", "coolwarm", "RdBu"])
    
    # 主页面
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("📁 数据输入")
        
        # 文件上传
        uploaded_file = st.file_uploader(
            "选择 Excel 文件",
            type=['xlsx', 'xls'],
            help="上传包含方程系数的 Excel 文件"
        )
        
        # 示例数据
        if st.button("使用示例数据"):
            st.session_state['use_sample'] = True
        
        # 数据预览
        if uploaded_file is not None or st.session_state.get('use_sample', False):
            try:
                if uploaded_file is not None:
                    df = pd.read_excel(uploaded_file)
                    st.session_state['df'] = df
                else:
                    # 使用示例数据
                    sample_data = {
                        'X22': [2], 'X21': [1], 'X20': [1.0], 'X2(y)': ['4*y + 1'],
                        'X32': [2.0], 'X31': [1], 'X30': [1], 'X3(y)': ['y**2 + 4*y + 1'],
                        'X2': [2], 'X1': [1], 'X0': [1.0], 'X(y)': ['y**2 + 2*y + 1'],
                        'Y6': [1.0], 'Y5': [0.8], 'Y4': [0.6], 'Y(x)': ['3*x + 3']
                    }
                    df = pd.DataFrame(sample_data)
                    st.session_state['df'] = df
                
                st.success("✅ 数据加载成功！")
                st.subheader("数据预览")
                st.dataframe(df, use_container_width=True)
                
                # 数据验证
                validation_result = validate_dataframe(df)
                if validation_result['is_valid']:
                    st.success("✅ 数据格式验证通过")
                else:
                    st.error(f"❌ 数据格式错误: {validation_result['error']}")
                    return
                
            except Exception as e:
                st.error(f"❌ 文件读取失败: {str(e)}")
                return
    
    with col2:
        st.header("📈 分析结果")
        
        if 'df' in st.session_state:
            df = st.session_state['df']
            
            # 解析数据
            with st.spinner("正在解析数据..."):
                result = parse_df_to_res(df)
            
            # 显示解析结果
            with st.expander("查看解析后的方程结构"):
                st.json(result)
            
            # 计算网格点
            if st.button("🚀 开始计算", type="primary"):
                x_range = (x_min, x_max)
                y_range = (y_min, y_max)
                
                with st.spinner(f"正在计算 {grid_size}x{grid_size} 网格点..."):
                    try:
                        progress_bar = st.progress(0)
                        grid_results = generate_grid_and_calculate(
                            result, x_range, y_range, 
                            grid_size, grid_size, 
                            progress_callback=lambda p: progress_bar.progress(p)
                        )
                        
                        st.session_state['grid_results'] = grid_results
                        st.success(f"✅ 计算完成！共 {len(grid_results)} 个点")
                        
                    except Exception as e:
                        st.error(f"❌ 计算失败: {str(e)}")
                        return
    
    # 结果展示
    if 'grid_results' in st.session_state:
        grid_results = st.session_state['grid_results']
        
        st.markdown("---")
        st.header("📊 分析结果")
        
        # 统计信息
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("数据点总数", len(grid_results))
        
        with col2:
            st.metric("OVLX 范围", f"{grid_results['ovlx'].min():.3f} ~ {grid_results['ovlx'].max():.3f}")
        
        with col3:
            st.metric("OVLY 范围", f"{grid_results['ovly'].min():.3f} ~ {grid_results['ovly'].max():.3f}")
        
        # 详细统计
        with st.expander("详细统计信息"):
            stats_col1, stats_col2 = st.columns(2)
            
            with stats_col1:
                st.subheader("OVLX 统计")
                st.write(grid_results['ovlx'].describe())
            
            with stats_col2:
                st.subheader("OVLY 统计")
                st.write(grid_results['ovly'].describe())
        
        # 可视化
        st.subheader("📈 可视化结果")
        
        if plot_type in ["热力图", "两者都显示"]:
            st.markdown("#### 热力图")
            fig_heatmap = plot_heatmap(grid_results, colormap_ovlx, colormap_ovly)
            st.pyplot(fig_heatmap, use_container_width=True)
        
        if plot_type in ["散点图", "两者都显示"]:
            st.markdown("#### 散点图")
            fig_scatter = plot_scatter(grid_results, colormap_ovlx, colormap_ovly)
            st.pyplot(fig_scatter, use_container_width=True)
        
        # 数据下载
        st.markdown("---")
        st.subheader("💾 数据下载")
        
        # 转换为CSV
        csv = grid_results.to_csv(index=False)
        st.download_button(
            label="📥 下载计算结果 (CSV)",
            data=csv,
            file_name=f"ovlx_ovly_results_{grid_size}x{grid_size}.csv",
            mime="text/csv"
        )
        
        # 显示原始数据
        with st.expander("查看计算结果数据"):
            st.dataframe(grid_results, use_container_width=True)

if __name__ == "__main__":
    if 'use_sample' not in st.session_state:
        st.session_state['use_sample'] = False
    main()