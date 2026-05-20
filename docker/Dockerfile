# Multi-stage Dockerfile for MELISA
FROM mcr.microsoft.com/powershell:7.4-windowsservercore AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY . .
RUN dotnet restore

FROM base AS final
WORKDIR /app
COPY --from=build /src .
CMD ["pwsh", "MELISA-Main.ps1"]
