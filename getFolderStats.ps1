$rootDir = "\\your\folder\directory"

function Get-FolderStats {
    param (
        [string]$folderPath
    )

    $files = Get-ChildItem -Path $folderPath -Recurse -File

    $fileCount = $files.Count

    $totalSize = ($files | Measure-Object -Property Length -Sum).Sum

    $totalSizeMB = [math]::Round($totalSize / 1GB, 5)

    [PSCustomObject]@{
        FolderPath = $folderPath
        FileCount = $fileCount
        TotalSizeMB = $totalSizeMB
    }
}

$directories = Get-ChildItem -Path $rootDir -Directory

foreach ($dir in $directories) {
    Get-FolderStats -folderPath $dir.FullName
}
