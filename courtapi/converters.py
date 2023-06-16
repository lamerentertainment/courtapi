from .dict_db import \
    pronomen_ersetzungen_m, \
    pronomen_ersetzungen_w, \
    ocr_ersetzungen, \
    verben_ersetzung_praesens, \
    verben_ersetzung_praeteritum
import re


def ersetze_wort(textstelle, ausgangswort, ersetzung, ocr_ersetzung=False):
    """
        Ersetzt das Ausgangswort in einem Textstelle-String durch die angegebene Ersetzung.

        Args:
            textstelle (str): Der Textstelle-String, in dem das Ausgangswort ersetzt werden soll.
            ausgangswort (str): Das Ausgangswort, das ersetzt werden soll.
            ersetzung (str): Die Ersetzung für das Ausgangswort.
            ocr_ersetzung (bool): Falls es sich um die OCR Ersetzung handelt, sollte hier auf True gesetzt werden.
                                  Dann wird die Methode capitalize nicht verwendet (weil oft grossgeschriebene Wörter) falsch
                                  erkannt werden

        Returns:
            str: Der modifizierte Textstelle-String mit der durchgeführten Ersetzung.

        Ersetzt das Ausgangswort mit der Ersetzung, wenn es von Leerzeichen umgeben ist.
        Ersetzt das Ausgangswort mit der Ersetzung, wenn es von einem Komma gefolgt ist.
        Ersetzt das Ausgangswort mit der Ersetzung, wenn es von einem Punkt gefolgt ist.
        Ersetzt das Ausgangswort mit der Ersetzung, wenn es am Satzanfang steht und großgeschrieben wird.
        (Bei OCR-Ersetzung: True) wird kein capitalizce durchgeführt
        """
    # Ersetze das Ausgangswort mit der Ersetzung, wenn es von Leerzeichen umgeben ist
    textstelle = textstelle.replace(" " + ausgangswort + " ", " " + ersetzung + " ")
    # Ersetze das Ausgangswort mit der Ersetzung, wenn es von einem Komma gefolgt ist
    textstelle = textstelle.replace(" " + ausgangswort + ",", " " + ersetzung + ",")
    # Ersetze das Ausgangswort mit der Ersetzung, wenn es von einem Punkt gefolgt ist
    textstelle = textstelle.replace(" " + ausgangswort + ".", " " + ersetzung + ".")
    # Ersetze das Ausgangswort mit der Ersetzung, wenn es am Satzanfang steht und großgeschrieben wird
    if not ocr_ersetzung:
        textstelle = textstelle.replace(ausgangswort.capitalize() + " ", ersetzung.capitalize() + " ")
    else:
        textstelle = textstelle.replace(ausgangswort + " ", ersetzung + " ")
        textstelle = textstelle.replace(ausgangswort.capitalize() + " ", ersetzung.capitalize() + " ")

    return textstelle


def ersetze_vergangenheitsform(textstelle, verb, verbersetzung, hilfsverb):
    # Erstelle ein Regex-Objekt
    regex = re.compile(verb + r'(.*?)(\.|,|!|\?|\bund\b|\boder\b)', re.MULTILINE)

    # Durchlaufe alle Übereinstimmungen im Text
    for match in regex.finditer(textstelle):
        groups = match.groups()
        # Je nachdem, ob ein Satzzeichen am Ende des Regex-Matches steht oder nicht
        # (d. h. "und" oder "oder" steht am Ende), muss das Leerzeichen anders eingefügt werden
        if groups[1] == "und" or groups[1] == "oder":
            textstelle = textstelle.replace(match.group(), verbersetzung + groups[0] + hilfsverb + " " + groups[1])
        else:
            textstelle = textstelle.replace(match.group(), verbersetzung + groups[0] + " " + hilfsverb + groups[1])

    return textstelle


