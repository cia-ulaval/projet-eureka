# projet-eureka

## Backend

#### GET /map
Permet de récupérer les informations dynamiques de la map

**Response**

end: Point d'arrivée [x, y]

start: Point de départ [x, y]

traffic: Traffic sur chaque case de la map
(0: Circulation bloqué/Traffic max, 1: Circulation fluide/Pas de traffic)
```
{
    "end": [int, int],
    "start": [int, int],
    "traffic": 
        [[float,...],...]
}
```
Exemple:
```
{
    "end": [9, 9],
    "start": [20, 18 ],
    "traffic": [
        [
            0.5420786148298,
            0,
            ...
        ]
    ]
}
```

#### POST /score
Permet de récupérer le score

**Body**

path: Chemin emprunté par le joueur
```
{
    "path": [[int, int],...]
}
```
Exemple: 
```
{
    "path" : [
        [20, 18],
        [19, 18],
        ...
        ]
}
```

**Response**

human_stats: Statistiques du joueur

ai_stats: Statistiques de l'IA

co2: Quantité de CO2 total émis durant le trajet

wait: Temps d'attente total durant le trajet

AI_path: Chemin emprunté par l'IA
```
{
    "human_stats": {
        "co2": float,
        "wait": float
    },
    "AI_path": [[int, int],...],
    "AI_stats": {
        "co2": float,
        "wait": float
    }
}
```
Exemple:
```
{
     "AI_stats": {
        "co2": 12.719999999,
        "wait": 20.0
    },
    "AI_path": [
        [10, 9],
        [11, 9],
        ...
        ],
    "human_stats": {
        "co2": 48.728571428,
        "wait": 225.0
    }
}
```