# Blog & Newsletter System — MicroClub

API FastAPI combinant deux systèmes : gestion de blog et gestion de newsletter, avec authentification admin via JWT.



---

## Stack technique

- **FastAPI** — framework de l'API
- **SQLAlchemy** — ORM, pour parler à la base de données en Python plutôt qu'en SQL
- **SQLite** — base de données locale (fichier `.db`)
- **Pydantic** — validation des données entrantes/sortantes
- **python-jose** — création et vérification des tokens JWT
- **passlib (bcrypt)** — hashage des mots de passe
- **python-dotenv** — lecture des variables d'environnement (`.env`)

---

## Structure du projet

```
blog-newsletter-system/
├── app/
│   ├── main.py              → point d'entrée, regroupe tous les routers
│   ├── database.py          → connexion SQLAlchemy + session
│   ├── core/
│   │   ├── config.py        → lecture du .env
│   │   └── security.py      → hashage, JWT, dépendance get_current_admin
│   ├── models/               → tables SQLAlchemy (Article, Subscriber, Newsletter, Admin)
│   ├── schemas/               → validation Pydantic (Create / Response)
│   └── routers/
│       ├── public_blog.py    → routes publiques (lecture articles)
│       ├── admin_blog.py      → CRUD articles (protégé JWT)
│       ├── newsletter.py       → abonnement, désabonnement, envoi, historique
│       └── auth.py             → login admin
├── .env                       → variables secrètes (jamais sur GitHub)
└── requirements.txt
```

---




### 1. database.py — les briques de base

- **`engine`** → la connexion physique à la base (sait où et comment se connecter)
- **`Base`** → la classe mère dont héritent tous les models
- **`SessionLocal`** → une "factory" qui fabrique des sessions
- **`Session`** → une conversation temporaire avec la base, ouverte puis fermée
- **`get_db()`** → fonction qui ouvre une session, la donne à la route via `yield`, puis la ferme dans le `finally`

### 2. Hashage des mots de passe

- On ne stocke **jamais** un mot de passe en clair.
- `pwd_context.hash(password)` → transforme `"password123"` en quelque chose comme `$2b$12$...`
- Le **sel** (salt) est un nombre aléatoire ajouté avant le hashage, généré automatiquement par bcrypt. Il garantit que deux mots de passe identiques produisent des hash différents → protège contre les rainbow tables.
- `pwd_context.verify(password_en_clair, hash_stocké)` → compare et retourne `True`/`False`.

### 3. JWT (JSON Web Token)


Un token = `header.payload.signature`
- **header** → l'algorithme (HS256)
- **payload** → les données (ex : `{"sub": "admin@email.com", "exp": ...}`)
- **signature** → générée avec `SECRET_KEY`, garantit que le token n'a pas été modifié

**HS256** = HMAC + SHA-256 → un mécanisme de signature qui combine les données et la clé secrète pour produire une signature impossible à falsifier sans connaître la clé.

Flux complet :
1. Admin envoie email + mot de passe
2. Vérification avec `verify_password`
3. Si OK → `create_access_token({"sub": admin.email})` génère le token
4. Admin renvoie ce token dans chaque requête (`Authorization: Bearer ...`)
5. `get_current_admin` décode le token, retrouve l'admin en base, et protège la route

### 4. Depends — l'injection de dépendances

`Depends(...)` dit à FastAPI : "avant d'exécuter cette route, exécute cette fonction et donne-moi son résultat".

Utilisations dans ce projet :
- `Depends(get_db)` → injecte une session de base de données
- `Depends(get_current_admin)` → vérifie le token JWT et injecte l'admin connecté

### 5. CRUD avec SQLAlchemy

```python
# Create
new_obj = Article(title=..., slug=..., ...)
db.add(new_obj)
db.commit()
db.refresh(new_obj)   # récupère l'id généré

# Read
db.query(Article).filter(Article.slug == slug).first()   # un seul résultat
db.query(Article).filter(Article.is_published == True).all()  # liste

# Update
article.title = nouveau_titre
db.commit()

# Delete
db.delete(article)
db.commit()
```

### 6. Pourquoi pas async/await ici

SQLAlchemy classique est **synchrone**. Mélanger `async def` avec un ORM synchrone bloquerait la boucle événementielle de FastAPI. Pour du vrai async il faudrait SQLAlchemy async ou Tortoise ORM — pas nécessaire pour ce projet.

### 7. .env et sécurité

- `.env` contient les secrets : `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- `python-dotenv` (`load_dotenv()`) charge ces variables dans `os.environ`
- `.env` est dans `.gitignore` → **jamais** poussé sur GitHub

---

## Routes de l'API

### Authentification
| Méthode | Route | Description |
|---|---|---|
| POST | `/auth/login` | Connexion admin → retourne un JWT |

### Blog — public
| Méthode | Route | Description |
|---|---|---|
| GET | `/articles` | Liste des articles publiés |
| GET | `/articles/{slug}` | Détail d'un article |

### Blog — admin (JWT requis)
| Méthode | Route | Description |
|---|---|---|
| POST | `/admin/article` | Créer un article |
| PUT | `/admin/articles/{id}` | Modifier un article |
| DELETE | `/admin/articles/{id}` | Supprimer un article |
| POST | `/admin/articles/{id}/publish` | Publier / dépublier |

### Newsletter — public
| Méthode | Route | Description |
|---|---|---|
| POST | `/subscribe` | S'abonner |
| GET | `/unsubscribe/{email}` | Se désabonner |

### Newsletter — admin (JWT requis)
| Méthode | Route | Description |
|---|---|---|
| GET | `/admin/subscribers` | Liste des abonnés actifs |
| POST | `/admin/newsletter/send` | Envoyer une newsletter |
| GET | `/admin/newsletter/history` | Historique des envois |

---

## Lancer le projet

```bash
venv\Scripts\activate
uvicorn app.main:app --reload
```

Puis ouvrir : `http://127.0.0.1:8000/docs`

---

## À faire

- [ ] Protéger les routes `/admin/*` avec `Depends(get_current_admin)`
- [ ] `services/email_service.py` — envoi réel des newsletters par email
- [ ] Tests complets sur Swagger UI
