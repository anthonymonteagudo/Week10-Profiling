param(
 [string]$Engine='C:/Program Files/Epic Games/UE_5.7',
 [string]$FabProject
)
$ErrorActionPreference='Stop'
$projectRoot=$PSScriptRoot
$project=Join-Path $projectRoot 'Week10Assessment.uproject'
$destination=Join-Path $projectRoot 'Content/Cigar_room'
if($FabProject){
 $source=Join-Path (Split-Path -Parent (Resolve-Path -LiteralPath $FabProject).Path) 'Content/Cigar_room'
 if(!(Test-Path -LiteralPath (Join-Path $source 'Maps/Cigar_room.umap'))){throw 'Fab project must contain Content/Cigar_room/Maps/Cigar_room.umap'}
 if(Test-Path -LiteralPath $destination){throw 'Cigar_room already exists here; existing content was preserved. Omit FabProject to use it.'}
 New-Item -ItemType Directory -Force (Join-Path $projectRoot 'Content') | Out-Null
 Copy-Item -LiteralPath $source -Destination $destination -Recurse
}
if(!(Test-Path -LiteralPath (Join-Path $destination 'Maps/Cigar_room.umap'))){throw 'Add the free Cigar Room Environment Fab pack to this project first, or pass -FabProject with an existing project containing it.'}
$exe=Join-Path $Engine 'Engine/Binaries/Win64/UnrealEditor-Cmd.exe'
if(!(Test-Path -LiteralPath $exe)){throw 'Unreal Engine 5.7 is required; provide -Engine if installed elsewhere.'}
foreach($map in 'Lounge_Reference','Lounge_Unoptimized'){
 if(Test-Path -LiteralPath (Join-Path $projectRoot "Content/OptimizationLab/$map.umap")){throw 'Lab already exists. Open the project; to rebuild use a fresh starter copy. Existing edits were preserved.'}
}
New-Item -ItemType Directory -Force (Join-Path $projectRoot 'Saved') | Out-Null
$build=Join-Path $projectRoot 'Tools/build_lab.py'
$validate=Join-Path $projectRoot 'Tools/validate_lab.py'
& $exe $project -run=pythonscript "-script=$build" -NullRHI -unattended -nosplash
if($LASTEXITCODE -ne 0){throw 'Lab generation failed. Inspect Saved/Logs; use a fresh starter before rebuilding partial output.'}
& $exe $project -run=pythonscript "-script=$validate" -NullRHI -unattended -nosplash
if($LASTEXITCODE -ne 0){throw 'Lab validation failed; inspect Saved/Logs.'}
$config=Join-Path $projectRoot 'Config/DefaultEngine.ini'
$content=[IO.File]::ReadAllText($config).Replace('/Game/Cigar_room/Maps/Cigar_room','/Game/OptimizationLab/Lounge_Unoptimized')
[IO.File]::WriteAllText($config,$content)
Write-Output 'READY: open Week10Assessment.uproject. Main lab: Lounge_Unoptimized. Keep source and reference maps unchanged.'
