param(
 [string]$Project=(Join-Path $PSScriptRoot '../Week10Assessment.uproject'),
 [string]$Map='/Game/OptimizationLab/Lounge_Unoptimized',
 [Parameter(Mandatory)][string]$OutputDirectory,
 [int]$Runs=3,[int]$Width=1280,[int]$Height=720,
 [string]$Engine='C:/Program Files/Epic Games/UE_5.7'
)
$ErrorActionPreference='Stop'
if($Runs -lt 1 -or $Runs -gt 10){throw 'Runs must be 1 through 10'}
if($Map -notmatch '^/Game/[A-Za-z0-9_/]+$'){throw 'Use an Unreal /Game/ map path'}
$projectPath=(Resolve-Path -LiteralPath $Project).Path
if(Test-Path -LiteralPath $OutputDirectory){throw 'Choose a fresh output directory'}
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
$out=(Resolve-Path -LiteralPath $OutputDirectory).Path
$exe=Join-Path $Engine 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe'
$csvRoot=Join-Path (Split-Path -Parent $projectPath) 'Saved/Profiling/CSV'
$manifest=[ordered]@{project=(Split-Path -Leaf $projectPath);map=$Map;width=$Width;height=$Height;screen_percentage=100;frames=900;analysis_start=300;analysis_stop_exclusive=850;runs=$Runs;engine=$Engine;capture_kind='Standalone editor runtime; steady timing without screenshots';files=@()}
for($i=1;$i -le $Runs;$i++){
 $before=@(Get-ChildItem -LiteralPath $csvRoot -Filter '*.csv' -ErrorAction SilentlyContinue | ForEach-Object FullName)
 $log=Join-Path $out "run-$i.log"
 $arguments=@(('"{0}"' -f $projectPath),$Map,'-game','-windowed',"-ResX=$Width","-ResY=$Height",'-ForceRes','-unattended','-nop4','-nosplash','-NoVSync','-ExitAfterCsvProfiling',('"-abslog={0}"' -f $log),'"-ExecCmds=t.MaxFPS 0,r.VSync 0,r.ScreenPercentage 100,CSVProfile FRAMES=900"')
 $proc=Start-Process -FilePath $exe -WindowStyle Hidden -PassThru -ArgumentList $arguments
 $null=$proc.Handle
 if(!$proc.WaitForExit(120000)){Stop-Process -Id $proc.Id;throw 'Capture timed out; inspect log'}
 if($proc.ExitCode -ne 0){throw "Run $i failed"}
 $new=@(Get-ChildItem -LiteralPath $csvRoot -Filter '*.csv' | Where-Object FullName -NotIn $before)
 if($new.Count -ne 1){throw 'Expected exactly one new CSV'}
 $name="run-$i.csv";Copy-Item -LiteralPath $new[0].FullName -Destination (Join-Path $out $name)
 $manifest.files+=@{csv=$name;sha256=(Get-FileHash -LiteralPath (Join-Path $out $name) -Algorithm SHA256).Hash}
 $manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $out 'conditions.json') -Encoding utf8
 Write-Output "Completed $Map run $i/$Runs"
}
