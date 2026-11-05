param(
    [ValidateSet('Visual','Timing')][string]$Kind,
    [Parameter(Mandatory)][string]$OutputDirectory,
    [string]$Engine = 'C:/Program Files/Epic Games/UE_5.7'
)
$ErrorActionPreference = 'Stop'
$project = (Resolve-Path (Join-Path $PSScriptRoot '../MaterialCostLab.uproject')).Path
$projectRoot = Split-Path -Parent $project
$exe = Join-Path $Engine 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe'
$null = New-Item -ItemType Directory $OutputDirectory
$out = (Resolve-Path $OutputDirectory).Path
$csvDir = Join-Path $projectRoot 'Saved/Profiling/CSV'
$shotDir = Join-Path $projectRoot 'Saved/Screenshots'
$jobs = if ($Kind -eq 'Timing') {
    foreach ($modes in @('CPD,MID,Lean,MasterOff,MasterOn','MasterOn,MasterOff,Lean,MID,CPD','Lean,CPD,MasterOn,MID,MasterOff')) {
        foreach ($mode in $modes.Split(',')) { @{ Mode = $mode; View = 'Front' } }
    }
} else {
    foreach ($mode in 'CPD','MID','Lean','MasterOff','MasterOn') { @{ Mode = $mode; View = 'Front' } }
}
$i = 0
foreach ($job in $jobs) {
    $i++
    $name = '{0:D2}-{1}-{2}' -f $i,$job.Mode,$job.View
    $oldCsv = @(Get-ChildItem $csvDir -Filter '*.csv' -ErrorAction SilentlyContinue | ForEach-Object FullName)
    $oldShots = @(Get-ChildItem $shotDir -Recurse -Filter '*.png' -ErrorAction SilentlyContinue | ForEach-Object FullName)
    $args = @(
        ('"{0}"' -f $project), '-game', '-windowed','-ForceRes','-unattended','-nop4','-nosplash','-stdout',
        '-NoVSync','-ExitAfterCsvProfiling', "-MaterialMode=$($job.Mode)"
    )
    if ($Kind -eq 'Timing') {
        $args += '-ResX=2560','-ResY=1440','"-ExecCmds=t.MaxFPS 0,r.VSync 0,r.ScreenPercentage 100,CSVProfile FRAMES=600"'
    } else {
        $args += '-ResX=2560','-ResY=1440','"-ExecCmds=t.MaxFPS 0,r.VSync 0,r.ScreenPercentage 100,CSVProfile FRAMES=120"','"-csvExecCmds=90:HighResShot 1"'
    }
    $log = Join-Path $out "$name.log"
    $proc = Start-Process -FilePath $exe -WindowStyle Hidden -PassThru -ArgumentList $args -RedirectStandardOutput $log -RedirectStandardError (Join-Path $out "$name.stderr.log")
    $null = $proc.Handle
    if (!$proc.WaitForExit(120000)) {
        & taskkill.exe /PID $proc.Id /T /F | Out-Null
        throw "$name timed out"
    }
    if ($proc.ExitCode -ne 0 -or !(Select-String -LiteralPath $log -Pattern 'MATERIAL_LAB_READY' -Quiet)) {
        throw "$name failed. Inspect $log"
    }
    $newCsv = @(Get-ChildItem $csvDir -Filter '*.csv' | Where-Object FullName -NotIn $oldCsv)
    if ($newCsv.Count -ne 1) { throw "$name produced $($newCsv.Count) new CSV captures" }
    Copy-Item -LiteralPath $newCsv[0].FullName -Destination (Join-Path $out "$name.csv")
    if ($Kind -eq 'Visual') {
        $newShot = @(Get-ChildItem $shotDir -Recurse -Filter '*.png' | Where-Object FullName -NotIn $oldShots)
        if ($newShot.Count -ne 1) { throw "$name produced $($newShot.Count) new screenshots" }
        Copy-Item -LiteralPath $newShot[0].FullName -Destination (Join-Path $out "$name.png")
    }
    Write-Output "Captured $name"
}
