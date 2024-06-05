param(
    [Parameter(Mandatory = $true)]
    [string]$action
)

$exeLocation = "./dist/InkLink.exe"
    
    
switch ($action) {
    'remove' {
        Start-Process -FilePath $exeLocation -ArgumentList "stop" -Wait -NoNewWindow
    }
    'install' {
        Start-Process -FilePath $exeLocation -ArgumentList "install" -Wait -NoNewWindow
    }
    'remove' {
        Start-Process -FilePath $exeLocation -ArgumentList "remove" -Wait -NoNewWindow
    }
    'start' {
        Start-Process -FilePath $exeLocation -ArgumentList "start" -Wait -NoNewWindow
    }
    Default {
        Write-Host "Invalid action"
    }
}