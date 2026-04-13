# ============================================================
# GLPI Library Setup via REST API
# Ejecutar después de instalar GLPI y habilitar la API
# ============================================================

$BASE_URL = "http://localhost:8080/apirest.php"
$APP_TOKEN = ""       # Llenar después de crear en GLPI > Setup > General > API
$USER_TOKEN = ""      # Llenar después de generar en perfil de usuario glpi

# ---- 1. Obtener session token ----
function Get-SessionToken {
    $headers = @{
        "App-Token"  = $APP_TOKEN
        "Content-Type" = "application/json"
    }
    $auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("glpi:glpi"))
    $headers["Authorization"] = "Basic $auth"

    $resp = Invoke-RestMethod -Uri "$BASE_URL/initSession" -Method GET -Headers $headers
    return $resp.session_token
}

# ---- 2. Crear un tipo de activo personalizado "Libro" ----
function Create-BookType {
    param($SessionToken)
    $headers = @{
        "App-Token"    = $APP_TOKEN
        "Session-Token"= $SessionToken
        "Content-Type" = "application/json"
    }
    # En GLPI, los tipos de computadora sirven como tipos de activo genéricos
    $body = @{
        input = @{
            name    = "Libro"
            comment = "Tipo de activo para libros de biblioteca"
        }
    } | ConvertTo-Json -Depth 3

    Invoke-RestMethod -Uri "$BASE_URL/ComputerType" -Method POST -Headers $headers -Body $body
    Write-Host "Tipo 'Libro' creado."
}

# ---- 3. Registrar libros (como activos tipo Computer) ----
$libros = @(
    @{ name="Cien años de soledad"; serial="ISBN-9780307474728"; otherserial="García Márquez, Gabriel"; comment="Editorial Sudamericana | 1967 | Literatura" },
    @{ name="El señor de los anillos"; serial="ISBN-9780618640157"; otherserial="Tolkien, J.R.R."; comment="Minotauro | 1954 | Literatura" },
    @{ name="Breve historia del tiempo"; serial="ISBN-9780553380163"; otherserial="Hawking, Stephen"; comment="Crítica | 1988 | Ciencias" },
    @{ name="El gen egoísta"; serial="ISBN-9780198788607"; otherserial="Dawkins, Richard"; comment="Salvat | 1976 | Ciencias" },
    @{ name="Sapiens: De animales a dioses"; serial="ISBN-9788499926223"; otherserial="Harari, Yuval Noah"; comment="Debate | 2011 | Historia" },
    @{ name="El arte de la guerra"; serial="ISBN-9788441413153"; otherserial="Sun Tzu"; comment="Edaf | Siglo V aC | Historia" },
    @{ name="Clean Code"; serial="ISBN-9780132350884"; otherserial="Martin, Robert C."; comment="Prentice Hall | 2008 | Tecnología" },
    @{ name="The Pragmatic Programmer"; serial="ISBN-9780201616224"; otherserial="Hunt, Andrew"; comment="Addison-Wesley | 1999 | Tecnología" },
    @{ name="El arte"; serial="ISBN-9788449305993"; otherserial="Read, Herbert"; comment="Omega | 1931 | Arte" },
    @{ name="Fundamentos de programación"; serial="ISBN-9786073238403"; otherserial="Joyanes, Luis"; comment="McGraw-Hill | 2008 | Tecnología" },
    @{ name="Historia del Perú"; serial="ISBN-9789972217234"; otherserial="Basadre, Jorge"; comment="El Comercio | 2005 | Historia" },
    @{ name="Química general"; serial="ISBN-9786071505088"; otherserial="Chang, Raymond"; comment="McGraw-Hill | 2010 | Ciencias" }
)

function Create-Books {
    param($SessionToken)
    $headers = @{
        "App-Token"    = $APP_TOKEN
        "Session-Token"= $SessionToken
        "Content-Type" = "application/json"
    }
    foreach ($libro in $libros) {
        $body = @{ input = $libro } | ConvertTo-Json -Depth 3
        try {
            Invoke-RestMethod -Uri "$BASE_URL/Computer" -Method POST -Headers $headers -Body $body | Out-Null
            Write-Host "Libro creado: $($libro.name)"
        } catch {
            Write-Warning "Error creando '$($libro.name)': $_"
        }
    }
}

# ---- 4. Crear usuarios lectores ----
$usuarios = @(
    @{ name="lector01"; realname="Flores"; firstname="María"; password="Lector2024!"; email="maria.flores@biblioteca.pe" },
    @{ name="lector02"; realname="Torres"; firstname="Carlos"; password="Lector2024!"; email="carlos.torres@biblioteca.pe" },
    @{ name="lector03"; realname="Quispe"; firstname="Rosa"; password="Lector2024!"; email="rosa.quispe@biblioteca.pe" },
    @{ name="lector04"; realname="Mendoza"; firstname="Juan"; password="Lector2024!"; email="juan.mendoza@biblioteca.pe" },
    @{ name="lector05"; realname="Vargas"; firstname="Elena"; password="Lector2024!"; email="elena.vargas@biblioteca.pe" },
    @{ name="biblio01"; realname="Pérez"; firstname="Daniel"; password="Biblio2024!"; email="daniel.perez@biblioteca.pe" },
    @{ name="biblio02"; realname="Sarmiento"; firstname="Luis"; password="Biblio2024!"; email="luis.sarmiento@biblioteca.pe" }
)

function Create-Users {
    param($SessionToken)
    $headers = @{
        "App-Token"    = $APP_TOKEN
        "Session-Token"= $SessionToken
        "Content-Type" = "application/json"
    }
    foreach ($user in $usuarios) {
        $body = @{ input = $user } | ConvertTo-Json -Depth 3
        try {
            Invoke-RestMethod -Uri "$BASE_URL/User" -Method POST -Headers $headers -Body $body | Out-Null
            Write-Host "Usuario creado: $($user.name)"
        } catch {
            Write-Warning "Error creando usuario '$($user.name)': $_"
        }
    }
}

# ---- MAIN ----
Write-Host "=== Setup GLPI Biblioteca ===" -ForegroundColor Cyan
Write-Host "IMPORTANTE: Configura APP_TOKEN y USER_TOKEN antes de ejecutar." -ForegroundColor Yellow
Write-Host ""
Write-Host "Pasos previos en GLPI:"
Write-Host "  1. Setup > General > API > Habilitar REST API"
Write-Host "  2. Crear App Token en la misma pantalla"
Write-Host "  3. Perfil de usuario > API tokens > Generar"
Write-Host ""

if ($APP_TOKEN -eq "") {
    Write-Warning "APP_TOKEN vacío. Edita este script antes de ejecutar."
    exit 1
}

$session = Get-SessionToken
Write-Host "Session token obtenido." -ForegroundColor Green

Create-BookType $session
Create-Books $session
Create-Users $session

Write-Host ""
Write-Host "Setup completado." -ForegroundColor Green
