# Specify the path to your .env file
$envFilePath = ".env"

# Check if the .env file exists
if (Test-Path $envFilePath -PathType Leaf) {
    # Read the content of the .env file
    $envFileContent = Get-Content -Path $envFilePath

    # Iterate over each line in the file
    $envFileContent | ForEach-Object {
        # Split each line into key and value using the '=' delimiter
        $parts = $_.Split('=')
        if ($parts.Count -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            
            # Set the environment variable
            [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::Process)
            
            Write-Host "Set $key=$value"
        }
    }
} else {
    Write-Host "The .env file does not exist."
}
