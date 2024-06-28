import re


def clean_number(num_str):
    """
    Limpia un string numérico removiendo símbolos de moneda, comas y otros caracteres no numéricos,
    dejando solo dígitos y el punto decimal.

    Args:
        num_str (str): El string que representa el número a limpiar.

    Returns:
        float: El número limpiado convertido a float. Retorna 0.0 si el string no puede ser convertido.
    """
    # Eliminar cualquier carácter que no sea un dígito o un punto decimal
    cleaned = re.sub(r"[^\d\.]", "", num_str)

    # Manejar casos donde el string comienza con un punto decimal
    if cleaned.startswith("."):
        cleaned = "0" + cleaned

    # Convertir el string limpiado a float
    try:
        cleaned_float = float(cleaned)
        return cleaned_float
    except ValueError:
        return 0.0  # Retornar 0.0 si el string no puede ser convertido a float
