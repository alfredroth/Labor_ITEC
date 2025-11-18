# Black-Box auslesen über die Power Shell 30.10.2025 AR
# Port auslesen über die PowerShell - zum testen ob die Black Box funktioniert und Daten liefert

# 1. Findet die COM Port Nr. wo die BlackBox angeschlossen ist

$Geraet = Get-PnpDevice | Where-Object { $_.FriendlyName -match "UART" } # Bezeichnung = "Silicon Labs CP210x USB to UART Bridge
if ($Geraet) {
    if ($Geraet.FriendlyName -match "\(COM\d+\)") {
        $ComPort = $matches[0].Trim('()')
        Write-Host "Black-Box gefunden: $($Geraet.FriendlyName)"
        Write-Host "Angeschlossen an USB COM Port Nr.: "$ComPort[-1]" " # Ausgabe in Terminal der COM Nr. 
    }
}
else {
    Write-Host "Keine Black Box angeschlossen"
}

#2. Parameter Einstellung für die Kommunikation der UART Bridge
$baudRate = 115200          
$k=0    # Variable für while Schleife - fuer Anzahl der Messungen
$m=10   # Variable für Anzahl der Messsungen

#3. Log Datei erstellen.  Hier werden die ausgelesenen Daten mit Zeitstempel gespeichert.
$logFile = "C:\temp\daten_BlackBox.txt"  # Hier Daten speichern (kann auch in .csv speichern - Endung Aendern

#4 Port öffnen
$port = New-Object System.IO.Ports.SerialPort $comPort, $baudRate, 'None', 8, 'One'
$port.ReadTimeout = 777
$port.Open()

#5Log-Datei vorbereiten in C\temp
if (!(Test-Path $logFile)) {
    "Zeitstempel:Datum Uhrzeit, Wert von Black Box" | Out-File -Encoding UTF8 $logFile
}

Write-Host "Daten von $comPort. Druecke STRG+C zum Beenden.`n"  #Ausgabe in PowerShell

#5 (Endlos)schleife zum Lesen der Daten

try {
    while ($k -lt $m) {
        try {
            $line = $port.ReadLine().Trim()
            if ($line -match '^\d+$') {
                $intVal = [int]$line
                $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                Write-Host "$timestamp - Empfangener Wert: : $intVal       ......    STRG+C zum Beenden.`n"
                $k++
                "$timestamp, $intVal" | Out-File -Append -Encoding UTF8 $logFile  
            } else {
                Write-Warning "Ungültige Zeile: '$line'"
            }
        } catch {
            # Timeout oder Lesefehler ignorieren
        }
          
    }
}
finally {
    $port.Close()
    Write-Host "`n Ende. Verbindung zu $comPort geschlossen."
}
