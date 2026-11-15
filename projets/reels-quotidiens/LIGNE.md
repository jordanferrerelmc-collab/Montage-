# Reels quotidiens — Specimen Agency (@specimenagency974)

**Un Reel de 20 s par jour, publié à 8 h, heure de La Réunion** (demande de l'utilisateur, 15/11/2026 : d'abord deux
par jour à 8 h et 19 h, puis ramené à un seul à 8 h le jour même ; la tâche de 19 h est désactivée).
Objectif du compte : donner des conseils aux entreprises et obtenir des clients potentiels (devis en message privé).

## Cible

Gérants de commerces, restaurants, artisans et indépendants **de La Réunion** qui veulent plus de clients grâce à
Instagram. Pas les community managers, pas le grand public.

## Format d'un Reel (verrouillé)

- 20 s environ (voix ≤ 17,3 s + logo de fin 2,2 s), 40 à 46 mots, **phrases courtes, aucune phrase inutile**.
- Structure : accroche (2 s) → histoire courte d'un commerce (problème → déclic) → leçon en une phrase →
  appel à l'action « Abonne-toi, et enregistre ce Reel. »
- Tutoiement. Français simple. Une seule idée par Reel.
- **Pas de faux chiffres, pas de faux témoignage, pas de promesse de résultat.** Les histoires sont des cas types
  (« un restaurateur », « une boutique »), jamais présentées comme un client réel de l'agence.
- Charte Specimen Agency (or, noir, ivoire, TeX Gyre Heros), modèle `templates/reel-conseil/`, voix clonée de
  l'utilisateur (`voix/voix_reference.wav`), bruitages maison `effets/sfx/`.
- Légende Instagram : accroche, 2 phrases de valeur, une action concrète, « Enregistre », « Abonne-toi »,
  « Devis gratuit en message privé », 5 hashtags maximum dont `#974` et `#lareunion`.

## Thèmes (tourner, ne jamais répéter un sujet déjà dans `specs/`)

1. Accroche et 3 premières secondes   2. Raconter son histoire / coulisses   3. Régularité et calendrier
4. Montrer son visage, son équipe      5. Preuve : avis clients, avant / après   6. Appel à l'action et message privé
7. Biographie et profil qui convertit  8. Erreurs fréquentes (logo, musique, texte illisible)
9. Local : parler aux gens de l'île, lieux, créole, événements   10. Reels contre photos, formats
11. Répondre aux commentaires et messages   12. Offre claire, prix, réservation

## Fabriquer un Reel

```bash
npm run voix:install                      # une fois par session (≈ 5 min, 6 Go)
# modèle de transcription (relecture de la voix), s'il manque dans ~/.cache/hyperframes/whisper/models/ :
curl -fsL -o ~/.cache/hyperframes/whisper/models/ggml-small.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
/root/.venvs/voice/bin/python projets/reels-quotidiens/scripts/make_reel.py projets/reels-quotidiens/specs/<NNN-nom>.json
```

- Fiche `specs/<NNN-nom>.json` : `id`, `titre`, `theme`, `legende`, `plans[]` (une phrase de voix + un visuel :
  `titre`, `carte`, `duo`, `etapes`, `cta`). Prendre `001-zero-client.json` comme modèle. Numéro `NNN` croissant.
- Le script relit chaque phrase par transcription et la régénère si un mot est déformé. Si une phrase reste sous
  0,85 après 5 essais (ligne « ATTENTION »), **reformuler la phrase** et relancer.
- Relire sur `hyperframes snapshot` (texte centré, rien de coupé), puis vérifier la durée (19 à 21,5 s).
- Sorties : `file/<id>.mp4` + `file/<id>.json` (versionnés : c'est la file d'attente de publication),
  `final/<id>-hd.mp4` (non versionné).
- Valider puis pousser : `git add projets/reels-quotidiens && git commit && git push`.

## Publier (file d'attente, premier entré, premier sorti)

- À publier = le plus petit `NNN` de `file/*.mp4` absent de `publies.json`.
- Adresse publique de la vidéo (le dépôt est public) :
  `https://raw.githubusercontent.com/jordanferrerelmc-collab/Montage-/<SHA du commit poussé>/projets/reels-quotidiens/file/<id>.mp4`
  Vérifier qu'elle répond 200 avant de publier.
- Connecteur Windsor.ai : `execute_action(connector="instagram", action="create_video_post",
  account="17841441686731067", params={video_url, caption (= legende), share_to_feed: true})`.
- Après succès : ajouter `{id, date, media_id / permalien}` à `publies.json`, valider et pousser.
- Si la file est vide ou si la publication échoue : **ne rien publier d'autre**, ne pas réessayer en boucle,
  prévenir l'utilisateur avec le message d'erreur exact.
- **Délai dépassé (constaté le 15/11/2026)** : `execute_action` peut répondre « timed out after 60s » alors que le Reel
  est bien publié. Ne JAMAIS relancer : relire d'abord les publications du jour (`get_data`, champs `timestamp`,
  `media_id`, `media_caption`, `media_permalink`, `date_preset=last_3dT`, sans `force_refresh`) ; ne republier que si
  le Reel est absent après plusieurs minutes.
- Une seule publication par créneau. Jamais deux fois le même Reel.

## Suivi

Chaque dimanche, relever les statistiques des 14 derniers Reels (vues, durée moyenne, taux de passage avant 3 s,
enregistrements) et noter dans `SUIVI.md` les accroches et thèmes qui marchent, pour orienter les scripts suivants.
