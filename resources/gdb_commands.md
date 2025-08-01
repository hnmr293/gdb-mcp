# GDB Command Reference

This document provides a comprehensive reference for GDB commands in both CLI (Command Line Interface) and MI (Machine Interface) modes.

## Table of Contents
1. [CLI Commands](#cli-commands)
2. [MI Commands](#mi-commands)
3. [Command Correspondence](#command-correspondence)

## CLI Commands

### Execution Control

| Command | Abbreviation | Description | Usage |
|---------|--------------|-------------|-------|
| `run` | `r` | Start program execution | `run [args]` |
| `continue` | `c` | Continue execution until next breakpoint | `continue [ignore-count]` |
| `step` | `s` | Single step (enters functions) | `step [count]` |
| `next` | `n` | Single step (over functions) | `next [count]` |
| `finish` | `fin` | Execute until current function returns | `finish` |
| `until` | `u` | Continue until reaching next source line | `until [location]` |
| `stepi` | `si` | Step one instruction (enters calls) | `stepi [count]` |
| `nexti` | `ni` | Step one instruction (over calls) | `nexti [count]` |
| `jump` | `j` | Continue execution at specified location | `jump location` |

### Breakpoints

| Command | Abbreviation | Description | Usage |
|---------|--------------|-------------|-------|
| `break` | `b` | Set breakpoint | `break [location]` |
| `tbreak` | `tb` | Set temporary breakpoint | `tbreak [location]` |
| `hbreak` | `hb` | Set hardware breakpoint | `hbreak [location]` |
| `watch` | - | Set watchpoint | `watch expression` |
| `rwatch` | - | Set read watchpoint | `rwatch expression` |
| `awatch` | - | Set access watchpoint | `awatch expression` |
| `clear` | - | Delete breakpoints at location | `clear [location]` |
| `delete` | `d` | Delete breakpoints | `delete [breakpoint-numbers]` |
| `disable` | `dis` | Disable breakpoints | `disable [breakpoint-numbers]` |
| `enable` | `en` | Enable breakpoints | `enable [breakpoint-numbers]` |
| `condition` | - | Set breakpoint condition | `condition bnum expression` |
| `commands` | - | Set commands for breakpoint | `commands [bnum]` |

### Stack Examination

| Command | Abbreviation | Description | Usage |
|---------|--------------|-------------|-------|
| `backtrace` | `bt` | Display stack backtrace | `backtrace [n]` |
| `where` | - | Alias for backtrace | `where [n]` |
| `frame` | `f` | Select and print stack frame | `frame [n]` |
| `up` | - | Move up stack frame | `up [n]` |
| `down` | `do` | Move down stack frame | `down [n]` |
| `info frame` | `i f` | Print info about frame | `info frame [addr]` |
| `info locals` | `i lo` | Print local variables | `info locals` |
| `info args` | `i ar` | Print function arguments | `info args` |

### Data Examination

| Command | Abbreviation | Description | Usage |
|---------|--------------|-------------|-------|
| `print` | `p` | Print value of expression | `print [/f] expression` |
| `display` | `disp` | Display expression each time | `display [/f] expression` |
| `undisplay` | `undisp` | Cancel display expressions | `undisplay [display-numbers]` |
| `set variable` | `set var` | Assign value to variable | `set variable var = value` |
| `x` | - | Examine memory | `x/[n][f][u] address` |
| `whatis` | - | Print data type | `whatis expression` |
| `ptype` | - | Print type definition | `ptype expression` |

### Source Code

| Command | Abbreviation | Description | Usage |
|---------|--------------|-------------|-------|
| `list` | `l` | List source code | `list [location]` |
| `search` | - | Search forward for regexp | `search regexp` |
| `reverse-search` | `rev` | Search backward for regexp | `reverse-search regexp` |
| `directory` | `dir` | Add directory to source path | `directory dirname` |

### Program Information

| Command | Abbreviation | Description | Usage |
|---------|--------------|-------------|-------|
| `info breakpoints` | `i b` | List breakpoints | `info breakpoints [n]` |
| `info watchpoints` | - | List watchpoints | `info watchpoints` |
| `info registers` | `i r` | List registers | `info registers [regname]` |
| `info threads` | `i th` | List threads | `info threads` |
| `info functions` | `i fu` | List functions | `info functions [regexp]` |
| `info variables` | `i va` | List global/static variables | `info variables [regexp]` |
| `info program` | - | Execution status of program | `info program` |

### File and Process Control

| Command | Abbreviation | Description | Usage |
|---------|--------------|-------------|-------|
| `file` | - | Load symbol table | `file filename` |
| `exec-file` | - | Specify executable | `exec-file filename` |
| `symbol-file` | - | Load symbol table | `symbol-file filename` |
| `attach` | - | Attach to process | `attach process-id` |
| `detach` | - | Detach from process | `detach` |
| `kill` | `k` | Kill execution of program | `kill` |
| `quit` | `q` | Exit GDB | `quit` |

### Miscellaneous

| Command | Abbreviation | Description | Usage |
|---------|--------------|-------------|-------|
| `help` | `h` | Get help | `help [command]` |
| `apropos` | - | Search for commands | `apropos word` |
| `shell` | `sh` | Execute shell command | `shell command` |
| `make` | - | Execute make | `make [args]` |
| `cd` | - | Change directory | `cd directory` |
| `pwd` | - | Print working directory | `pwd` |

## MI Commands

GDB/MI is a machine-oriented text interface designed for use by programs that want to use GDB as a component.

### MI Command Format
- All MI commands start with a dash (`-`)
- Commands can have options and parameters
- Output is in a structured format suitable for parsing

### Breakpoint Commands

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-break-after` | Set ignore count | `number count` | `-break-after 2 5` |
| `-break-commands` | Set breakpoint commands | `number command1 command2...` | `-break-commands 1 "print x" "continue"` |
| `-break-condition` | Set condition | `number expr` | `-break-condition 1 x>5` |
| `-break-delete` | Delete breakpoints | `( breakpoint )+` | `-break-delete 1 2 3` |
| `-break-disable` | Disable breakpoints | `( breakpoint )+` | `-break-disable 1 2` |
| `-break-enable` | Enable breakpoints | `( breakpoint )+` | `-break-enable 1 2` |
| `-break-info` | Get breakpoint info | `breakpoint` | `-break-info 1` |
| `-break-insert` | Insert breakpoint | `[ -t ] [ -h ] [ -f ] [ -d ] [ -a ] [ -c condition ] [ -i ignore-count ] [ -p thread-id ] [ location ]` | `-break-insert main` |
| `-break-list` | List breakpoints | - | `-break-list` |
| `-break-passcount` | Set tracepoint pass count | `tracepoint-number passcount` | `-break-passcount 1 100` |
| `-break-watch` | Create watchpoint | `[ -a | -r ] expression` | `-break-watch x` |
| `-dprintf-insert` | Insert dynamic printf | `[ -t ] [ -f ] [ -d ] [ -c condition ] [ -i ignore-count ] [ -p thread-id ] [ location ] [ format ] [ argument ]` | `-dprintf-insert main "x=%d\\n" x` |

### Program Execution

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-exec-continue` | Resume execution | `[--reverse] [--all\|--thread-group N]` | `-exec-continue` |
| `-exec-finish` | Finish function | `[--reverse]` | `-exec-finish` |
| `-exec-interrupt` | Interrupt execution | `[--all\|--thread-group N]` | `-exec-interrupt` |
| `-exec-jump` | Jump to location | `location` | `-exec-jump main` |
| `-exec-next` | Step over | `[--reverse]` | `-exec-next` |
| `-exec-next-instruction` | Step over instruction | `[--reverse]` | `-exec-next-instruction` |
| `-exec-return` | Return from function | - | `-exec-return` |
| `-exec-run` | Start execution | `[--all \| --thread-group N] [--start]` | `-exec-run` |
| `-exec-step` | Step into | `[--reverse]` | `-exec-step` |
| `-exec-step-instruction` | Step into instruction | `[--reverse]` | `-exec-step-instruction` |
| `-exec-until` | Execute until | `[location]` | `-exec-until 100` |

### Stack Manipulation

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-enable-frame-filters` | Enable frame filters | - | `-enable-frame-filters` |
| `-stack-info-frame` | Get frame info | - | `-stack-info-frame` |
| `-stack-info-depth` | Get stack depth | `[max-depth]` | `-stack-info-depth 10` |
| `-stack-list-arguments` | List arguments | `[--no-frame-filters] [--skip-unavailable] print-values [low-frame high-frame]` | `-stack-list-arguments 1` |
| `-stack-list-frames` | List frames | `[--no-frame-filters low-frame high-frame]` | `-stack-list-frames` |
| `-stack-list-locals` | List local variables | `[--no-frame-filters] [--skip-unavailable] print-values` | `-stack-list-locals 1` |
| `-stack-list-variables` | List all variables | `[--no-frame-filters] [--skip-unavailable] print-values` | `-stack-list-variables 1` |
| `-stack-select-frame` | Select frame | `framenum` | `-stack-select-frame 2` |

### Data Manipulation

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-data-disassemble` | Disassemble | `-s start-addr -e end-addr [ -f filename ] [ -l linenum ] [ -n lines ] [ -- mode ]` | `-data-disassemble -s $pc -e "$pc + 20" -- 0` |
| `-data-evaluate-expression` | Evaluate expression | `expr` | `-data-evaluate-expression "x+y"` |
| `-data-list-changed-registers` | List changed registers | - | `-data-list-changed-registers` |
| `-data-list-register-names` | List register names | `[ ( regno )+ ]` | `-data-list-register-names` |
| `-data-list-register-values` | List register values | `fmt [ ( regno )+ ]` | `-data-list-register-values x` |
| `-data-read-memory` | Read memory | `[ -o byte-offset ] address word-format word-size nr-rows nr-cols [ aschar ]` | `-data-read-memory 0x0000 x 4 10 10` |
| `-data-read-memory-bytes` | Read memory bytes | `address count` | `-data-read-memory-bytes 0x0000 100` |
| `-data-write-memory-bytes` | Write memory bytes | `address contents` | `-data-write-memory-bytes 0x0000 "0011223344"` |

### Variable Objects

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-var-create` | Create variable object | `name frame-addr expression` | `-var-create myvar * x` |
| `-var-delete` | Delete variable object | `[ -c ] name` | `-var-delete myvar` |
| `-var-set-format` | Set display format | `name format-spec` | `-var-set-format myvar hex` |
| `-var-show-format` | Show display format | `name` | `-var-show-format myvar` |
| `-var-info-num-children` | Get number of children | `name` | `-var-info-num-children myvar` |
| `-var-list-children` | List children | `[print-values] name [from to]` | `-var-list-children myvar` |
| `-var-info-type` | Get variable type | `name` | `-var-info-type myvar` |
| `-var-info-expression` | Get variable expression | `name` | `-var-info-expression myvar` |
| `-var-info-path-expression` | Get path expression | `name` | `-var-info-path-expression myvar` |
| `-var-show-attributes` | Show attributes | `name` | `-var-show-attributes myvar` |
| `-var-evaluate-expression` | Evaluate variable | `[-f format-spec] name` | `-var-evaluate-expression myvar` |
| `-var-assign` | Assign value | `name expression` | `-var-assign myvar 10` |
| `-var-update` | Update variable | `[print-values] name` | `-var-update myvar` |
| `-var-set-frozen` | Freeze variable | `name flag` | `-var-set-frozen myvar 1` |

### File Commands

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-file-exec-and-symbols` | Specify executable and symbols | `file` | `-file-exec-and-symbols /path/to/exe` |
| `-file-exec-file` | Specify executable | `file` | `-file-exec-file /path/to/exe` |
| `-file-list-exec-source-file` | List current source | - | `-file-list-exec-source-file` |
| `-file-list-exec-source-files` | List all sources | - | `-file-list-exec-source-files` |
| `-file-symbol-file` | Read symbol table | `file` | `-file-symbol-file /path/to/symbols` |

### Thread Commands

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-thread-info` | Get thread info | `[thread-id]` | `-thread-info` |
| `-thread-list-ids` | List thread IDs | - | `-thread-list-ids` |
| `-thread-select` | Select thread | `thread-id` | `-thread-select 2` |

### Target Commands

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-target-attach` | Attach to process | `pid | gid | file` | `-target-attach 1234` |
| `-target-detach` | Detach from target | `[pid | gid]` | `-target-detach` |
| `-target-disconnect` | Disconnect from target | - | `-target-disconnect` |
| `-target-download` | Download to target | - | `-target-download` |
| `-target-select` | Select target | `type parameters` | `-target-select remote localhost:1234` |

### Support Commands

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-gdb-exit` | Exit GDB | - | `-gdb-exit` |
| `-gdb-set` | Set GDB variable | `args` | `-gdb-set print pretty on` |
| `-gdb-show` | Show GDB variable | `variable` | `-gdb-show print pretty` |
| `-gdb-version` | Show GDB version | - | `-gdb-version` |
| `-info-gdb-mi-command` | Query command support | `cmd_name` | `-info-gdb-mi-command break-insert` |
| `-list-features` | List supported features | - | `-list-features` |
| `-list-target-features` | List target features | - | `-list-target-features` |
| `-list-thread-groups` | List thread groups | `[--available] [--recurse 1] [group]` | `-list-thread-groups` |

### Miscellaneous Commands

| MI Command | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `-enable-pretty-printing` | Enable pretty printing | - | `-enable-pretty-printing` |
| `-inferior-tty-set` | Set inferior tty | `terminal` | `-inferior-tty-set /dev/pts/1` |
| `-inferior-tty-show` | Show inferior tty | - | `-inferior-tty-show` |
| `-interpreter-exec` | Execute in interpreter | `interpreter command` | `-interpreter-exec console "print x"` |

## Command Correspondence

### CLI to MI Mapping

| CLI Command | MI Equivalent |
|-------------|---------------|
| `break` | `-break-insert` |
| `delete` | `-break-delete` |
| `disable` | `-break-disable` |
| `enable` | `-break-enable` |
| `condition` | `-break-condition` |
| `tbreak` | `-break-insert -t` |
| `hbreak` | `-break-insert -h` |
| `watch` | `-break-watch` |
| `rwatch` | `-break-watch -r` |
| `awatch` | `-break-watch -a` |
| `info breakpoints` | `-break-list` |
| `run` | `-exec-run` |
| `continue` | `-exec-continue` |
| `step` | `-exec-step` |
| `next` | `-exec-next` |
| `finish` | `-exec-finish` |
| `until` | `-exec-until` |
| `stepi` | `-exec-step-instruction` |
| `nexti` | `-exec-next-instruction` |
| `return` | `-exec-return` |
| `jump` | `-exec-jump` |
| `interrupt` | `-exec-interrupt` |
| `backtrace` | `-stack-list-frames` |
| `frame` | `-stack-select-frame` |
| `up` | (use `-stack-select-frame` with frame calculation) |
| `down` | (use `-stack-select-frame` with frame calculation) |
| `info locals` | `-stack-list-locals` |
| `info args` | `-stack-list-arguments` |
| `print` | `-data-evaluate-expression` |
| `x` | `-data-read-memory` |
| `disassemble` | `-data-disassemble` |
| `info registers` | `-data-list-register-values` |
| `attach` | `-target-attach` |
| `detach` | `-target-detach` |
| `file` | `-file-exec-and-symbols` |
| `exec-file` | `-file-exec-file` |
| `symbol-file` | `-file-symbol-file` |
| `info threads` | `-thread-info` |
| `thread` | `-thread-select` |
| `quit` | `-gdb-exit` |
| `set` | `-gdb-set` |
| `show` | `-gdb-show` |

## MI Output Format

MI commands produce output in a specific format:

### Result Records
```
^done[,results]
^running
^connected
^error,msg="message"
^exit
```

### Async Records
```
*stopped,reason="breakpoint-hit",bkptno="1",thread-id="1"
*running,thread-id="all"
=thread-group-added,id="i1"
```

### Stream Records
```
~"output from program\n"
@"target output"
&"log output"
```

### Example MI Session
```
(gdb)
-break-insert main
^done,bkpt={number="1",type="breakpoint",disp="keep",enabled="y",
addr="0x08048440",func="main",file="test.c",fullname="/home/test.c",
line="10",thread-groups=["i1"],times="0",original-location="main"}
(gdb)
-exec-run
^running
*running,thread-id="all"
(gdb)
*stopped,reason="breakpoint-hit",disp="keep",bkptno="1",frame={
addr="0x08048440",func="main",args=[],file="test.c",
fullname="/home/test.c",line="10"},thread-id="1",stopped-threads="all"
(gdb)
```

## Notes

1. **Abbreviations**: Most CLI commands can be abbreviated to their shortest unambiguous form.
2. **Auto-repeat**: Pressing Enter in CLI mode repeats the last command (useful for stepping).
3. **MI Stability**: The MI interface is designed to be stable across GDB versions for programmatic use.
4. **Output Parsing**: MI output is designed to be easily parsed by programs, while CLI output is human-readable.
5. **Asynchronous Operation**: MI supports asynchronous operation where commands can be issued while the target is running.

## References

- [GDB Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html)
- [GDB/MI Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb.html/GDB_002fMI.html)