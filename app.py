import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, 
    RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import SolidFillColorMask
from io import BytesIO
from PIL import Image

# Konfiguracja strony

_about = """
[Przemysław Zawadzki](https://www.linkedin.com/in/przemyslawzawadzki/)

**DataBase Analyst**

"""
st.set_page_config(page_title="Generator QR Code", page_icon="OK", menu_items={'About': _about} )


st.title("Generator Kodów QR")
st.markdown("""
#### Witaj w prostym kodów QR! 
Wprowadź tekst, wybierz kolory oraz styl, a następnie pobierz gotowy obraz.

- żadnego dodawania śledzenia
- żadnego terminu ważności
- żadnego przechowywania danych
- żadnego przekierowania
            
#### Tylko to co wpiszesz i wygenerowany kod QR, który jest twój do użytokowania bez ograniczeń!
""")

# Mapowanie poziomów korekcji błędów
ERROR_CORRECTION_MAP = {
    "Niska (7%)": qrcode.constants.ERROR_CORRECT_L,
    "Średnia (15%)": qrcode.constants.ERROR_CORRECT_M,
    "Wysoka (25%)": qrcode.constants.ERROR_CORRECT_Q,
    "Bardzo Wysoka (30%)": qrcode.constants.ERROR_CORRECT_H
}

# Mapowanie stylów modułów
MODULE_DRAWERS = {
    "Kwadratowy": SquareModuleDrawer(),
    "Kwadratowy z przerwami": GappedSquareModuleDrawer(),
    "Kołowy": CircleModuleDrawer(),
    "Zaokrąglony": RoundedModuleDrawer(),
    "Pionowe paski": VerticalBarsDrawer(),
    "Poziome paski": HorizontalBarsDrawer()
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# # Sidebar z ustawieniami
# st.sidebar.header("Ustawienia")

data = st.text_input("Wprowadź tekst lub URL", "https://google.com")

col1, col2 = st.columns(2)
with col1:
    fill_color_hex = st.color_picker("Kolor wypełnienia", "#000000")
with col2:
    back_color_hex = st.color_picker("Kolor tła", "#FFFFFF")

error_level_label = st.select_slider(
    "Poziom korekcji błędów",
    options=list(ERROR_CORRECTION_MAP.keys()),
    value="Średnia (15%)",
    help="Wyższy poziom pozwala na odczytanie kodu nawet po jego uszkodzeniu lub zakryciu części (np. logiem)."
)

module_style_label = st.selectbox(
    "Styl modułów (punktów)",
    options=list(MODULE_DRAWERS.keys())
)

# Generowanie kodu QR
if data:
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=ERROR_CORRECTION_MAP[error_level_label],
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Konwersja kolorów
        fill_rgb = hex_to_rgb(fill_color_hex)
        back_rgb = hex_to_rgb(back_color_hex)

        # Tworzenie obrazu z wybranym stylem
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=MODULE_DRAWERS[module_style_label],
            color_mask=SolidFillColorMask(back_color=back_rgb, front_color=fill_rgb)
        )

        # Wyświetlanie podglądu
        st.subheader("Podgląd")
        
        # Konwersja do formatu obsługiwanego przez Streamlit (BytesIO)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        
        st.image(buffered)

        # Przycisk pobierania
        st.download_button(
            label="Pobierz Kod QR (PNG)",
            data=buffered.getvalue(),
            file_name="qrcode.png",
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"Wystąpił błąd podczas generowania kodu: {e}")
else:
    st.warning("Wprowadź tekst, aby wygenerować kod QR.")


