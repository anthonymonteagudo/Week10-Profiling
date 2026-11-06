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
$launcherSource = @'
using System;
using System.IO;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.Web.Script.Serialization;
using System.Windows.Forms;
class Launcher {
 [STAThread] static void Main(string[] args) {
  try {
   if(args.Length != 1) throw new Exception("Expected one project link.");
   Match m=Regex.Match(args[0], @"\Atechart-ue://(lounge|materials|debris|niagara|week9)/?\z");
   if(!m.Success) throw new Exception("Unknown project link.");
   string dir=AppDomain.CurrentDomain.BaseDirectory;
   var json=new JavaScriptSerializer();
   var config=json.Deserialize<Dictionary<string,object>>(File.ReadAllText(Path.Combine(dir,"projects.json")));
   var projects=(Dictionary<string,object>)config["projects"];
   string id=m.Groups[1].Value;
   if(!projects.ContainsKey(id)) throw new Exception("Project is not configured. Re-run setup.");
   string project=(string)projects[id], editor=(string)config["editor"];
   if(!File.Exists(project) || !project.EndsWith(".uproject",StringComparison.OrdinalIgnoreCase) || !File.Exists(editor)) throw new Exception("Configured project/editor has moved. Re-run setup.");
   var start=new ProcessStartInfo(editor,"\""+project+"\""); start.UseShellExecute=false;
   var process=Process.Start(start);
   File.AppendAllText(Path.Combine(dir,"launch-log.jsonl"),json.Serialize(new {time=DateTimeOffset.Now.ToString("o"),project_id=id,project=project,process_id=process.Id})+Environment.NewLine);
  } catch(Exception e) { MessageBox.Show(e.Message,"Technical Art launcher",MessageBoxButtons.OK,MessageBoxIcon.Error); }
 }
}
'@
$sourcePath = Join-Path $installDir 'UnrealProjectLauncher.cs'
$launcherPath = Join-Path $installDir 'UnrealProjectLauncher.exe'
Set-Content -LiteralPath $sourcePath -Value $launcherSource -Encoding UTF8
$compiler = Join-Path $env:SystemRoot 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
& $compiler /nologo /target:winexe /reference:System.Web.Extensions.dll /reference:System.Windows.Forms.dll "/out:$launcherPath" $sourcePath
if ($LASTEXITCODE -ne 0) { throw 'Launcher compile failed.' }
New-Item -Path $registryPath -Force | Out-Null
Set-Item -LiteralPath $registryPath -Value 'URL:Technical Art Unreal project'
New-ItemProperty -LiteralPath $registryPath -Name 'URL Protocol' -Value '' -PropertyType String -Force | Out-Null
New-Item -Path "$registryPath\shell\open\command" -Force | Out-Null
$command = '"{0}" "%1"' -f $launcherPath
Set-Item -LiteralPath "$registryPath\shell\open\command" -Value $command
Write-Host 'Installed for this Windows user. Return to the walkthrough and click Open project.'
