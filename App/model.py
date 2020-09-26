"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    analyzer = {"accidents": None,
                "dateIndex": None
                }
    analyzer["accidents"] = lt.newList("SINGLE_LINKED", compareIds)
    analyzer["dateIndex"] = om.newMap(omaptype="BST",comparefunction=compareDates)
    
    return analyzer

# Funciones para agregar informacion al catalogo
def addAccident(analyzer,accident):
    """
    """
    lt.addLast(analyzer["accidents"],accident)
    updateDateIndex(analyzer["dateIndex"], accident)
    return analyzer

def updateDateIndex(map,accident):
    occurreddate = accident["Start_Time"]
    accidentdate = datetime.datetime.strptime(occurreddate, "%Y-%m-%d %H:%M:%S")
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(),datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry,accident)
    return map

def addDateIndex(datentry, accident):
    lst = datentry["lstaccidents"]
    lt.addLast(lst, accident)
    severityIndex = datentry["severityIndex"]
    seventry = m.get(severityIndex, accident["Severity"])
    if seventry is None:
        entry = newSeverityEntry(accident["Severity"], accident)
        lt.addLast(entry["lstseverities"],accident)
        m.put(severityIndex, accident["Severity"], entry)
    else:
        entry = me.getValue(seventry)
        lt.addLast(entry["lstseverities"], accident)
    return datentry

def newDataEntry(accident):
    entry = {"severityIndex":None, "lstaccidents": None}
    entry["severityIndex"] = m.newMap(numelements=30,
                                      maptype="PROBING",
                                      comparefunction= compareSeverities)
    entry["lstaccidents"] = lt.newList("SINGLE_LINKED", compareDates)
    return entry

def newSeverityEntry(sev, accident):
    seventry = {"severity": None, "lstseverities": None}
    seventry["severity"] = sev
    seventry["lstseverities"] = lt.newList("SINGLE_LINKED", compareSeverities)
    return seventry

# ==============================
# Funciones de consulta
# ==============================

def accidentsSize(analyzer):

    return lt.size(analyzer["accidents"])

def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])

def getAccidentsByDate(analyzer,date):
    
    accidentdate = om.get(analyzer["dateIndex"], date)
    try:
        if accidentdate["key"] is not None:
            mapa = me.getValue(accidentdate)["severityIndex"]
            info = []
            for i in range(1,5):
                entry = m.get(mapa,str(i))
                if entry is not None:
                    lst = me.getValue(entry)["lstseverities"]
                    size = lt.size(lst)
                    info.append(size)
                else:
                   info.append(0)
            return info
    except:
        return None

# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareSeverities(sev1, sev2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    sev = me.getKey(sev2)
    if (sev1 == sev):
        return 0
    elif (sev1 > sev):
        return 1
    else:
        return -1