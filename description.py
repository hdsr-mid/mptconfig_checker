"""
1
inpar = internal parameter
- Staat inpar in parameter xml?

2
Inpar <> exper
- SS.0 hoort bij schuif en niet bij stuw

3
sublocs expar HRx
- uitgangspunt: als een sublocatie en stuurpeil heeft, dan zouden alle sublocatie die
  relevant zijn (waaraan een stuurpeil zou kunnen zijn gekoppeld) ook een stuurpeil moeten hebben.
- nooit: krooshek, totaal debiet, debiet meter
- rest in theorie wel

4
HistTags per inloc+inpar
- Alleen deze drie mogen voorkomen:
    - de 3-cijferige
    - 4-cijferige
    - eventueel x8xx.
- Echter 1006 en 1007 mogen niet gekoppeld aan KW1006
- Hoe voorkom je dat meerdere HistTags die niet bij elkaar horen op 1 meetpunt terecht komen?

5
inloc+inpar per HistTag
- Stel dat je inpar Q.G.0 (debiet) en je hebt 2 sublocatie en KW100011 en KW100012,
  en dat ze beide gevoed worden door dezelfde HistTag. Dat kan niet (1 CAW HistTag
  die 2 meetpunten voedt), behalve voor stuurpeil, want die kan op meerdere sublocaties
  (of wellicht moet er een tweede stuurpeil).
- Bijv. 1 stuurpeil op 2 pompen (in 1 gemaalhuis) (alternerend sturing, beide maar halve toeren)
- M.a.w.: deze check geeft niet een oplossing, maar wel of er mogelijk iets aan de hand is

6
Inloc in validatie-CSV’s
- Voor streefhoogte, hefhoogte, opening percentage hebben we aparte validatie csvs voor
- In Validatie csv staan validatie criteria per type tijdreeks
- Elke csv staat voor een type parameter
- Van een parameter zijn er meerdere locaties waar die voorkomt
- Per locatie (bijv KWxxxx) staat er een regel in zon csv:
    - Streef 1 H.S.0
    - streef 2 H2.S.0
- ff zij-stapje: alle validatie csvs kunnen meerdere validatie perioden hebben per kunstwerk:
    - 1 meetpunt kan meerdere validatie periode hebben
    - Locatie.csv heeft start end: zegt iets over geldigheid van de locatie
    - Oppvlwater_watervalidatie.csv heeft ook start endate: is start eind van validatie periode)
    - Per definitie zijn deze validatie periode aansluitend (nooit een gat of overlappend!)
    - We hoeven deze Oppvlwater_watervalidatie.csv niet te relateren aan sublocaties (die hebben we nu ontkoppelt)

7
Inloc in mpt-CSV’s
- Als iets in id_mapping (als in loc) zit, dan ook in mpt csv (dat moet)!
- Andersom niet. Waarom niet?
    - onbemeten sublocaties, hoofdlocatie is niet altijd een Hs
    - Id mapping is geldig voor hele historie. Er zijn meer in mpt.csv dan dat er
      in id_mapping staan. Dat heeft te maken met onbemeten objecten. Deze hebben allen een
      fictieve startdatum 1900 en een fictieve einddatum 32101230.
        - Sublocaties
            - Vispassage (onbemeten locatie)
            - Pomp
            - Stuw
            - Afsluiter
            - Totaal
            - Debietmeter (altijd tijdreeks in id-mappiing, moet dus ook in csv)
            - Krooshek (als er geen tijdreeks wordt aangeboden, dan ook niet
              als sublocatie definieren, want niet relevant voor waterverplaatsing)
        - Hoofdlocatie
            - Bijna altijd streefpeil
            - Debietmeter (stand alone)
            - Waterstandloc.csv (Alles wat hier in zit, moet WEL in id_mapping!)

8
Subloc HBOV/HBEN in Wsloc CSV
- Hebben we in de subloc table kolom hbov/hben wel ingevuld een id die bestaat in de waterstand locatie tabel?

9
Subloc HBOVPS/HBENPS in Peilschaal CSV
- Hebben we in de subloc table kolom hbovPS/hbenPS wel ingevuld een id die bestaat in de PS locatie tabel?

10
Subloc HBOVPS/HBENPS <> Wsloc PEILSCHAAL
- OW tabel heeft een kolom peilschaal (relatie datalogger en een peilschaal).
- Database opzet niet ideaal, want deze relatie HBOVPs en HBOV wordt ook al gekoppeld in de subloc tabel
- Koppeling is nogmaals gemaakt, omdat FEWS niet kan omgaan met nested relations
    - Roger: is jammer, maar aan andere kant:
        - wordt het met nested relations al heel snel complex
        - zonder nested is snellere performance

11
Subloc LOC_NAME <> TYPE+FUNCTIE
- Locatienaam is opgebouwd uit verschillende onderdelen: NOOITGEDACHT_1059-K_NOOITGEDACHT SCHUIF-schuif1_aanvoer
- Check of type (is aparte kolom in subloc) matched met type in naam. Die ‘_aanvoer’
  hierboven in naam wordt handmatig ingevuld door MID mpt config databeheerder.

12
Sublocs: PARENT gelijk = XY, SYSTEEM, RAYON, KOMPAS gelijk
- Parent is hier niet peilgebied, maar hoofdloc (vs subloc)
- XY, SYSTEEM, RAYON, KOMPAS zijn kolommen in subloc csv
- Alle sublocaties van 1 hoofdlocatie moeten dezelfde XY, dezelfde SYSTEEM, etc hebben

13
Subloc TYPE <> Inpar
- Als je weet dat het een stuw dan moet er een Hk.0 zijn
- Renier: soms wordt van een stuw toch niet Hk.0 gemeten?
- Roger: Je kijkt naar bestaande relaties in idmapping

14
Subloc PARENT <> Subloc LOC_ID[:7][0]
- Conventie check van subloc id
- LOC_ID = bijv KW100013
- LOC_ID[:7] = KW10001
- Dus hoofloc moet KW100010 zijn

15
Subloc PARENT in Hoofdloc CSV
- KW100010 moet wel in hoofdloc staan

16
Wsloc XY != Hoofdloc XY
- Spreekt voor zich
- Hdsr XY werkt niet met decimalen, maar met hele meters
- Renier: als OW binnen 1 meter van KW ligt, dan toch probleem?
- Roger: KW staat per definitie op de peilgrens en OW moet IN een peilvak liggen

17
Wsloc PEILSCHAAL in Peilschaal CSV
- Spreekt voor zich
"""
