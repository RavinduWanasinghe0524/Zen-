# Zen Voice Assistant - Auto-Start Setup Script
# This PowerShell script configures Windows Task Scheduler to auto-start Zen Assistant

param(
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"

# Configuration
$TaskName = "ZenVoiceAssistant"
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$BatchFile = Join-Path $ScriptPath "start_zen.bat"
$Description = "Automatically starts Zen Voice Assistant on Windows login"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Zen Voice Assistant - Auto-Start Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠ WARNING: Not running as Administrator" -ForegroundColor Yellow
    Write-Host "Some features may not work correctly." -ForegroundColor Yellow
    Write-Host "Consider running PowerShell as Administrator for best results." -ForegroundColor Yellow
    Write-Host ""
}

# Uninstall mode
if ($Uninstall) {
    Write-Host "Removing auto-start configuration..." -ForegroundColor Yellow
    
    try {
        $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        
        if ($task) {
            Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
            Write-Host "✓ Auto-start task removed successfully!" -ForegroundColor Green
        } else {
            Write-Host "ℹ Auto-start task not found. Nothing to remove." -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "✗ Failed to remove auto-start task: $_" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "Zen Assistant will no longer start automatically on login." -ForegroundColor Green
    exit 0
}

# Install mode
Write-Host "Setting up auto-start for Zen Voice Assistant..." -ForegroundColor White
Write-Host ""

# Verify batch file exists
if (-not (Test-Path $BatchFile)) {
    Write-Host "✗ ERROR: start_zen.bat not found at:" -ForegroundColor Red
    Write-Host "  $BatchFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure you're running this script from the Zen Assistant directory." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Found startup script: $BatchFile" -ForegroundColor Green

try {
    # Check if task already exists
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    
    if ($existingTask) {
        Write-Host "ℹ Task already exists. Removing old task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }
    
    # Create scheduled task action
    $action = New-ScheduledTaskAction -Execute $BatchFile -WorkingDirectory $ScriptPath
    
    # Create trigger (at logon with 10 second delay)
    $trigger = New-ScheduledTaskTrigger -AtLogOn
    $trigger.Delay = "PT10S"  # 10 second delay after logon
    
    # Create settings
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable:$false `
        -DontStopOnIdleEnd
    
    # Get current user
    $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
    
    # Register the task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Description $Description `
        -Force | Out-Null
    
    Write-Host "✓ Auto-start task created successfully!" -ForegroundColor Green
    Write-Host ""
    
    # Display task information
    Write-Host "Task Configuration:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName" -ForegroundColor White
    Write-Host "  Trigger: At logon (10 second delay)" -ForegroundColor White
    Write-Host "  Action: Start Zen Assistant" -ForegroundColor White
    Write-Host "  User: $env:USERNAME" -ForegroundColor White
    Write-Host ""
    
    Write-Host "✓ Setup complete! Zen Assistant will now start automatically when you log in." -ForegroundColor Green
    Write-Host ""
    Write-Host "To test: Log out and log back in, or run this command:" -ForegroundColor Yellow
    Write-Host "  Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To remove auto-start, run:" -ForegroundColor Yellow
    Write-Host "  .\setup_autostart.ps1 -Uninstall" -ForegroundColor Cyan
}
catch {
    Write-Host ""
    Write-Host "✗ Failed to create scheduled task: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Try running PowerShell as Administrator" -ForegroundColor White
    Write-Host "  2. Check Task Scheduler permissions" -ForegroundColor White
    Write-Host "  3. Verify Windows Task Scheduler service is running" -ForegroundColor White
    exit 1
}

Write-Host "================================================" -ForegroundColor Cyan
