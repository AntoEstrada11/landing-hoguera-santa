# Protección de rama `main` en Gitea

Repo: **https://git.allanmontero.com/aneg/landing-hoguera-santa**

Objetivo: nadie hace merge a `main` sin Pull Request aprobado por **aneg**.

> Esta configuración se hace **una sola vez** en la web de Gitea (no va en el código del repo).

---

## Paso 1 — Dueño del repositorio

Solo el usuario **aneg** debe ser **Owner** del repo.

1. Gitea → repo → **Settings** → **Collaborators** (o **Access**).
2. Colaboradores: rol **Write** (pueden push a ramas, abrir PR).
3. No des rol **Admin** a colaboradores si no deben cambiar reglas de rama.

---

## Paso 2 — Regla de rama protegida

1. **Settings** → **Branches** → **Add rule** (o **New Branch Rule**).
2. **Branch name pattern:** `main`
3. Activar:

| Opción | Valor |
|--------|--------|
| **Protected branch** | Sí |
| **Disable push** / **Enable push protection** | Sí (bloquea push directo a `main`) |
| **Require pull request before merging** | Sí |
| **Required approvals** | `1` |
| **Whitelist for merge** (usuarios que pueden mergear) | Solo **`aneg`** |
| **Dismiss stale approvals** | Recomendado: Sí |

4. Guardar.

---

## Paso 3 — Flujo de trabajo

```
dev / feature/* / contenido
        │
        ▼
   Pull Request → main
        │
        ▼
   aneg revisa y aprueba
        │
        ▼
   Merge (solo aneg)
```

### Comandos habituales (colaboradores)

```bash
git checkout dev
git pull origin dev
# ... cambios ...
git commit -m "feat: ..."
git push origin dev
# Abrir PR en Gitea: dev → main
```

### Merge (solo aneg)

En Gitea: **Pull Requests** → abrir PR → **Review** → **Approve** → **Merge pull request**.

---

## Paso 4 — Verificar que funciona

1. Intenta `git push origin main` desde otra cuenta → debe **rechazar**.
2. Abre un PR de `dev` → `main` → sin aprobación de **aneg** no debe permitir merge.
3. Tras aprobar como **aneg**, el merge debe completarse.

---

## Remotes recomendados

```bash
git remote add gitea https://git.allanmontero.com/aneg/landing-hoguera-santa.git
git remote -v
# origin  → GitHub (opcional, backup)
# gitea   → Gitea aneg (principal para el equipo)
```

Push a Gitea:

```bash
git push gitea main
git push gitea dev
```
