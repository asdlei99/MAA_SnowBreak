from pathlib import Path

import PyInstaller.__main__

import shutil
import sys
import json

from configure import configure_ocr_model


working_dir = Path(__file__).parent
install_path = working_dir / Path("install")
version = len(sys.argv) > 1 and sys.argv[1] or "v0.0.1"


def install_deps():
    if not (working_dir / "deps" / "bin").exists():
        print('Please download the MaaFramework to "deps" first.')
        print('请先下载 MaaFramework 到 "deps"。')
        sys.exit(1)

    shutil.copytree(
        working_dir / "deps" / "bin",
        install_path,
        ignore=shutil.ignore_patterns(
            "*MaaDbgControlUnit*",
            "*MaaThriftControlUnit*",
            "*MaaRpc*",
            "*MaaHttp*",
        ),
        dirs_exist_ok=True,
    )
    shutil.copytree(
        working_dir / "deps" / "share" / "MaaAgentBinary",
        install_path / "MaaAgentBinary",
        dirs_exist_ok=True,
    )


def install_resource():

    configure_ocr_model()

    shutil.copytree(
        working_dir / "assets" / "resource",
        install_path / "resource",
        dirs_exist_ok=True,
    )
    shutil.copy2(
        working_dir / "assets" / "interface.json",
        install_path,
    )

    with open(install_path / "interface.json", "r", encoding="utf-8") as f:
        interface: dict = json.load(f)

    interface["version"] = version

    #添加agent的配置
    interface["agent"] = interface.get("agent", {})#如果没有agent,则创建一个
    if sys.platform == "win32":
        interface["agent"]["child_exec"] = "{PROJECT_DIR}/agent/agent.exe"
    elif sys.platform == "darwin" or "linux":
        interface["agent"]["child_exec"] = "{PROJECT_DIR}/agent/agent"#linux和macos的可执行文件均为agent
    interface["agent"]["child_args"] = interface.get("agent", {}).get(
        "child_args", ["{PROJECT_DIR}"]
    )  # {PROJECT_DIR}为maafw的dll/so文件路径,通过参数传递给agent
    # 如果有其他的参数,需要在{PROJECT_DIR}的前面添加,需要保证{PROJECT_DIR}为最后一位

    with open(install_path / "interface.json", "w", encoding="utf-8") as f:
        json.dump(interface, f, ensure_ascii=False, indent=4)


def install_chores():
    shutil.copy2(
        working_dir / "README.md",
        install_path,
    )
    shutil.copy2(
        working_dir / "LICENSE",
        install_path,
    )


def install_agent():
    # 名字为agent
    command = [
        str(working_dir /"assets"/ "agent" / "main.py"),
        "--name=agent",
        "--clean",
        "--noconsole",
    ]

    PyInstaller.__main__.run(command)
    print(working_dir / "dist" / "agent")
    shutil.copytree(
        working_dir / "dist" / "agent",
        install_path / "agent",
        dirs_exist_ok=True,
    )


if __name__ == "__main__":
    install_deps()
    install_resource()
    install_chores()
    install_agent()

    print(f"Install to {install_path} successfully.")
