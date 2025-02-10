param (
    [string]$appName,
    [string]$appPath
)

$registryPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
Set-ItemProperty -Path $registryPath -Name $appName -Value $appPath
Write-Output "$appName has been added to startup"
