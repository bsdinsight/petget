# Petnaly — Breeding Management for Odoo

Petnaly is a free, open-source (AGPL-3) **breeding management platform** for Odoo
Community 19. It is built around a species-agnostic core (`petnaly.animal`) so the
same foundation serves dogs today, and cats and horses over time.

Every module in this repository is **AGPL-3 and free** — no paid modules, no
feature gates, no license fees. Clone it, run it on your own server, keep it
forever.

If you would rather not run a server yourself, **Petnaly Cloud** is the managed
option: we host, back up and update it for you. See **https://petnaly.com** for
what it includes and what it costs.

## Modules

| Module | What it does | Depends on |
|---|---|---|
| `petnaly_core` | Foundation: animals, owners, documents, reminders, notes | base, mail, contacts |
| `petnaly_breeding_core` | Heat cycles, mating/AI, pregnancy, litters | petnaly_core |
| `petnaly_dog` | Dog species extension + breed catalogue | petnaly_core |
| `petnaly_dog_knowledge` | Breed knowledge: life stages, feeding, growth, reproduction | petnaly_dog |
| `petnaly_health` | Hip/elbow scoring, DNA panels, breeding-clearance warnings | petnaly_breeding_core |
| `petnaly_pedigree` | Registration details + multi-generation pedigree tree | petnaly_core |
| `petnaly_buyer_sale` | Buyers, reservations, deposits, sale tracking (no invoicing) | petnaly_core |
| `petnaly_customer_followup` | Automatic customer-care tasks after a sale | petnaly_buyer_sale |
| `petnaly_compliance_au` | Australian state breeding compliance rules and warnings | petnaly_breeding_core |
| `petnaly_kb` | Breed library, care guides and stories for owners and breeders | petnaly_dog |

Start with `petnaly_core` + `petnaly_dog`. Add the rest as you need them.

## Install

Requires Odoo Community **19.0**.

### With Docker (quickest)

```bash
git clone https://github.com/bsdinsight/petnaly.git
cd petnaly
docker compose up -d
```

Then open <http://localhost:8069>:

1. Odoo asks you to create a database. The master password is in `odoo.conf`;
   you pick your own admin password on that screen — **nothing here ships with
   a default login**.
2. Once the database exists, open **Apps**, then install **Petnaly: Core** and
   **Petnaly: Dog**. Add the other modules as you need them.

The web port is published on `127.0.0.1` only, so a fresh clone is not
reachable from outside your machine. Change `admin_passwd` in `odoo.conf`
before you put this on a server the internet can reach.

### Into an existing Odoo

1. Copy the module folders into your Odoo `addons_path`.
2. Restart Odoo and update the apps list.
3. Install **Petnaly: Core** (and **Petnaly: Dog**), then any extensions.

## License

Every module here is licensed **AGPL-3** (see `LICENSE`). You may use, study,
modify, and redistribute them under the terms of that license.

## About

Petnaly is developed and maintained by **BSD**. Managed hosting, implementation,
compliance configuration, data migration and training are available at
**https://petnaly.com**.
