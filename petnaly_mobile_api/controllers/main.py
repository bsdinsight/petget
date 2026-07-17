import base64
import json
from datetime import timedelta

from werkzeug.wrappers import Response

from odoo import fields, http
from odoo.http import request

API = '/api/v1'
CORS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
}


class PetnalyMobileAPI(http.Controller):

    # ---------------- helpers ----------------
    def _json(self, payload, status=200):
        return Response(
            json.dumps(payload, default=str), status=status,
            content_type='application/json; charset=utf-8',
            headers=list(CORS.items()),
        )

    def _ok(self, data=None, status=200):
        body = {'ok': True}
        if isinstance(data, dict):
            body.update(data)
        elif data is not None:
            body['data'] = data
        return self._json(body, status)

    def _err(self, code, status=400, message=None):
        return self._json({'ok': False, 'error': code, 'message': message or code}, status)

    def _body(self):
        try:
            return json.loads(request.httprequest.get_data(as_text=True) or '{}')
        except Exception:
            return {}

    def _is_options(self):
        return request.httprequest.method == 'OPTIONS'

    def _auth(self):
        h = request.httprequest.headers.get('Authorization', '') or ''
        if not h.lower().startswith('bearer '):
            return None
        tok = request.env['petnaly.mobile.token'].sudo().search(
            [('token', '=', h[7:].strip()), ('active', '=', True)], limit=1)
        if not tok or (tok.expires_at and tok.expires_at < fields.Datetime.now()):
            return None
        tok.last_used_at = fields.Datetime.now()
        return tok.user_id

    def _issue_token(self, user, device=None):
        tok = request.env['petnaly.mobile.token'].sudo().create({
            'user_id': user.id,
            'device_name': device or 'mobile',
            'expires_at': fields.Datetime.now() + timedelta(days=30),
        })
        return self._ok({
            'token': tok.token,
            'user': {
                'uid': user.id, 'name': user.name, 'email': user.login,
                'partner_id': user.partner_id.id,
            },
        })

    @staticmethod
    def _img(value):
        if not value:
            return False
        if isinstance(value, bytes):
            value = value.decode()
        return 'data:image/png;base64,%s' % value

    # ---------------- serializers (record passed already sudo) ----------------
    def _pet_brief(self, a):
        return {
            'id': a.id, 'system_id': a.system_id, 'name': a.name,
            'species': a.species, 'sex': a.sex,
            'breed': a.breed_id.name if 'breed_id' in a._fields and a.breed_id else None,
            'date_of_birth': a.date_of_birth or None,
            'age': a.age_display, 'status': a.status,
            'sale_state': a.sale_state if 'sale_state' in a._fields else None,
            'photo': self._img(a.image_128),
        }

    def _pet_detail(self, a):
        d = self._pet_brief(a)
        d['photo'] = self._img(a.image_256)
        d.update({
            'registered_name': a.registered_name,
            'microchip': a.microchip,
            'registration_number': a.registration_number,
            'color': a.color_id.name if 'color_id' in a._fields and a.color_id else a.color,
            'owner': a.owner_id.name or None,
            'sire': a.sire_id.name or None,
            'dam': a.dam_id.name or None,
        })
        if 'coi_percent' in a._fields:
            d['coi_percent'] = a.coi_percent
        if 'pedigree_html' in a._fields:
            d['pedigree_html'] = a.pedigree_html or None
        # documents
        d['documents'] = [{
            'id': doc.id, 'name': doc.name, 'category': doc.category,
            'file_name': doc.file_name,
            'download': '%s/documents/%s/download' % (API, doc.id),
        } for doc in a.document_ids]
        # reminders
        d['reminders'] = [{
            'id': r.id, 'name': r.name, 'type': r.reminder_type,
            'due_date': r.due_date or None, 'state': r.state,
        } for r in a.reminder_ids]
        # health tests (optional module)
        d['health_tests'] = []
        if 'petnaly.health.test' in request.env:
            tests = request.env['petnaly.health.test'].sudo().search([('animal_id', '=', a.id)])
            d['health_tests'] = [{
                'id': t.id, 'type': t.test_type, 'result': t.result,
                'date': t.test_date or None,
                'dna_marker': t.dna_marker if 'dna_marker' in t._fields else None,
                'hip_score': t.hip_score_total if 'hip_score_total' in t._fields else None,
                'report_number': t.report_number if 'report_number' in t._fields else None,
            } for t in tests]
        return d

    # ---------------- public endpoints ----------------
    @http.route([API, f'{API}/health'], type='http', auth='public',
                methods=['GET', 'OPTIONS'], csrf=False)
    def health(self, **kw):
        if self._is_options():
            return self._json({}, 200)
        return self._ok({'service': 'Petnaly API', 'version': 'v1', 'status': 'up'})

    @http.route(f'{API}/auth/signup', type='http', auth='public',
                methods=['POST', 'OPTIONS'], csrf=False)
    def signup(self, **kw):
        if self._is_options():
            return self._json({}, 200)
        d = self._body()
        email = (d.get('email') or '').strip().lower()
        pwd = d.get('password') or ''
        if not email or not pwd:
            return self._err('missing_fields', 400)
        Users = request.env['res.users'].sudo()
        if Users.search([('login', '=', email)], limit=1):
            return self._err('email_taken', 409)
        portal = request.env.ref('base.group_portal')
        user = Users.create({
            'name': d.get('name') or email,
            'login': email, 'email': email, 'password': pwd,
            'group_ids': [(6, 0, [portal.id])],
        })
        return self._issue_token(user, d.get('device_name'))

    @http.route(f'{API}/auth/login', type='http', auth='public',
                methods=['POST', 'OPTIONS'], csrf=False)
    def login(self, **kw):
        if self._is_options():
            return self._json({}, 200)
        d = self._body()
        login = (d.get('email') or '').strip().lower()
        pwd = d.get('password') or ''
        try:
            auth = request.env['res.users'].sudo().authenticate(
                {'type': 'password', 'login': login, 'password': pwd}, {})
            uid = auth['uid'] if isinstance(auth, dict) else auth
        except Exception:
            return self._err('invalid_credentials', 401)
        if not uid:
            return self._err('invalid_credentials', 401)
        user = request.env['res.users'].sudo().browse(uid)
        return self._issue_token(user, d.get('device_name'))

    @http.route(f'{API}/auth/forgot-password', type='http', auth='public',
                methods=['POST', 'OPTIONS'], csrf=False)
    def forgot(self, **kw):
        if self._is_options():
            return self._json({}, 200)
        email = (self._body().get('email') or '').strip().lower()
        user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
        if user:
            try:
                user.action_reset_password()
            except Exception:
                pass
        return self._ok({})  # always 200 — don't leak which emails exist

    # ---------------- authenticated endpoints ----------------
    @http.route(f'{API}/me', type='http', auth='public',
                methods=['GET', 'OPTIONS'], csrf=False)
    def me(self, **kw):
        if self._is_options():
            return self._json({}, 200)
        user = self._auth()
        if not user:
            return self._err('unauthorized', 401)
        p = user.partner_id
        return self._ok({'user': {
            'uid': user.id, 'name': user.name, 'email': user.login,
            'partner_id': p.id, 'phone': p.phone, 'email_addr': p.email,
        }})

    @http.route(f'{API}/me/update', type='http', auth='public',
                methods=['POST', 'OPTIONS'], csrf=False)
    def me_update(self, **kw):
        if self._is_options():
            return self._json({}, 200)
        user = self._auth()
        if not user:
            return self._err('unauthorized', 401)
        d = self._body()
        # res.users delegates name/phone/email to its partner (_inherits), so a
        # single sudo write keeps user + partner in sync. We do NOT touch login
        # here — changing the auth identity is a separate, riskier flow.
        vals = {}
        if 'name' in d:
            name = (d.get('name') or '').strip()
            if not name:
                return self._err('missing_fields', 400, 'Name cannot be empty.')
            vals['name'] = name
        if 'phone' in d:
            vals['phone'] = (str(d.get('phone') or '').strip() or False)
        if 'email_addr' in d:
            vals['email'] = (str(d.get('email_addr') or '').strip() or False)
        if vals:
            try:
                user.sudo().write(vals)
            except Exception:
                return self._err('update_failed', 400)
        p = user.partner_id
        return self._ok({'user': {
            'uid': user.id, 'name': user.name, 'email': user.login,
            'partner_id': p.id, 'phone': p.phone, 'email_addr': p.email,
        }})

    @http.route(f'{API}/me/password', type='http', auth='public',
                methods=['POST', 'OPTIONS'], csrf=False)
    def me_password(self, **kw):
        if self._is_options():
            return self._json({}, 200)
        user = self._auth()
        if not user:
            return self._err('unauthorized', 401)
        d = self._body()
        cur = d.get('current_password') or ''
        new = d.get('new_password') or ''
        if len(new) < 6:
            return self._err('weak_password', 400,
                             'New password must be at least 6 characters.')
        # verify the current password before allowing a change
        try:
            auth = request.env['res.users'].sudo().authenticate(
                {'type': 'password', 'login': user.login, 'password': cur}, {})
            uid = auth['uid'] if isinstance(auth, dict) else auth
        except Exception:
            uid = None
        if not uid or uid != user.id:
            return self._err('invalid_credentials', 401,
                             'Current password is incorrect.')
        try:
            user.sudo().write({'password': new})
        except Exception:
            return self._err('update_failed', 400)
        return self._ok({})

    @http.route(f'{API}/pets', type='http', auth='public',
                methods=['GET', 'OPTIONS'], csrf=False)
    def pets(self, **kw):
        if self._is_options():
            return self._json({}, 200)
        user = self._auth()
        if not user:
            return self._err('unauthorized', 401)
        env = request.env(user=user.id)
        animals = env['petnaly.animal'].search(
            [('owner_id', '=', user.partner_id.id)], order='name')
        return self._ok({'pets': [self._pet_brief(a.sudo()) for a in animals]})

    @http.route(f'{API}/pets/<int:pet_id>', type='http', auth='public',
                methods=['GET', 'OPTIONS'], csrf=False)
    def pet_detail(self, pet_id, **kw):
        if self._is_options():
            return self._json({}, 200)
        user = self._auth()
        if not user:
            return self._err('unauthorized', 401)
        env = request.env(user=user.id)
        a = env['petnaly.animal'].search(
            [('id', '=', pet_id), ('owner_id', '=', user.partner_id.id)], limit=1)
        if not a:
            return self._err('not_found', 404)
        return self._ok({'pet': self._pet_detail(a.sudo())})

    @http.route(f'{API}/pets/<int:pet_id>/photo', type='http', auth='public',
                methods=['POST', 'OPTIONS'], csrf=False)
    def pet_photo(self, pet_id, **kw):
        if self._is_options():
            return self._json({}, 200)
        user = self._auth()
        if not user:
            return self._err('unauthorized', 401)
        env = request.env(user=user.id)
        a = env['petnaly.animal'].search(
            [('id', '=', pet_id), ('owner_id', '=', user.partner_id.id)], limit=1)
        if not a:
            return self._err('not_found', 404)
        b64 = (self._body().get('image') or '').strip()
        if b64.startswith('data:') and ',' in b64:
            b64 = b64.split(',', 1)[1]
        if not b64:
            return self._err('missing_image', 400)
        try:
            # write via sudo (portal users are read-only on the animal);
            # ownership is already verified by the search above.
            a.sudo().write({'image_1920': b64})
        except Exception:
            return self._err('invalid_image', 400)
        return self._ok({'pet': self._pet_detail(a.sudo())})

    @http.route(f'{API}/documents/<int:doc_id>/download', type='http', auth='public',
                methods=['GET', 'OPTIONS'], csrf=False)
    def document_download(self, doc_id, **kw):
        if self._is_options():
            return self._json({}, 200)
        user = self._auth()
        if not user:
            return self._err('unauthorized', 401)
        env = request.env(user=user.id)
        doc = env['petnaly.document'].search([('id', '=', doc_id)], limit=1)
        if not doc or not doc.file:
            return self._err('not_found', 404)
        data = base64.b64decode(doc.sudo().file)
        return Response(
            data, status=200,
            content_type='application/octet-stream',
            headers=[
                ('Content-Disposition',
                 'attachment; filename="%s"' % (doc.file_name or 'document')),
                *CORS.items(),
            ],
        )

    # ---------------- knowledge base ----------------
    def _kb_brief(self, a):
        labels = dict(a._fields['category'].selection)
        return {
            'id': a.id,
            'title': a.name,
            'subtitle': a.subtitle or None,
            'category': a.category,
            'category_label': labels.get(a.category, a.category),
            'breed': a.breed_id.name if a.breed_id else None,
            'breed_id': a.breed_id.id if a.breed_id else None,
            'summary': a.summary or None,
            'reading_minutes': a.reading_minutes,
            'date': a.date_published or None,
            'cover': self._img(a.image_256),
            'tags': a.tag_ids.mapped('name'),
        }

    def _kb_detail(self, a):
        d = self._kb_brief(a)
        d['cover'] = self._img(a.image_512 or a.image_256)
        d['body'] = a.body or ''
        return d

    @http.route(f'{API}/kb', type='http', auth='public',
                methods=['GET', 'OPTIONS'], csrf=False)
    def kb_list(self, **kw):
        if self._is_options():
            return self._json({}, 200)
        user = self._auth()
        if not user:
            return self._err('unauthorized', 401)
        Article = request.env['petnaly.kb.article'].sudo()
        domain = [('published', '=', True)]
        if kw.get('category'):
            domain.append(('category', '=', kw['category']))
        if kw.get('breed_id'):
            try:
                domain.append(('breed_id', '=', int(kw['breed_id'])))
            except (TypeError, ValueError):
                pass
        # ?mine=1 -> articles for the breeds the user actually owns (+ general)
        if kw.get('mine') and 'breed_id' in request.env['petnaly.animal']._fields:
            env = request.env(user=user.id)
            pets = env['petnaly.animal'].search(
                [('owner_id', '=', user.partner_id.id)])
            breed_ids = pets.sudo().mapped('breed_id').ids
            if breed_ids:
                domain = [('published', '=', True), '|',
                          ('breed_id', 'in', breed_ids), ('breed_id', '=', False)]
        arts = Article.search(domain, limit=100)
        return self._ok({'articles': [self._kb_brief(a) for a in arts]})

    @http.route(f'{API}/kb/<int:article_id>', type='http', auth='public',
                methods=['GET', 'OPTIONS'], csrf=False)
    def kb_detail(self, article_id, **kw):
        if self._is_options():
            return self._json({}, 200)
        user = self._auth()
        if not user:
            return self._err('unauthorized', 401)
        a = request.env['petnaly.kb.article'].sudo().search(
            [('id', '=', article_id), ('published', '=', True)], limit=1)
        if not a:
            return self._err('not_found', 404)
        return self._ok({'article': self._kb_detail(a)})
