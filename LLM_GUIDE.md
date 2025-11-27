# Guide d'utilisation du Parser LLM (Gemini)

## 🆕 Nouvelle Fonctionnalité : Parser Intelligent

Le robot peut maintenant comprendre des commandes **beaucoup plus complexes** grâce à Gemini !

## Comparaison Parser Simple vs LLM

### Parser Simple (actuel)
❌ "Va vers le carré rouge" → ✅ Fonctionne
❌ "Va au carré rouge **en passant par** le cercle bleu" → ❌ Ne comprend que la première cible

### Parser LLM (nouveau)
✅ "Va vers le carré rouge" → ✅ Fonctionne
✅ "Va au carré rouge **en passant par** le cercle bleu" → ✅ Comprend les 2 cibles !
✅ "Passe par le bleu, puis le rouge, puis finis au vert" → ✅ Comprend 3 cibles !

## Configuration

### 1. Obtenir une clé API Gemini (gratuit)

1. Aller sur : https://makersuite.google.com/app/apikey
2. Se connecter avec un compte Google
3. Cliquer sur "Create API Key"
4. Copier la clé

### 2. Configurer la clé

**Méthode 1 : Fichier .env (recommandé)**
```bash
cp .env.example .env
# Éditer .env et remplacer your_api_key_here par votre clé
```

**Méthode 2 : Variable d'environnement**
```bash
export GEMINI_API_KEY='votre_clé_ici'
```

## Installation

```bash
pip install google-generativeai
```

Ou :
```bash
pip install -r requirements.txt
```

## Test du Parser LLM

```bash
python3 test_llm.py
```

Résultat attendu :
```
✅ Parser LLM initialisé

[Test 1/7]
📝 Analyse de la commande (LLM): 'Va vers le carré rouge'
  - Interprétation: Le robot doit aller vers le carré rouge.
  - Confiance: 100%
  - Mode: LLM (Gemini)
  - Nombre de cibles: 1
    1. [target] rouge square
```

## Exemples de Commandes Complexes

### Waypoints (points de passage)
```
"Va au carré rouge en passant par le cercle bleu"
```
→ Le robot ira d'abord au cercle bleu, puis au carré rouge

### Séquence de cibles
```
"Rejoins le cercle vert puis le carré jaune"
```
→ Cible 1 : cercle vert, puis Cible 2 : carré jaune

### Commandes très complexes
```
"Passe d'abord par le cercle bleu, puis va au carré rouge, et finis au cercle vert"
```
→ 3 étapes :
1. Cercle bleu (waypoint)
2. Carré rouge (target)
3. Cercle vert (target)

## Limites du Mode Gratuit

- **10 requêtes par minute** (largement suffisant pour usage normal)
- **1500 requêtes par jour**

Si vous dépassez, attendez 1 minute ou passez à un plan payant.

## Fallback Automatique

Si le LLM échoue (pas de clé API, quota dépassé, erreur), le système **bascule automatiquement** sur le parser simple.

```python
# Pas de clé API ? → Parser simple utilisé automatiquement
# Quota dépassé ? → Parser simple utilisé
# Erreur réseau ? → Parser simple utilisé
```

## Intégration dans le Programme Principal

Le parser LLM est **optionnel**. Le programme fonctionne toujours avec le parser simple si :
- Pas de clé API configurée
- Problème de connexion
- Quota dépassé

## Prochaines Étapes

Pour intégrer le parser LLM dans le programme principal ([main.py](main.py)), il faudra :

1. Détecter si la clé API est disponible
2. Utiliser `LLMParser` au lieu de `NLPParser` si disponible
3. Gérer les multi-cibles dans la boucle de navigation
4. Créer des chemins successifs pour chaque waypoint

Voulez-vous que je procède à cette intégration ?

## Avantages du LLM

✅ Comprend le langage naturel (vraiment)
✅ Gère plusieurs cibles
✅ Gère les waypoints ("passe par")
✅ Fallback automatique sur parser simple
✅ Gratuit (avec limites)
✅ Très rapide (Gemini 2.5 Flash)

## Format de Sortie

Le parser LLM retourne :
```python
{
    "targets": [
        {"color": "bleu", "shape": "circle", "type": "waypoint"},
        {"color": "rouge", "shape": "square", "type": "target"}
    ],
    "confidence": 0.95,
    "interpretation": "Aller au carré rouge en passant par le cercle bleu",
    "raw_command": "Va au carré rouge en passant par le cercle bleu"
}
```

## Fichiers Créés

- `src/llm_parser.py` - Parser intelligent avec Gemini
- `test_llm.py` - Script de test
- `.env.example` - Template pour la clé API
- `.env` - Votre clé API (ignoré par git)
- `LLM_GUIDE.md` - Ce fichier

## Questions Fréquentes

### Puis-je utiliser un autre LLM ?
Oui ! Le code peut être adapté pour :
- OpenAI GPT
- Claude (Anthropic)
- Ollama (local, gratuit)

### C'est payant ?
Non, Gemini a un tier gratuit largement suffisant pour ce projet.

### Que se passe-t-il si je dépasse le quota ?
Le parser simple prend le relais automatiquement.

### Le LLM est-il obligatoire ?
Non, le programme fonctionne parfaitement sans.
