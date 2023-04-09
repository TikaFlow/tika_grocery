# ����Windows.Forms����
Add-Type -AssemblyName System.Windows.Forms
# ����PresentationFramework����
Add-Type -AssemblyName PresentationFramework

# ����NotifyIcon����
$notifyIcon = New-Object System.Windows.Forms.NotifyIcon
# ����ͼ���ļ���·��
$iconFilePath = "clock.ico"
# ��ָ���ļ�����ȡͼ�꣬����������Ϊ����ͼ��
$notifyIcon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($iconFilePath)
# ��������ͼ��ɼ�
$notifyIcon.Visible = $true
# Ĭ�Ͽ��϶�
$isDrag = $true
# ��������ͼ�����ʾ�ı�
$notifyIcon.Text = "˫���˳�����ǰ���϶���" + $isDrag
# ��תbool�ĺ���������������
function reverse([ref]$arg) {
    # ��ת
    $arg.Value = -not $arg.Value
}
# ����л�
$notifyIcon.add_MouseClick({
    reverse ([ref]$isDrag)
    $notifyIcon.Text = "˫���˳�����ǰ���϶���" + $isDrag + $form.Left
})
# ˫������ͼ��ʱ��ֹ�ű�
$notifyIcon.add_MouseDoubleClick({
    $form.Close()
})

# ������ǩ����������ʾʱ��
$label = New-Object System.Windows.Controls.Label
$label.Foreground = "White" # ������ɫΪ��ɫ
$label.FontFamily = "΢���ź�" # ����Ϊ΢���ź�
$label.FontWeight = "Normal" # �����ϸΪ����
$label.FontSize = 24 # �����СΪ24
$label.HorizontalAlignment = "Left" # ˮƽ���뷽ʽΪ�����
$label.VerticalAlignment = "Center" # ��ֱ���뷽ʽΪ���ж���
$label.Margin = New-Object System.Windows.Thickness(0) # ��ǩ��߾�Ϊ0
$label.Padding = New-Object System.Windows.Thickness(0) # ��ǩ�ڱ߾�Ϊ0
# Ϊ��ǩ���һ��0.2͸���ȵĺ�ɫ����
$label.Background = New-Object System.Windows.Media.SolidColorBrush((New-Object System.Windows.Media.ColorConverter).ConvertFromString("#33000000"))

# ������ʱ���������ڶ�ʱ����ʱ��
$timer = New-Object System.Windows.Threading.DispatcherTimer
# ���ö�ʱ��ʱ����Ϊ1��
$timer.Interval = [TimeSpan]::FromMilliseconds(200)
# ��Ӷ�ʱ��Tick�¼�������򣬸��±�ǩ����
$timer.add_Tick({
    # ��ȡ��ǰʱ�䣬��ʽ��Ϊ"HH:mm:ss"���ַ���
    $time = Get-Date -Format "HH:mm:ss"
    # ���±�ǩ����
    $label.Content = $time
    # �Զ�����
    $form.Top = 0
})

# �������ڶ���������ʾʱ���ǩ
$form = New-Object System.Windows.Window
$form.AllowsTransparency = $true # ����͸����
$form.Background = "Transparent" # ����͸��
$form.BorderThickness = 0 # �߿���Ϊ0
$form.WindowStyle = "None" # �ޱ߿򴰿�
$form.ResizeMode = "NoResize" # ��ֹ���ڴ�С����
$form.Topmost = $true # �ö�
$form.Width = 100 # ���ڿ��Ϊ100
$form.Height = 30 # ���ڸ߶�Ϊ30
# ���ڵ���Ļ�Ҳ�ľ����ʼΪ512
$form.Left = [System.Windows.SystemParameters]::PrimaryScreenWidth - 512
# ���ڵ���Ļ�����ľ���Ϊ0
$form.Top = 0
# ������������ʾ
$form.ShowInTaskbar = $false
# ����϶�����
$form.add_MouseLeftButtonDown({
    if ($isDrag){
        $form.DragMove()
    }
})
# ����ǩ��ӵ�������
$form.Content = $label

# ���Closed�¼�����������ڹرմ���ʱֹͣ��ʱ�����ͷ���Դ
$form.add_Closed({
    # ֹͣ��ʱ��
    $timer.Stop()
    $timer = $null
    # ɾ������ͼ��
    $notifyIcon.Visible = $false
    $notifyIcon.Dispose()
    # �ͷ���Դ
    $label = $null
    $form = $null
})

# ������ʱ������ʾ����
$timer.Start()
$form.ShowDialog() | Out-Null
