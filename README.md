# Convertisseur de devises : modèles de services cloud

Travail pratique du cours **8INF876 — Conception et architecture des systèmes d'infonuagique**, **Question III** : exemples de code exécutables pour les modèles de services cloud.

Une même application, un **convertisseur de devises** (EUR, USD, CAD, JPY), est déclinée selon plusieurs modèles de services afin de les comparer.

## Accès en ligne

| Modèle | Adresse |
|---|---|
| **FaaS** — fonction de conversion | `https://convertisseur-faas-paas-seven.vercel.app/api/convertir?montant=100&de=EUR&vers=CAD` |
| **SaaS** — application web | `https://convertisseur-faas-paas-k5vx.vercel.app` |
| **PaaS** |

## Architecture

```
Navigateur de l'utilisateur
        │
        ▼
SaaS : application Flask (Vercel)  ──►  Base PostgreSQL (Neon)
        │                                comptes + historique
        ▼
FaaS : fonction de conversion (Vercel)
```

- Le **FaaS** contient toute la logique de conversion. Il ne s'exécute qu'à l'appel et ne garde aucun état.
- Le **SaaS** est le logiciel fini destiné à l'utilisateur : interface web, comptes, historique personnel. Il ne calcule rien lui-même et délègue la conversion au FaaS.