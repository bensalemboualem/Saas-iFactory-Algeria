# Gouvernance de la documentation multilingue IAFactory

Cette page décrit les règles et bonnes pratiques pour maintenir la documentation IAFactory synchronisée en français (FR), anglais (EN) et arabe (AR).

## Langue source
- La langue source par défaut est le **français** (FR) pour toute la documentation IAFactory.
- Certaines parties techniques/API peuvent être rédigées d’abord en anglais (EN) si besoin, puis traduites en FR/AR.

## Workflow de traduction
1. **Modification d’un fichier source (FR ou EN)**
   - Copier la structure et le contenu dans les fichiers EN/AR correspondants.
   - Ajouter un marqueur `TODO(EN)` ou `TODO(AR)` en haut de chaque fichier non encore traduit.
2. **Traduction**
   - Traduire le contenu en respectant la structure et les sections du fichier source.
   - Retirer le marqueur `TODO` une fois la traduction validée.
3. **Mise à jour**
   - Lorsqu’une modification est faite sur la version source, reporter rapidement l’évolution sur les autres langues avec un `TODO` si la traduction n’est pas immédiate.

## Versioning & suivi
- L’alignement des versions se fait manuellement (ou via Git) : chaque fichier EN/AR doit refléter la même version de contenu que le FR.
- En cas de divergence, ajouter un commentaire ou un `TODO` précisant la section à mettre à jour.
- Utiliser des commits explicites pour tracer les évolutions multilingues.

## Bonnes pratiques (fiscal/juridique)
- Les contenus à portée fiscale ou juridique doivent être validés par un professionnel local avant publication ou traduction.
- Ajouter un avertissement dans les fichiers concernés : « Ce contenu ne remplace pas un conseil professionnel. »
- Privilégier la clarté et la neutralité dans la traduction, sans interprétation.

## Ressources utiles
- [API Documentation Localization – 10 Best Practices](https://daily.dev/blog/api-documentation-localization-10-best-practices)
- [Managing Multilingual Documents & Version Control](https://www.dbi-services.com/blog/managing-multilingual-documents-including-version-control/)
- [Traduction technique et QA](https://fr.smartling.com/blog/technical-documentation-translation)

Pour toute question, contactez l’équipe documentation IAFactory.
