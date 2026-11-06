param([switch]$Uninstall, [hashtable]$Projects, [string]$Editor)
$ErrorActionPreference = 'Stop'
$installDir = Join-Path $env:LOCALAPPDATA 'TechArtUnrealLauncher'
$registryPath = 'HKCU:\Software\Classes\techart-ue'
if ($Uninstall) {
    Remove-Item -LiteralPath $registryPath -Recurse -Force -ErrorAction SilentlyContinue
    # Retain the tiny local configuration for recovery; remove only our registration.
    Write-Host 'Unreal launch links unregistered. Local configuration retained.'
    exit
}
$names = [ordered]@{lounge='Week10Assessment.uproject';materials='MaterialCostLab.uproject';debris='DebrisComparison.uproject';niagara='NiagaraLab.uproject';week9='Week09MaterialLab.uproject'}
$selectedProjects = @{}
if (!$Editor) { $Editor = Join-Path $env:ProgramFiles 'Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe' }
if (!(Test-Path -LiteralPath $Editor -PathType Leaf)) { throw 'Provide -Editor with your UnrealEditor.exe path.' }
foreach ($id in $names.Keys) {
    $entered = if ($Projects) { [string]$Projects[$id] } else { Read-Host "Full path for $id ($($names[$id])), or Enter to skip" }
    $entered = $entered.Trim().Trim('"')
    if (!$entered) { continue }
    $resolved = (Resolve-Path -LiteralPath $entered).Path
    if ([IO.Path]::GetExtension($resolved) -ne '.uproject' -or !(Test-Path -LiteralPath $resolved -PathType Leaf)) { throw 'Choose an existing .uproject file.' }
    $null = Get-Content -LiteralPath $resolved -Raw | ConvertFrom-Json
    $selectedProjects[$id] = $resolved
}
if ($selectedProjects.Count -eq 0) { throw 'No projects selected. Nothing registered.' }
New-Item -ItemType Directory -Path $installDir -Force | Out-Null
@{ projects = $selectedProjects; editor = (Resolve-Path -LiteralPath $Editor).Path } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $installDir 'projects.json') -Encoding UTF8
$handler = @'
param([string]$Uri)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
try {
    if ($Uri -cnotmatch '^techart-ue://(lounge|materials|debris|niagara|week9)/?$') { throw 'Unknown project link.' }
    $id = $Matches[1]
    $config = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'projects.json') -Raw | ConvertFrom-Json
    $project = $config.projects.$id
    if (!$project -or [IO.Path]::GetExtension($project) -ne '.uproject' -or !(Test-Path -LiteralPath $project -PathType Leaf)) { throw 'Project is not configured or has moved. Re-run launcher setup.' }
    # Open only a locally configured project in the configured editor.
    # URI text is never executed, interpolated into a command, or passed as arguments.
    if (!(Test-Path -LiteralPath $config.editor -PathType Leaf)) { throw 'Configured Unreal editor has moved. Re-run setup.' }
    $process = Start-Process -FilePath $config.editor -ArgumentList ('"' + $project + '"') -PassThru
    [pscustomobject]@{ time = (Get-Date).ToString('o'); project_id = $id; project = $project; process_id = $process.Id } | ConvertTo-Json -Compress | Add-Content -LiteralPath (Join-Path $PSScriptRoot 'launch-log.jsonl')
} catch {
    [System.Windows.Forms.MessageBox]::Show($_.Exception.Message,'Technical Art launcher','OK','Error') | Out-Null
}
'@
$handlerPath = Join-Path $installDir 'Open-UnrealProject.ps1'
Set-Content -LiteralPath $handlerPath -Value $handler -Encoding UTF8
New-Item -Path $registryPath -Force | Out-Null
Set-Item -LiteralPath $registryPath -Value 'URL:Technical Art Unreal project'
New-ItemProperty -LiteralPath $registryPath -Name 'URL Protocol' -Value '' -PropertyType String -Force | Out-Null
New-Item -Path "$registryPath\shell\open\command" -Force | Out-Null
$powershell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$command = '"{0}" -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "{1}" "%1"' -f $powershell,$handlerPath
Set-Item -LiteralPath "$registryPath\shell\open\command" -Value $command
Write-Host 'Installed for this Windows user. Return to the walkthrough and click Open project.'
