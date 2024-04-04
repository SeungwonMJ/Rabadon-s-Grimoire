from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt
import requests

def fetchItemPixmap(itemID, IMAGE_LOCATION):
    if itemID == 0:
        pixmap = QPixmap(30, 30)
        pixmap.fill(QColor(100, 100, 100))
        return pixmap
    
    pixmap = QPixmap(IMAGE_LOCATION + 'item/' + str(itemID) + '.png').scaled(30, 30, mode=Qt.SmoothTransformation)
    
    return pixmap


def fetchChampPixmap(champName, IMAGE_LOCATION):
    pixmap = QPixmap(IMAGE_LOCATION + 'champion/' + str(champName) + '.png').scaled(30, 30, mode=Qt.SmoothTransformation)

    return pixmap


def fetchProfileInfo(PUUID, BASE_URL):
    userData = requests.get(BASE_URL + '/user/by-PUUID/' + str(PUUID)).json()
    requests.put(BASE_URL + '/update-user/' + str(PUUID))
    games = fetchGameInfo(userData, BASE_URL, '/0/20')
    
    data = {
        "userData": userData,
        "games": games
    }
    
    return data


def fetchGameInfo(userData, BASE_URL, indexes):
    gamesIDS = requests.get(BASE_URL + '/game-id/x-x/' + userData['PUUID'] + indexes).json()
    games = dict()
    for game in gamesIDS:
        gameData = requests.get(BASE_URL + '/game-data/all/' + game).json()
        games[game] = gameData

    return games


def fetchChampInfo(PUUID, BASE_URL):
    champStats = requests.get(BASE_URL + '/champ-stats/' + PUUID).json()
    gamesPlayed = requests.get(BASE_URL + '/user/games-played/' + PUUID).json()

    return gamesPlayed, champStats