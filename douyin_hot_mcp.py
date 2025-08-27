#!/usr/bin/env python3
"""
抖音热榜MCP工具
基于MoreAPI的抖音热榜API开发的MCP工具

功能：
- 获取抖音热榜数据
- 支持不同榜单类型
"""

import json
import logging
import requests
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# ================================
# 1. 配置工具
# ================================
TOOL_NAME = "抖音热榜MCP工具"
API_BASE_URL = "http://api.moreapi.cn"
API_TOKEN = "llqNHPkpHAL4blLj41W6MVtt2SCNujJmlajY7ZEvdOlL1gm9lQTsaTyY32SK4Jyd"

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(TOOL_NAME)

# 创建MCP服务器
mcp = FastMCP(TOOL_NAME)

# ================================
# 2. API调用函数
# ================================

def call_douyin_api(endpoint: str, data: dict) -> dict:
    """
    调用抖音API的通用函数
    
    Args:
        endpoint (str): API端点
        data (dict): 请求数据
        
    Returns:
        dict: API响应结果
    """
    try:
        url = f"{API_BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API请求失败: {e}")
        raise
    except Exception as e:
        logger.error(f"API调用错误: {e}")
        raise

def format_hot_value(hot_value: int) -> str:
    """
    格式化热度值显示
    
    Args:
        hot_value (int): 热度值
        
    Returns:
        str: 格式化后的热度值
    """
    if hot_value > 100000000:
        return f'{hot_value/100000000:.1f}亿'
    elif hot_value > 10000:
        return f'{hot_value/10000:.1f}万'
    else:
        return f'{hot_value:,}'

def parse_hot_board_data(result: dict) -> dict:
    """
    解析热榜数据并格式化
    
    Args:
        result (dict): API返回的原始数据
        
    Returns:
        dict: 解析后的格式化数据
    """
    parsed_data = {
        "success": False,
        "message": "",
        "hot_list": [],
        "trending_list": [],
        "total_count": 0,
        "response_time": result.get('time', 'unknown'),
        "status": result.get('msg', 'unknown')
    }
    
    try:
        # 检查数据结构并提取热榜
        if 'data' in result and isinstance(result['data'], dict):
            data_obj = result['data']
            
            # 从data.data.word_list获取热榜数据
            if 'data' in data_obj and isinstance(data_obj['data'], dict):
                inner_data = data_obj['data']
                
                # 提取热榜词条
                if 'word_list' in inner_data and isinstance(inner_data['word_list'], list):
                    word_list = inner_data['word_list']
                    parsed_data["total_count"] = len(word_list)
                    
                    for item in word_list:
                        if isinstance(item, dict):
                            word = item.get('word', '无内容')
                            hot_value = item.get('hot_value', 0)
                            position = item.get('position', 0)
                            label = item.get('label', '')
                            
                            parsed_data["hot_list"].append({
                                "position": position,
                                "word": word,
                                "hot_value": hot_value,
                                "hot_display": format_hot_value(hot_value),
                                "label": label
                            })
                
                # 提取趋势数据
                if 'trending_list' in inner_data and isinstance(inner_data['trending_list'], list):
                    trending_list = inner_data['trending_list']
                    for trend in trending_list:
                        if isinstance(trend, dict):
                            word = trend.get('word', '无内容')
                            parsed_data["trending_list"].append(word)
                
                parsed_data["success"] = True
                parsed_data["message"] = "热榜数据解析成功"
            else:
                parsed_data["message"] = "数据结构异常：未找到内层data字段"
        else:
            parsed_data["message"] = "数据结构异常：未找到data字段"
            
    except Exception as e:
        parsed_data["message"] = f"数据解析失败: {str(e)}"
    
    return parsed_data

