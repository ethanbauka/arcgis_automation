# set config store root
$configStoreRoot = "\\location\of\configstore\services"
$targetFolder = "yourServiceFolder" # use "" for root folder services

# build base path to folder
$folderPath = if ($targetFolder -eq "") {
    $configRoot
} else {
    Join-Path $configStoreRoot $targetFolder
}

# loop through each service sub dir to get json info
# be sure to change .MapServer or .ImageServer depending on AGS site
Get-ChildItem -Path $folderPath -Directory | Where-Object { $_.Name -like "*.MapServer" } | ForEach-Object {
    $serviceDir = $_.FullName
    $jsonFileName = "$($_.Name).json"
    $jsonPath = Join-Path $serviceDir $jsonFileName
    $jsonContent = Get-Content $jsonPath -Raw | ConvertFrom-Json

    $props = $jsonContent.properties
    $serviceName = $_.BaseName
    $minInst = $jsonContent.minInstancesPerNode
    $maxInst = $jsonContent.maxInstancesPerNode
    $maxUse = $jsonContent.maxUsageTime
    $maxWait = $jsonContent.maxWaitTime
    $maxIdle = $jsonContent.maxIdleTime

    Write-Host "Service: $serviceName"
    Write-Host " Min Instances per machine: $($minInst)"
    Write-Host " Max Instances per machine: $($maxInst)"
    Write-Host " Max time a client can use a service (sec): $($maxUse)"
    Write-Host " Max time a client will wait to get a service (sec): $($maxWait)"
    Write-Host " Max time an idle instance can be kept running (sec): $($maxIdle)"
    Write-Host "----"
}