def zeilenumbrueche_entfernen(textstelle):
    # Allfällige Leerzeichen am Ende der Zeile löschen
    textstelle = re.sub(r'\s+$', '', textstelle, flags=re.MULTILINE)
    # Wenn Buchstabe, Ziffer oder Unterstrich am Ende der Zeile (ausser Bindestrich), Leerschlag hinzufügen
    textstelle = re.sub(r'([^-])$', r'\1 ', textstelle, flags=re.MULTILINE)
    # Bindestrich am Ende der Zeile löschen
    textstelle = re.sub(r'-$', '', textstelle, flags=re.MULTILINE)

    # Zeilenumbrüche (andere Art) entfernen
    textstelle = textstelle.replace('\n', '')
    # Carriage breaks (Zeilenumbrüche) entfernen
    textstelle = textstelle.replace('\r', '')

    # doppelte und dreifache Leerzeichen ersetzen
    textstelle = textstelle.replace('  ', ' ')
    textstelle = textstelle.replace('   ', ' ')

    # gekreuzte Anführungs- und Schlusszeichenformatierung ersetzen
    textstelle = textstelle.replace(chr(171), chr(34))
    textstelle = textstelle.replace(chr(187), chr(34))

    # Frankenformatierung
    textstelle = textstelle.replace(' CHF ', ' Fr. ')
    textstelle = textstelle.replace(' SFR ', ' Fr. ')
    textstelle = textstelle.replace('.00 ', '.-- ')

    # entferne Platzhalterquadrat für unbekanntes Zeichen
    textstelle = textstelle.replace(chr(0), '')

    return textstelle


def umlautkorrektur(textstelle):
    textstelle = bytes(textstelle, "utf-8").decode("unicode_escape")
    return textstelle


def ocr_ersetzung(textstelle):
    """
        Ersetzt typische Fehler, die bei der OCR Texterkennung entstehen (oft wird dass grossgeschriebene I als kleines l missinterpretiert)

        Args:
            textstelle (str): Die zu bearbeitende Textstelle.

        Returns:
            str: Der modifizierte Text mit den ersetzen Wörtern.

        """
    for ausgangswort, ersetzung in ocr_ersetzungen.items():
        textstelle = ersetze_wort(textstelle, ausgangswort, ersetzung, ocr_ersetzung=True)

    return textstelle


def pronomen_ersetzung(textstelle, geschlecht='m'):
    """
        Ersetzt Pronomen in einer Textstelle entsprechend dem angegebenen Geschlecht.

        Args:
            textstelle (str): Die Textstelle, in der die Pronomen ersetzt werden sollen.
            geschlecht (str, optional): Das Geschlecht, für das die Pronomen ersetzt werden sollen.
                Akzeptierte Werte: 'm' (männlich) oder 'w' (weiblich). Standardmäßig ist das Geschlecht auf 'm' eingestellt.

        Returns:
            str: Die Textstelle mit den vorgenommenen Pronomen-Ersetzungen.

        """
    if geschlecht == 'm':
        ersetzungen_dict = pronomen_ersetzungen_m
    elif geschlecht == "w":
        ersetzungen_dict = pronomen_ersetzungen_w

    for ausgangswort, ersetzung in ersetzungen_dict.items():
        textstelle = ersetze_wort(textstelle, ausgangswort, ersetzung)

    return textstelle


def verben_ersetzung(textstelle):
    for ausgangswort, ersetzung in verben_ersetzung_praesens.items():
        textstelle = ersetze_wort(textstelle, ausgangswort, ersetzung)

    for ausgangswort, ersetzungen in verben_ersetzung_praeteritum.items():
        textstelle = ersetze_vergangenheitsform(textstelle, ausgangswort, ersetzungen[0], ersetzungen[1])

    return textstelle


def als_aussage_formatieren(textstelle, geschlecht='m'):
    textstelle = umlautkorrektur(textstelle)
    textstelle = zeilenumbrueche_entfernen(textstelle)
    textstelle = ocr_ersetzung(textstelle)
    textstelle = pronomen_ersetzung(textstelle, geschlecht)
    textstelle = verben_ersetzung(textstelle)
    return textstelle
