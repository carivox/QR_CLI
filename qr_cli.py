import os
import re
from pathlib import Path
import qrcode


def sanitize_filename(url: str) -> str:
    # Entfernung von unerlaubten Zeichen
    clean_url = re.sub(r"^https?://", "", url)
    clean_url = re.sub(r'[\\/*?:"<>|]', "", clean_url)

    if not clean_url:
        clean_url = "qrcode_output"

    return clean_url[:150]


def get_download_path() -> Path:
    home = Path.home()
    return home / "Downloads"


def generate_qr():
    print()
    print("╔══════════════════════════════╗")
    print("║     QR-Code Generator CLI    ║")
    print("║        © Lukas Broda         ║")
    print("╚══════════════════════════════╝")
    print()

    #URL abfragen
    url = input("Bitte füge den Link ein: ").strip()

    if not url:
        print("Fehler: Es wurde kein Link eingegeben.")
        return

    #Dateinamen generieren
    filename = sanitize_filename(url) + ".png"
    download_dir = get_download_path()
    output_path = download_dir / filename

    #QR Code erstellen
    print("\nGeneriere QR-Code...")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    #Speichern als PNG
    img = qr.make_image(fill_color="black", back_color="white")

    try:
        # Ordner erstellen, falls er aus irgendeinem Grund nicht existiert
        download_dir.mkdir(parents=True, exist_ok=True)

        img.save(output_path)
        print(f"Erfolgreich gespeichert unter:\n{output_path}")
    except Exception as e:
        print(f"Fehler beim Speichern der Datei: {e}")


if __name__ == "__main__":
    generate_qr()