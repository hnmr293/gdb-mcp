# Claude Code に GDB MCP サーバーを追加する方法

## 1. プロジェクトのインストール

まず、GDB MCPサーバーをインストールします：

```bash
cd /path/to/gdb-mcp
pip install -e .
```

または、uvを使用している場合：

```bash
cd /path/to/gdb-mcp
uv pip install -e .
```

## 2. Claude Code 設定ファイルの編集

### 設定ファイルの場所

- **Linux/WSL**: `~/.config/claude/claude_code_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_code_config.json`
- **Windows**: `%APPDATA%\Claude\claude_code_config.json`

### 設定の追加

設定ファイルを開いて、`mcpServers`セクションに以下を追加します：

```json
{
  "mcpServers": {
    "gdb-mcp": {
      "command": "gdb-mcp"
    }
  }
}
```

#### フルパスを使用する場合

インストールせずに直接実行する場合：

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

#### uvを使用する場合

```json
{
  "mcpServers": {
    "gdb-mcp": {
      "command": "uv",
      "args": ["run", "gdb-mcp"],
      "cwd": "/path/to/gdb-mcp"
    }
  }
}
```

### 既存の設定がある場合

既に他のMCPサーバーが設定されている場合は、カンマで区切って追加します：

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "existing-command"
    },
    "gdb-mcp": {
      "command": "gdb-mcp"
    }
  }
}
```

## 3. Claude Code の再起動

設定を反映させるには、Claude Codeを再起動する必要があります。

## 4. 動作確認

Claude Codeで以下のように確認できます：

1. **リソースの確認**:
   ```
   「GDBコマンドリファレンスを見せて」
   ```

2. **ツールの使用**:
   ```
   「GDBセッションを開始して、簡単なデバッグをしてみて」
   ```

## トラブルシューティング

### エラー: "gdb-mcp: command not found"

```json
{
  "mcpServers": {
    "gdb-mcp": {
      "command": "python",
      "args": ["-m", "gdb_mcp"],
      "cwd": "/path/to/gdb-mcp/src"
    }
  }
}
```

### GDBが見つからない場合

GDBがインストールされていることを確認：

```bash
# Ubuntu/Debian
sudo apt-get install gdb

# macOS
brew install gdb

# Fedora/RHEL
sudo dnf install gdb
```

### ログの確認

Claude Codeのログで詳細を確認できます：
- Linux/WSL: `~/.config/claude/logs/`
- macOS: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%\Claude\logs\`

## 使用例

### 基本的なデバッグセッション

```
「GDBでhello.cをデバッグしたい」
```

Claude Codeは自動的に：
1. GDBセッションを開始
2. プログラムをロード
3. ブレークポイントの設定
4. デバッグコマンドの実行

### GDBコマンドの参照

```
「GDBのbreakコマンドの使い方を教えて」
```

MCPサーバーのリソースから自動的に情報を取得して回答します。