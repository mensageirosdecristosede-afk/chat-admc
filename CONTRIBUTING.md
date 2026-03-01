# Contributing

Boas práticas para contribuir e manter histórico limpo.

Branching e nomes de branch
- `main` — branch protegida para produção.
- `feat/<descricao>` — novas features.
- `fix/<descricao>` — correções de bugs.
- `chore/<descricao>` — manutenção, infra, docs.
- `release/<versao>` — branch para preparação de release.

Commits
- Use Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.

Pull Requests
- Abra PRs contra `main` a partir de uma branch de feature/fix.
- Preencha o template de PR e peça revisão.
- Não faça merge direto em `main` sem revisão; use squash/merge ou merge commit conforme política do time.

Labels e fluxo
- Labels sugeridas (veja `.github/labels.yml`): `bug`, `enhancement`, `documentation`, `chore`, `security`, `release`.
- Para criar uma nova branch local e empurrar:

```bash
git checkout -b feat/minha-nova-funcionalidade
git commit -m "feat: descrição curta"
git push -u origin feat/minha-nova-funcionalidade
```

- Para criar labels via `gh` (se preferir):

```bash
# exemplo: criar label
gh label create "enhancement" --color 0e8a16 --description "New feature or request"
```

Reescrita de histórico
- Evite reescrever histórico em branches compartilhadas.
- Quando for necessário (remover segredos), combine com time e instrua todos a recriarem clones.
