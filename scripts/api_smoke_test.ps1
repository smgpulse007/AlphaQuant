Param(
  [string]$BaseUrl = "http://localhost:8000"
)

$ErrorActionPreference='Stop'
Write-Host "Checking $BaseUrl/health..."
$health = Invoke-RestMethod -Uri "$BaseUrl/health" -TimeoutSec 10
if($health.status -ne 'ok'){ throw "Health check failed: $($health | ConvertTo-Json)" }

Write-Host "Calling $BaseUrl/run..."
$body = @{ mode='B'; budget=5000; risk='High'; horizon_months=@(3,12); current_positions=@(); preferences=@{ avoid=@(); focus=@('AI infra','semis') } } | ConvertTo-Json -Depth 5
$resp = Invoke-RestMethod -Method Post -Uri "$BaseUrl/run" -Body $body -ContentType 'application/json'

$pass = $true
$notes = @()
if(-not $resp.meta.started_at){ $pass=$false; $notes+='missing meta.started_at' }
if(-not $resp.audit.double_source){ $pass=$false; $notes+='double_source false' }
if(-not $resp.trades -or $resp.trades.Count -lt 1){ $pass=$false; $notes+='no trades' }
if(-not $resp.market_scan.macro -or -not $resp.market_scan.macro.citations -or $resp.market_scan.macro.citations.Count -lt 2){ $pass=$false; $notes+='macro not double-sourced' }

[pscustomobject]@{
  PASS = $pass
  Regime = $resp.regime.tag
  Trades = $resp.trades.Count
  DoubleSource = $resp.audit.double_source
  Notes = ($notes -join '; ')
} | Format-List

