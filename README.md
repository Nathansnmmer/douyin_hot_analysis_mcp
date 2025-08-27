# 抖音热榜MCP工具使用说明

## 📋 工具概述

这是一个基于MoreAPI的抖音热榜MCP工具，可以获取抖音平台的热门内容榜单数据。

## 🚀 功能特性

- ✅ 获取抖音热榜数据
- ✅ 支持多种榜单类型
- ✅ 提供API状态检查
- ✅ 完整的错误处理
- ✅ JSON格式化输出

## 🔧 可用工具

### 1. get_douyin_hot_board
获取抖音热榜数据（完整参数版本）

**参数：**
- `board_type` (str): 榜单类型，默认为"0"
- `board_sub_type` (str): 榜单子类型，默认为空
- `proxy` (str): 代理设置，默认为空

**示例：**
```python
get_douyin_hot_board("0", "", "")
```

### 2. get_douyin_hot_board_simple
获取抖音热榜数据（简化版本）

使用默认参数，更便于快速调用。

**示例：**
```python
get_douyin_hot_board_simple()
```

### 3. check_api_status
检查API服务状态

用于验证API连接和服务可用性。

**示例：**
```python
check_api_status()
```

## 🛠️ 安装和使用

### 方法1：直接运行
```bash
cd d:\mcpdemo\made-mcp
python douyin_hot_mcp.py
```

### 方法2：配置到MCP客户端
将 `mcp_config.json` 中的配置添加到您的MCP客户端配置文件中。

## 📊 返回数据格式

工具返回JSON格式的数据，包含：
- `status`: 请求状态（success/error）
- `message`: 状态描述
- `timestamp`: 请求时间戳
- `data`: 热榜数据内容

## ⚙️ 配置信息

- **API地址**: http://api.moreapi.cn
- **API端点**: /api/douyin/aweme_board
- **认证**: Bearer Token
- **Token**: 已配置（llqNHPkpHAL4blLj41W6MVtt2SCNujJmlajY7ZEvdOlL1gm9lQTsaTyY32SK4Jyd）

## 🧪 测试结果

✅ **语法检查**: 通过  
✅ **模块导入**: 通过  
✅ **API连接**: 通过（状态码200，响应长度65878字符）  
✅ **MCP框架**: 通过  

## ⚠️ 注意事项

1. **网络连接**: 确保网络连接正常，能够访问api.moreapi.cn
2. **API限制**: 请遵守API提供商的使用限制和频率限制
3. **Token有效性**: 确保API Token保持有效状态
4. **错误处理**: 工具内置了完整的错误处理机制

## 📝 文件结构

```
made-mcp/
├── douyin_hot_mcp.py          # 主工具文件
├── mcp_config.json            # MCP配置文件
├── test_douyin_mcp.py         # 完整测试脚本
├── simple_test.py             # 简单API测试
├── test_api.py                # API连接测试
└── README.md                  # 本说明文件
```

## 🔍 故障排除

如果遇到问题，请按以下步骤检查：

1. **检查网络连接**
   ```bash
   python simple_test.py
   ```

2. **检查MCP框架**
   ```bash
   python -c "from mcp.server.fastmcp import FastMCP; print('OK')"
   ```

3. **查看详细错误信息**
   ```bash
   python douyin_hot_mcp.py
   ```

## 📞 技术支持

如有问题，请检查：
- API Token是否有效
- 网络连接是否正常
- Python环境是否完整
- 依赖模块是否安装

## 📈 更新记录

- **v1.0.0** (2025-08-23): 初始版本，实现基础热榜获取功能
