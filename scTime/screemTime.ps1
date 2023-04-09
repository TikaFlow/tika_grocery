# 加载Windows.Forms程序集
Add-Type -AssemblyName System.Windows.Forms
# 加载PresentationFramework程序集
Add-Type -AssemblyName PresentationFramework

# 创建NotifyIcon对象
$notifyIcon = New-Object System.Windows.Forms.NotifyIcon
# 设置图标文件的路径
$iconFilePath = "clock.ico"
# 从指定文件中提取图标，并将其设置为托盘图标
$notifyIcon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($iconFilePath)
# 设置托盘图标可见
$notifyIcon.Visible = $true
# 默认可拖动
$isDrag = $true
# 设置托盘图标的提示文本
$notifyIcon.Text = "双击退出，当前可拖动：" + $isDrag
# 翻转bool的函数，必须用引用
function reverse([ref]$arg) {
    # 翻转
    $arg.Value = -not $arg.Value
}
# 点击切换
$notifyIcon.add_MouseClick({
    reverse ([ref]$isDrag)
    $notifyIcon.Text = "双击退出，当前可拖动：" + $isDrag + $form.Left
})
# 双击托盘图标时终止脚本
$notifyIcon.add_MouseDoubleClick({
    $form.Close()
})

# 创建标签对象，用于显示时间
$label = New-Object System.Windows.Controls.Label
$label.Foreground = "White" # 字体颜色为白色
$label.FontFamily = "微软雅黑" # 字体为微软雅黑
$label.FontWeight = "Normal" # 字体粗细为正常
$label.FontSize = 24 # 字体大小为24
$label.HorizontalAlignment = "Left" # 水平对齐方式为左对齐
$label.VerticalAlignment = "Center" # 垂直对齐方式为居中对齐
$label.Margin = New-Object System.Windows.Thickness(0) # 标签外边距为0
$label.Padding = New-Object System.Windows.Thickness(0) # 标签内边距为0
# 为标签添加一个0.2透明度的黑色背景
$label.Background = New-Object System.Windows.Media.SolidColorBrush((New-Object System.Windows.Media.ColorConverter).ConvertFromString("#33000000"))

# 创建定时器对象，用于定时更新时间
$timer = New-Object System.Windows.Threading.DispatcherTimer
# 设置定时器时间间隔为1秒
$timer.Interval = [TimeSpan]::FromMilliseconds(200)
# 添加定时器Tick事件处理程序，更新标签内容
$timer.add_Tick({
    # 获取当前时间，格式化为"HH:mm:ss"的字符串
    $time = Get-Date -Format "HH:mm:ss"
    # 更新标签内容
    $label.Content = $time
    # 自动贴边
    $form.Top = 0
})

# 创建窗口对象，用于显示时间标签
$form = New-Object System.Windows.Window
$form.AllowsTransparency = $true # 允许透明度
$form.Background = "Transparent" # 背景透明
$form.BorderThickness = 0 # 边框厚度为0
$form.WindowStyle = "None" # 无边框窗口
$form.ResizeMode = "NoResize" # 禁止窗口大小调整
$form.Topmost = $true # 置顶
$form.Width = 100 # 窗口宽度为100
$form.Height = 30 # 窗口高度为30
# 窗口到屏幕右侧的距离初始为512
$form.Left = [System.Windows.SystemParameters]::PrimaryScreenWidth - 512
# 窗口到屏幕顶部的距离为0
$form.Top = 0
# 不在任务栏显示
$form.ShowInTaskbar = $false
# 添加拖动功能
$form.add_MouseLeftButtonDown({
    if ($isDrag){
        $form.DragMove()
    }
})
# 将标签添加到窗口中
$form.Content = $label

# 添加Closed事件处理程序，用于关闭窗口时停止定时器并释放资源
$form.add_Closed({
    # 停止定时器
    $timer.Stop()
    $timer = $null
    # 删除托盘图标
    $notifyIcon.Visible = $false
    $notifyIcon.Dispose()
    # 释放资源
    $label = $null
    $form = $null
})

# 启动定时器并显示窗口
$timer.Start()
$form.ShowDialog() | Out-Null
