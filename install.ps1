# 约会军师 · LocalDate 一键安装（Windows）
# 用法：irm https://raw.githubusercontent.com/1648714300/localdate/main/install.ps1 | iex
$ErrorActionPreference = "Stop"

$Repo    = "https://github.com/1648714300/localdate.git"
$Skills  = if ($env:WORKBUDDY_SKILLS) { $env:WORKBUDDY_SKILLS } else { Join-Path $env:USERPROFILE ".workbuddy\skills" }
$Target  = Join-Path $Skills "localdate"
$Alias   = Join-Path $Skills "date"

Write-Host "== 约会军师 · LocalDate ==" -ForegroundColor Cyan

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "需要先装 git: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Force -Path $Skills | Out-Null

if (Test-Path (Join-Path $Target ".git")) {
    Write-Host "已装过，拉取更新: $Target"
    git -C $Target pull --ff-only
} else {
    Write-Host "克隆到: $Target"
    git clone --depth 1 $Repo $Target
}

# 短名 date：用目录联接指向同一份技能，以后只说 /date
if (Test-Path $Alias) { Remove-Item $Alias -Force -Recurse -ErrorAction SilentlyContinue }
cmd /c mklink /J "$Alias" "$Target" | Out-Null

Write-Host ""
Write-Host "装好了。下一步，直接对你的 AI 说:" -ForegroundColor Green
Write-Host "  /date 排这个周末的约会   (或)   约会军师，淮南，周六下午，预算 100"
Write-Host ""
Write-Host "它会先问四件事: 城市包 / 白天还是晚上 / 对方体力与禁忌 / 预算。"
Write-Host "之后每轮 15 个方案，你报编号排序，它把你的口味写进权重。"
