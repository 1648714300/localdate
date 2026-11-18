#!/usr/bin/env python3
"""LocalDate 技能自检：零依赖、纯标准库。

交付前跑一次，确认目录结构、SKILL.md 元信息与必需资源齐备。
用法：python scripts/verify.py [技能根目录]
退出码：0 全通过；1 有失败项。
"""

import os
import re
import sys

GREEN, RED, YELLOW, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[0m"


def ok(msg):
    print(f"  {GREEN}OK{RESET}  {msg}")


def fail(msg):
    print(f"  {RED}FAIL{RESET}  {msg}")
    return 1


def warn(msg):
    print(f"  {YELLOW}WARN{RESET}  {msg}")


def verify(root):
    errors = 0
    print(f"== LocalDate 自检：{root} ==")

    # 1. SKILL.md 存在
    skill_md = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill_md):
        return fail("SKILL.md 不存在，无法继续")

    with open(skill_md, encoding="utf-8") as f:
        content = f.read()

    # 2. frontmatter 格式
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        errors += fail("SKILL.md 缺 YAML frontmatter（--- 包裹）")
    else:
        fm = m.group(1)
        if re.search(r"^name:\s*\S+", fm, re.M):
            ok("frontmatter name 存在")
        else:
            errors += fail("frontmatter 缺 name")
        if re.search(r"^description:\s*\S+", fm, re.M):
            ok("frontmatter description 存在")
        else:
            errors += fail("frontmatter 缺 description")
        if re.search(r"^agent_created:\s*true", fm, re.M):
            ok("agent_created: true 存在（可被技能管理修改/删除）")
        else:
            errors += warn("缺 agent_created: true（本机 skill_manage 将无法修改/删除）")

    # 3. 必需目录
    for d in ["city-packs", "city-pack-template", "assets", "tools", "scripts", "docs", "feedback"]:
        p = os.path.join(root, d)
        if os.path.isdir(p):
            ok(f"目录 {d}/ 存在")
        else:
            errors += fail(f"缺目录 {d}/")

    # 4. 必需文件
    for f in ["ALGORITHM.md", "FEEDBACK.md", "README.md", "LICENSE",
              "tools/score_lite.py", "tools/feedback.py",
              "feedback/feedback.jsonl", "scripts/verify.py"]:
        p = os.path.join(root, f)
        if os.path.isfile(p):
            ok(f"文件 {f} 存在")
        else:
            errors += fail(f"缺文件 {f}")

    # 5. city-pack 完整性
    packs_dir = os.path.join(root, "city-packs")
    if os.path.isdir(packs_dir):
        packs = [d for d in os.listdir(packs_dir)
                 if os.path.isdir(os.path.join(packs_dir, d))]
        if packs:
            ok(f"城市包：{', '.join(packs)}")
            for pack in packs:
                for req in ["SKILL.md", "weights.md", "output_template.md", "catalog"]:
                    p = os.path.join(packs_dir, pack, req)
                    if not os.path.exists(p):
                        errors += warn(f"城市包 {pack} 缺 {req}")
        else:
            errors += fail("city-packs/ 下没有任何城市包")

    # 6. 算法脚本可运行性（语法编译，不执行业务逻辑，不落盘 pyc）
    for f in ["tools/score_lite.py", "tools/feedback.py"]:
        p = os.path.join(root, f)
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as fh:
                    compile(fh.read(), p, "exec")
                ok(f"{f} 语法通过")
            except SyntaxError as e:
                errors += fail(f"{f} 语法错误：{e}")

    print()
    if errors:
        print(f"{RED}结果：{errors} 项失败/警告，请修复后再交付。{RESET}")
    else:
        print(f"{GREEN}结果：全部通过，可交付。{RESET}")
    return 1 if errors else 0


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.exit(verify(os.path.abspath(root)))
