# GDB MCP サーバーのテスト方法

## 1. 環境のセットアップ

### 依存関係のインストール
```bash
pip install -e .
# または
pip install mcp
```

## 2. サーバーの起動テスト

### 方法1: 直接実行
```bash
python examples/run_server.py
```

### 方法2: パッケージとして実行
```bash
python -m gdb_mcp
```

### 方法3: src付きで実行
```bash
cd src && python -m gdb_mcp
```

## 3. MCP Inspector を使用したテスト

MCP Inspector は MCP サーバーをテストするための公式ツールです。

### インストール
```bash
npm install -g @modelcontextprotocol/inspector
```

### 実行
```bash
# 別のターミナルでサーバーを起動
mcp-inspector python examples/run_server.py
```

ブラウザで `http://localhost:5173` を開き、以下を確認：

1. **Resources タブ**:
   - `gdb://commands/reference` - 完全なリファレンス
   - `gdb://commands/cli` - CLIコマンド
   - `gdb://commands/mi` - MIコマンド
   - `gdb://commands/mapping` - コマンドマッピング

2. 各リソースをクリックして内容を確認

## 4. Claude Desktop での設定

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) または
`%APPDATA%/Claude/claude_desktop_config.json` (Windows) に以下を追加：

```json
{
  "mcpServers": {
    "gdb-mcp": {
      "command": "python",
      "args": ["/path/to/gdb-mcp/examples/run_server.py"]
    }
  }
}
```

## 5. プログラムからのテスト

### テストクライアントの実行

`examples/test_client.py` を使用：

```bash
python examples/test_client.py
```

### テストクライアントのコード例
```python
#!/usr/bin/env python3
"""Test client for GDB MCP server."""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_resources():
    server_params = StdioServerParameters(
        command="python",
        args=["examples/run_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List resources
            resources = await session.list_resources()
            print("Available resources:")
            for resource in resources:
                print(f"  - {resource.uri}: {resource.name}")
            
            # Read a resource
            content = await session.read_resource("gdb://commands/cli")
            print(f"\nCLI Commands content preview:")
            print(content.contents[0].text[:500] + "...")

if __name__ == "__main__":
    asyncio.run(test_resources())
```

## 6. コマンドラインでの簡易テスト

### JSON-RPC リクエストを送信
```bash
# サーバーを起動してテスト
echo '{"jsonrpc": "2.0", "method": "resources/list", "params": {}, "id": 1}' | python examples/run_server.py
```

## 7. デバッグ

### ログレベルを上げる
`src/server.py` でログレベルを変更：
```python
logging.basicConfig(level=logging.DEBUG)
```

### エラーのトラブルシューティング

1. **ModuleNotFoundError**: 
   ```bash
   pip install -e .
   ```

2. **Permission denied**:
   ```bash
   chmod +x examples/run_server.py
   ```

3. **Port already in use** (MCP Inspector):
   別のポートを使用：
   ```bash
   mcp-inspector --port 5174 python examples/run_server.py
   ```

## 8. 期待される出力

正常に動作している場合、MCP Inspector で以下が表示されます：

- **Resources** タブに4つのリソースがリストされる
- 各リソースをクリックすると、対応するMarkdownコンテンツが表示される
- エラーメッセージが表示されない

## 使用例

Claude Desktop で設定後：
```
「GDBのbreakコマンドについて教えて」
→ MCPサーバーが自動的にリソースを提供
```