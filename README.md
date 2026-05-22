# Petget — Breeding Management for Odoo

Petget is a free, open-source (AGPL-3) **breeding management platform** for Odoo
Community 19. It is built around a species-agnostic core (`petget.animal`) so the
same foundation serves dogs today and other species over time.

All modules are **100% free** on the Odoo Apps Store. There are no paid modules,
no feature gates, and no license fees. If you want help deploying, configuring for
your local regulations, migrating data, or training your team, BSD offers
project-based implementation services — see **https://thepetget.com**.

## Modules

| Module | What it does | Depends on |
|---|---|---|
| `petget_core` | Foundation: animals, owners, documents, reminders, notes | base, mail, contacts |
| `petget_breeding_core` | Heat cycles, mating/AI, pregnancy, litters | petget_core |
| `petget_dog` | Dog species extension + breed catalogue | petget_core |
| `petget_dog_knowledge` | Breed knowledge: life stages, feeding, growth, reproduction | petget_dog |
| `petget_health` | Hip/elbow scoring, DNA panels, breeding-clearance warnings | petget_breeding_core |
| `petget_pedigree` | Registration details + multi-generation pedigree tree | petget_core |
| `petget_buyer_sale` | Buyers, reservations, deposits, sale tracking (no invoicing) | petget_core |
| `petget_customer_followup` | Automatic customer-care tasks after a sale | petget_buyer_sale |
| `petget_compliance_au` | Australian state breeding compliance rules and warnings | petget_breeding_core |

Start with `petget_core` + `petget_dog`. Add the rest as you need them.

## Install

1. Copy the module folders into your Odoo `addons_path`.
2. Restart Odoo and update the apps list.
3. Install **Petget: Core** (and **Petget: Dog**), then any extensions.

Requires Odoo Community **19.0**.

## License

Every module here is licensed **AGPL-3** (see `LICENSE`). You may use, study,
modify, and redistribute them under the terms of that license.

## About

Petget is developed and maintained by **BSD**. Commercial implementation,
compliance configuration, data migration, hosting and training are available as
paid services at **https://thepetget.com**.
