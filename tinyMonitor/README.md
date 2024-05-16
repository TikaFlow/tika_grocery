English | [简体中文](README_zh-CN.md)

 # TinyMonitor

A simple performance monitoring program.

# Installation

## Method 1

Download the executable file from the [release](https://github.com/TikaFlow/tika_grocery/releases) in the repository.

## Method 2

Run the `.py` script directly in a Python environment.

```powershell
python monitor.py
```

# Usage

- Drag the floating window to any position and it will automatically stick to the edge.
- Right-click the tray icon to open the settings menu, where you can temporarily hide the floating window and set which information to display.
- To prevent accidental touch, you can turn on mouse penetration, when the mouse penetration can not drag the floating window.
- The selected information will be displayed at the end, which can be used to adjust the display order.

# Packaging

## Step 1: Install the packaging tool

```powershell
pip install pyinstaller
```

## Step 2: Package

```powershell
pyinstaller monitor.spec
```