def format_hot_board_display(parsed_data: dict, top_count: int = 20) -> str:
    """
    格式化热榜数据为显示文本
    
    Args:
        parsed_data (dict): 解析后的热榜数据
        top_count (int): 显示的条目数量
        
    Returns:
        str: 格式化后的显示文本
    """
    if not parsed_data["success"]:
        return f"❌ 热榜数据解析失败: {parsed_data['message']}"
    
    lines = []
    lines.append("🔥 抖音热榜实时数据")
    lines.append("=" * 60)
    lines.append(f"📅 获取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"📊 数据状态: {parsed_data['status']}")
    lines.append(f"⏱️ 响应时间: {parsed_data['response_time']}")
    lines.append(f"📈 热榜词条数量: {parsed_data['total_count']}")
    lines.append("=" * 60)
    
    if parsed_data["hot_list"]:
        lines.append(f"\n🏆 抖音热榜 TOP {min(top_count, len(parsed_data['hot_list']))}:")
        lines.append("=" * 60)
        
        for i, item in enumerate(parsed_data["hot_list"][:top_count], 1):
            position = item["position"] or i
            word = item["word"]
            hot_display = item["hot_display"]
            label = item["label"]
            
            lines.append(f"{position:2d}. {word}")
            if item["hot_value"] > 0:
                lines.append(f"    🔥 热度: {hot_display}")
            if label:
                lines.append(f"    🏷️ {label}")
            lines.append("")
    
    if parsed_data["trending_list"]:
        lines.append("\n📊 热门趋势:")
        lines.append("-" * 40)
        for i, trend in enumerate(parsed_data["trending_list"][:5], 1):
            lines.append(f"{i}. {trend}")
        lines.append("")
    
    return "\n".join(lines)

# ================================
# 3. MCP工具函数
# ================================

@mcp.tool()
def get_douyin_hot_board(board_type: str = "0", board_sub_type: str = "", proxy: str = "") -> str:
    """
    获取抖音热榜数据
    
    Args:
        board_type (str): 榜单类型，默认为"0"
        board_sub_type (str): 榜单子类型，默认为空
        proxy (str): 代理设置，默认为空
        
    Returns:
        str: 格式化的热榜数据显示
    """
    try:
        # 构建请求数据
        request_data = {
            "board_type": board_type,
            "board_sub_type": board_sub_type,
            "proxy": proxy
        }
        
        logger.info(f"正在获取抖音热榜数据，参数: {request_data}")
        
        # 调用API
        result = call_douyin_api("/api/douyin/aweme_board", request_data)
        
        # 解析数据
        parsed_data = parse_hot_board_data(result)
        
        if parsed_data["success"]:
            # 返回格式化的热榜显示
            return format_hot_board_display(parsed_data, top_count=20)
        else:
            # 返回原始数据作为备选
            response = {
                "status": "success",
                "message": "成功获取抖音热榜数据（原始格式）",
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "parse_error": parsed_data["message"],
                "data": result
            }
            return f"✅ 抖音热榜获取成功\n\n{json.dumps(response, indent=2, ensure_ascii=False)}"
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP错误: {e.response.status_code} - {e.response.text if e.response else '未知错误'}"
        logger.error(error_msg)
        return f"❌ API请求失败: {error_msg}"
        
    except requests.exceptions.Timeout:
        error_msg = "请求超时，请稍后重试"
        logger.error(error_msg)
        return f"❌ {error_msg}"
        
    except requests.exceptions.ConnectionError:
        error_msg = "网络连接错误，请检查网络连接"
        logger.error(error_msg)
        return f"❌ {error_msg}"
        
    except Exception as e:
        error_msg = f"获取热榜失败: {str(e)}"
        logger.error(error_msg)
        return f"❌ {error_msg}"

@mcp.tool()
def get_douyin_hot_board_simple() -> str:
    """
    获取抖音热榜数据（简化版本，使用默认参数）
    
    Returns:
        str: 格式化的热榜数据显示
    """
    return get_douyin_hot_board()

@mcp.tool()
def get_douyin_hot_board_analysis(top_count: int = 10) -> str:
    """
    获取抖音热榜数据并进行详细分析
    
    Args:
        top_count (int): 显示的热榜条目数量，默认为10
        
    Returns:
        str: 包含分析的热榜数据显示
    """
    try:
        # 获取热榜数据
        request_data = {
            "board_type": "0",
            "board_sub_type": "",
            "proxy": ""
        }
        
        result = call_douyin_api("/api/douyin/aweme_board", request_data)
        parsed_data = parse_hot_board_data(result)
        
        if not parsed_data["success"]:
            return f"❌ 热榜数据解析失败: {parsed_data['message']}"
        
        # 基本显示
        display_text = format_hot_board_display(parsed_data, top_count=top_count)
        
        # 添加分析信息
        analysis_lines = []
        analysis_lines.append("\n📊 热榜数据分析:")
        analysis_lines.append("-" * 40)
        
        if parsed_data["hot_list"]:
            hot_list = parsed_data["hot_list"]
            
            # 统计信息
            total_items = len(hot_list)
            items_with_heat = len([item for item in hot_list if item["hot_value"] > 0])
            items_with_labels = len([item for item in hot_list if item["label"]])
            
            analysis_lines.append(f"总热榜条目: {total_items}")
            analysis_lines.append(f"有热度值的条目: {items_with_heat}")
            analysis_lines.append(f"有标签的条目: {items_with_labels}")
            
            # 热度统计
            if items_with_heat > 0:
                heat_values = [item["hot_value"] for item in hot_list if item["hot_value"] > 0]
                max_heat = max(heat_values)
                min_heat = min(heat_values)
                avg_heat = sum(heat_values) / len(heat_values)
                
                analysis_lines.append(f"最高热度: {format_hot_value(max_heat)}")
                analysis_lines.append(f"最低热度: {format_hot_value(min_heat)}")
                analysis_lines.append(f"平均热度: {format_hot_value(int(avg_heat))}")
            
            # 标签统计
            if items_with_labels > 0:
                labels = [item["label"] for item in hot_list if item["label"]]
                from collections import Counter
                label_counts = Counter(labels)
                
                analysis_lines.append("\n🏷️ 热门标签:")
                for label, count in label_counts.most_common(5):
                    analysis_lines.append(f"  {label}: {count}次")
        
        return display_text + "\n" + "\n".join(analysis_lines)
        
    except Exception as e:
        return f"❌ 热榜分析失败: {str(e)}"

@mcp.tool()
def check_api_status() -> str:
    """
    检查API服务状态
    
    Returns:
        str: API状态信息
    """
    try:
        # 尝试调用API检查状态
        test_data = {
            "board_type": "0",
            "board_sub_type": "",
            "proxy": ""
        }
        
        result = call_douyin_api("/api/douyin/aweme_board", test_data)
        
        status_info = {
            "api_status": "正常",
            "api_url": API_BASE_URL,
            "token_configured": bool(API_TOKEN),
            "test_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "response_received": True
        }
        
        return f"✅ API状态检查完成\n\n{json.dumps(status_info, indent=2, ensure_ascii=False)}"
        
    except Exception as e:
        status_info = {
            "api_status": "异常",
            "api_url": API_BASE_URL,
            "token_configured": bool(API_TOKEN),
            "test_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "error": str(e)
        }
        
        return f"❌ API状态异常\n\n{json.dumps(status_info, indent=2, ensure_ascii=False)}"

# ================================
# 4. 启动服务器
# ================================
if __name__ == "__main__":
    logger.info(f"启动 {TOOL_NAME}")
    logger.info(f"API地址: {API_BASE_URL}")
    logger.info(f"Token已配置: {'是' if API_TOKEN else '否'}")
    
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("正在关闭...")
    finally:
        logger.info("服务器已关闭")

# ================================
# 5. 使用说明
# ================================
"""
🚀 抖音热榜MCP工具使用说明：

🔧 可用工具：
1. get_douyin_hot_board(board_type, board_sub_type, proxy)
   - 获取抖音热榜数据（完整参数版本）
   - board_type: 榜单类型（默认"0"）
   - board_sub_type: 榜单子类型（默认空）
   - proxy: 代理设置（默认空）
   - 返回格式化的热榜显示，包含 TOP 20

2. get_douyin_hot_board_simple()
   - 获取抖音热榜数据（简化版本，使用默认参数）
   - 返回格式化的热榜显示，包含 TOP 20

3. get_douyin_hot_board_analysis(top_count)
   - 获取抖音热榜数据并进行详细分析
   - top_count: 显示的热榜条目数量（默认10）
   - 返回包含数据分析的热榜显示

4. check_api_status()
   - 检查API服务状态
   - 返回API连接和服务可用性信息

📝 使用示例：
- 获取默认热榜: get_douyin_hot_board_simple()
- 获取特定榜单: get_douyin_hot_board("1", "music")
- 热榜数据分析: get_douyin_hot_board_analysis(15)
- 检查API状态: check_api_status()

🔑 配置信息：
- API地址: http://api.moreapi.cn
- Token: 已配置
- 端点: /api/douyin/aweme_board

🌆 特色功能：
- 智能数据解析：自动解析API返回的复杂数据结构
- 热度值格式化：自动将大数字转换为易读的万、亿格式
- 分类标签显示：显示热榜内容的相关标签信息
- 趋势分析：额外显示热门趋势数据
- 统计分析：提供热度值统计和标签分布分析
- 错误处理：完善的异常处理和错误信息提示

⚠️ 注意事项：
- 确保网络连接正常
- API Token需要有效
- 遵守API使用限制
- 数据仅供参考，实时性取决于API提供商
"""

# ================================
# 6. 快速测试函数（只在直接运行时使用）
# ================================

def test_hot_board():
    """
    快速测试热榜功能
    """
    print("🧪 正在测试抖音热榜MCP工具...")
    
    try:
        # 测试API连接
        request_data = {
            "board_type": "0",
            "board_sub_type": "",
            "proxy": ""
        }
        
        result = call_douyin_api("/api/douyin/aweme_board", request_data)
        parsed_data = parse_hot_board_data(result)
        
        if parsed_data["success"]:
            display = format_hot_board_display(parsed_data, top_count=5)
            print(display)
            print("\n✅ 测试成功！MCP工具工作正常。")
        else:
            print(f"⚠️ 数据解析失败: {parsed_data['message']}")
            print("但API连接正常，工具可以使用。")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")