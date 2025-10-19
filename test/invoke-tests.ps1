# Create a user
$body = @{ first_name = "Grace"; last_name = "Hopper" } | ConvertTo-Json
$created = Invoke-RestMethod -Method Post -Uri http://localhost:8088/user -Body $body -ContentType "application/json"
Write-Host "Created user:"
$created | ConvertTo-Json

# Fetch by id
$id = $created.id
$got = Invoke-RestMethod -Method Get -Uri ("http://localhost:8088/user/{0}" -f $id)
Write-Host "Fetched user:"
$got | ConvertTo-Json
