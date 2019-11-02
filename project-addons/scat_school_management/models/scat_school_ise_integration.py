# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from zeep import Client
from lxml import objectify
from datetime import datetime


class ResCompany(models.Model):

    _inherit = "res.company"

    ise_login = fields.Char("Usuario ISE")
    ise_password = fields.Char(u"Contraseña ISE")
    ise_payment_mode_id = fields.Many2one("account.payment.mode",
                                          "Modo de pago por defecto")
    ise_fiscal_position_id = fields.Many2one("account.fiscal.position",
                                             "Posición fiscal por defecto")


class ScatSchoolIseIntegration(models.Model):

    _name = "scat.school.ise.integration"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = "call_date"
    _order = "call_date desc"

    call_date = fields.Datetime(u"Fecha de conexión", required=True,
                                default=fields.Datetime.now)
    end_date = fields.Datetime(u"Fecha de finalización",
                               default=fields.Datetime.now)
    fail = fields.Boolean("Error")
    token = fields.Char("Token", readonly=True)
    operation = fields.Char(u"Operación", required=True)
    company_id = fields.Many2one("res.company", u"Compañía", readonly=True,
                                 default=lambda s: s.env.user.company_id.id)

    @api.multi
    def _get_pricelist_item(self, child):
        if child.BONIFICACIONISE:
            pricelist_item = self.env['product.pricelist.item'].\
                search([('percent_price', '=', child.BONIFICACIONISE)],
                       limit=1)
        else:
            pricelist_item = self.env['product.pricelist.item'].\
                search([('percent_price', '=', False)], limit=1)
        if not pricelist_item:
            self.message_post(body=u"Cree una tarifa de venta con una "
                              u"bonificación de %s." %
                              str(child.BONIFICACIONISE),
                              message_type='comment')
        return pricelist_item

    @api.multi
    def _get_parent_vals(self, child, exp):
        return {'x_ise_estado': 'titular',
                'is_company': True,
                'company_id': False,
                'customer': True,
                'street': child.DIRECCION,
                'zip': child.CP,
                'city': child.MUNICIPIO,
                'state_id':
                (child.CP and self.env['res.better.zip'].
                 search([('name', '=', child.CP)])) and
                self.env['res.better.zip'].
                search([('name', '=', child.CP)])[0].state_id.id or False,
                'x_ise_nie': child.NIFTITULAR,
                'property_account_position_id':
                exp.company_id.ise_fiscal_position_id.id,
                'customer_payment_mode_id':
                exp.company_id.ise_payment_mode_id.id,
                'phone': child.TELEFONO,
                'email': child.EMAIL,
                'name': child.APELLIDOSTITULAR and
                tools.ustr(child.APELLIDOSTITULAR) + u", " +
                child.NOMBRETITULAR or child.NOMBRETITULAR}

    @api.multi
    def _set_acc_number(self, parent, child_data, country, exp):
        acc_number = str(child_data.CUENTABANCARIA).replace("-", "")
        bank = self.env['res.partner.bank'].\
            search([('acc_number', '=', acc_number),
                    ('partner_id', '=', parent.id),
                    '|', ('company_id', '=', exp.company_id.id),
                    ('company_id', '=', False)])
        today = fields.Date.today()
        if child_data.FECHADESDESERVICIO:
            start_date = datetime.\
                strptime(str(child_data.FECHADESDESERVICIO),
                         '%d/%m/%Y').strftime('%Y-%m-%d')
            if start_date > today:
                start_date = today
        else:
            start_date = today

        if not bank:
            if not parent.not_modify_bank_data:
                mandates = self.env['account.banking.mandate'].\
                    search([('partner_id', '=', parent.id),
                            ('state', 'in', ['draft', 'valid'])])
                if mandates:
                    mandates.cancel()
                    self.message_post(body=u"Se ha cancelado un mandato para "
                                      u"empresa %s por cambio de cuenta. "
                                      u"De %s a %s. "
                                      u"Revisad los efectos pendientes de "
                                      u"remesar." %
                                      (parent.name,
                                       mandates[0].partner_bank_id.acc_number,
                                       acc_number),
                                      message_type='comment')
            bank_vals = {'acc_number': acc_number,
                         'partner_id': parent.id,
                         'company_id': False,
                         'acc_country_id': country and country.id or False}
            bank = self.env['res.partner.bank'].create(bank_vals)
            bank._onchange_acc_number_l10n_es_partner()
            mandate = self.env['account.banking.mandate'].\
                create({'company_id': exp.company_id.id,
                        'format': 'sepa',
                        'partner_bank_id': bank.id,
                        'scheme': 'CORE',
                        'recurrent_sequence_type': 'recurring',
                        'type': 'recurrent',
                        'signature_date': start_date})
            mandate.validate()
            if parent.not_modify_bank_data:
                self.message_post(body=u"Se iba a cancelar un mandato para la "
                                       u"empresa %s por cambio de cuenta. "
                                       u"Pero no se ha hecho por que no se "
                                       u"permiten los cambios. La nueva cuenta"
                                       u" sería %s." %
                                       (parent.name, acc_number),
                                  message_type='notification')
        else:
            if not parent.not_modify_bank_data:
                mandates = self.env['account.banking.mandate'].\
                    search([('partner_id', '=', parent.id),
                            ('state', 'in', ['valid']),
                            ('company_id', '=', exp.company_id.id)])
                if not mandates:
                    mandate = self.env['account.banking.mandate'].\
                        create({'company_id': exp.company_id.id,
                                'format': 'sepa',
                                'partner_bank_id': bank[0].id,
                                'scheme': 'CORE',
                                'recurrent_sequence_type': 'recurring',
                                'type': 'recurrent',
                                'signature_date': start_date})
                    mandate.validate()

    @api.multi
    def _try_write_vat(self, parent, country, vat):
        if vat:
            try:
                parent.write({'vat': (country and country.code or u"ES") +
                              str(vat).replace("-", "")})
            except Exception:
                self.message_post(body=u"NIF %s no válido para el titular %s" %
                                  ((country and country.code or u"ES") +
                                   str(vat).replace("-", ""),
                                   parent.name), message_type='notification')
                parent.vat = False
        else:
            self.message_post(body=u"En el ISE no figura el nif para el "
                                   u"titular %s" % parent.name,
                              message_type='notification')

    @api.multi
    def _update_parent_data(self, parent, child_data, exp):
        update_vals = {}
        if not parent.phone:
            update_vals['phone'] = child_data.TELEFONO
        if not parent.email:
            update_vals['email'] = child_data.EMAIL
        if update_vals:
            parent.with_context(force_company=exp.company_id.id).\
                write(update_vals)

    @api.multi
    def _create_student_school(self, child, child_data, school, exp,
                               start_date):
        school_vals = {'start_date': start_date,
                       'school_id': school.id,
                       'company_name': exp.company_id.name,
                       'student_id': child.id}
        if child_data.FECHAHASTASERVICIO:
            end_date = datetime.strptime(str(child_data.FECHAHASTASERVICIO),
                                         '%d/%m/%Y').strftime('%Y-%m-%d')
            if end_date <= fields.Date.today():
                school_vals['end_date'] = end_date
        self.env['scat.school.student'].create(school_vals)

    @api.multi
    def _update_child_data(self, child, child_data):
        update_vals = {}
        if child_data.NIVELEDUCATIVO and self.env['scat.course'].\
                search([('name', 'ilike',
                         tools.ustr(child_data.NIVELEDUCATIVO))]):
            course = self.env['scat.course'].\
                search([('name', 'ilike',
                         tools.ustr(child_data.NIVELEDUCATIVO))])[0]
            if child.course_id.id != course.id:
                update_vals['course_id'] = course.id
        if child.x_ise_estado != str(child_data.ESTADO).lower():
            update_vals['x_ise_estado'] = str(child_data.ESTADO).lower()
        if update_vals:
            child.write(update_vals)

    @api.multi
    def check_child_data(self, child_data, child, school, exp):
        if child_data.FECHADESDESERVICIO:
            start_date = datetime.\
                strptime(str(child_data.FECHADESDESERVICIO),
                         '%d/%m/%Y').strftime('%Y-%m-%d')
        else:
            start_date = datetime.\
                strptime(str(child_data.FECHADESDEMATRICULA),
                         '%d/%m/%Y').strftime('%Y-%m-%d')
        schools = self.env['scat.school.student'].\
            search([('student_id', '=', child.id),
                    ('school_id', '=', school.id),
                    ('start_date', '=', start_date)])
        open_schools = child.school_ids.filtered(lambda x: not x.end_date)
        send = False
        if not schools:
            if open_schools:
                for oschool in open_schools:
                    if oschool.school_id.id != school.id or \
                            not child.not_update_date:
                        oschool.write({'end_date': start_date})
                        if not send:
                            self.\
                                message_post(body=u"Se ha finalizado un "
                                                  u"colegio para el niño %s "
                                                  u"por cambio de colegio "
                                                  u"o fechas. Revisad el "
                                                  u"control de presencia "
                                                  u"actual y cread el nuevo"
                                                  % child.name,
                                             message_type='comment')
                            send = True
            if not open_schools or send:
                self._create_student_school(child, child_data, school, exp,
                                            start_date)
        elif child_data.FECHAHASTASERVICIO and open_schools:
            end_date = datetime.\
                strptime(str(child_data.FECHAHASTASERVICIO),
                         '%d/%m/%Y').strftime('%Y-%m-%d')
            if end_date <= fields.Date.today():
                open_schools.write({'end_date': end_date})

        pricelist_item = self._get_pricelist_item(child_data)
        if not pricelist_item:
            self.fail = True
            return
        if child_data.CUENTABANCARIA:
            country = self.env['res.country'].\
                search([('code', '=', str(child_data.CUENTABANCARIA)[:2])],
                       limit=1)
            country = country and country[0] or False
        else:
            country = False

        if not child.not_update_parent:
            if child_data.NIFTITULAR and child_data.NOMBRETITULAR:
                parent = self.env['res.partner'].\
                    search([('x_ise_nie', '=', child_data.NIFTITULAR)])
                if parent:
                    if parent[0].id != child.parent_id.id:
                        child.with_context(force_company=exp.company_id.id).\
                            parent_id = parent[0].id
                    parent = parent[0]
                    self._update_parent_data(parent, child_data, exp)
                    parent_comp = self.env['res.partner'].\
                        with_context(force_company=exp.company_id.id).\
                        browse(parent.id)
                    if pricelist_item.pricelist_id.id != \
                            parent_comp.property_product_pricelist.id:
                        old_name = parent_comp.property_product_pricelist.name
                        parent_comp.property_product_pricelist = \
                            pricelist_item.pricelist_id.id
                        self.\
                            message_post(body=u"Se ha actualizado la "
                                              u"bonificación para el niño %s "
                                              u"de %s a %s desde el ISE, "
                                              u"revisad su facturación."
                                              % (child.name, old_name,
                                                 pricelist_item.pricelist_id.
                                                 name),
                                         message_type='notification')
                    if not parent_comp.customer_payment_mode_id:
                        parent_comp.customer_payment_mode_id = \
                            exp.company_id.ise_payment_mode_id.id
                    if parent_comp.property_account_position_id.id != \
                            exp.company_id.ise_fiscal_position_id.id:
                        parent_comp.property_account_position_id = \
                            exp.company_id.ise_fiscal_position_id.id
                else:
                    parent_vals = self._get_parent_vals(child_data, exp)
                    parent_vals['property_product_pricelist'] = \
                        pricelist_item.pricelist_id.id
                    parent_vals['country_id'] = country and country.id or False
                    parent = self.env['res.partner'].\
                        with_context(force_company=exp.company_id.id).\
                        create(parent_vals)
                    child.with_context(force_company=exp.company_id.id).\
                        parent_id = parent.id
                    self._try_write_vat(parent, country, child_data.NIFTITULAR)

                if child_data.CUENTABANCARIA:
                    self._set_acc_number(parent, child_data, country, exp)
            else:
                child_comp = self.env['res.partner'].\
                    with_context(force_company=exp.company_id.id).\
                    browse(child.id)
                if pricelist_item.pricelist_id.id != \
                        child_comp.property_product_pricelist.id:
                    old_name = child_comp.property_product_pricelist.name
                    child_comp.property_product_pricelist = \
                        pricelist_item.pricelist_id.id
                    self.\
                        message_post(body=u"Se ha actualizado la bonificación "
                                          u"para el niño %s de %s a %s desde "
                                          u"el ISE, revisad su facturación."
                                          % (child.name, old_name,
                                             pricelist_item.pricelist_id.name),
                                     message_type='notification')
                if child_data.CUENTABANCARIA:
                    self._set_acc_number(child, child_data, country, exp)
        self._update_child_data(child, child_data)

    @api.multi
    def create_new_child(self, child, school, exp):
        pricelist_item = self._get_pricelist_item(child)
        if not pricelist_item:
            self.fail = True
            return
        if child.CUENTABANCARIA:
            country = self.env['res.country'].\
                search([('code', '=', str(child.CUENTABANCARIA)[:2])],
                       limit=1)
            country = country and country[0] or False
        else:
            country = False

        if child.NIFTITULAR and child.NOMBRETITULAR:
            parent = self.env['res.partner'].search([('x_ise_nie', '=',
                                                      child.NIFTITULAR)])

            if parent:
                parent = parent[0]
                self._update_parent_data(parent, child, exp)
            else:
                parent_vals = self._get_parent_vals(child, exp)
                parent_vals['property_product_pricelist'] = \
                    pricelist_item.pricelist_id.id
                parent_vals['country_id'] = country and country.id or False
                parent = self.env['res.partner'].\
                    with_context(force_company=exp.company_id.id).\
                    create(parent_vals)
                self._try_write_vat(parent, country, child.NIFTITULAR)

            if child.CUENTABANCARIA:
                self._set_acc_number(parent, child, country, exp)

        child_vals = {'x_ise_nie': child.NIE,
                      'x_ise_estado': str(child.ESTADO).lower(),
                      'comensal_type': 'A',
                      'company_id': False,
                      'y_ise_factura_aut': True,
                      'y_ise_l': True,
                      'y_ise_m': True,
                      'y_ise_x': True,
                      'y_ise_j': True,
                      'y_ise_v': True,
                      'name': tools.ustr(child.APELLIDOS) + u", " +
                      child.NOMBRE,
                      'course_id': (child.NIVELEDUCATIVO and
                                    self.env['scat.course'].
                                    search([('name', 'ilike',
                                             tools.
                                             ustr(child.NIVELEDUCATIVO))])) and
                      self.env['scat.course'].
                      search([('name', 'ilike',
                               tools.ustr(child.NIVELEDUCATIVO))])[0].id
                      or False}
        if child.NIFTITULAR:
            child_vals['parent_id'] = parent.id
        else:
            child_vals.update({'street': child.DIRECCION,
                               'zip': child.CP,
                               'city': child.MUNICIPIO,
                               'state_id':
                               (child.CP and self.env['res.better.zip'].
                                search([('name', '=', child.CP)])) and
                               self.env['res.better.zip'].
                               search([('name', '=', child.CP)])[0].
                               state_id.id or False,
                               'is_company': True,
                               'customer': True,
                               'phone': child.TELEFONO,
                               'email': child.EMAIL,
                               'property_account_position_id':
                               exp.company_id.ise_fiscal_position_id.id,
                               'customer_payment_mode_id':
                               exp.company_id.ise_payment_mode_id.id,
                               'property_product_pricelist':
                               pricelist_item.pricelist_id.id,
                               'country_id': country and country.id or False})
        child_partner = self.env['res.partner'].\
            with_context(force_company=exp.company_id.id).create(child_vals)
        if not child.NIFTITULAR:
            self._set_acc_number(child_partner, child, country, exp)
        self.message_post(body=u"Se ha creado un nuevo niño %s con NIE %s."
                               % (child_partner.name, child_partner.x_ise_nie),
                          message_type='notification')

        if child.FECHADESDESERVICIO:
            start_date = datetime.\
                strptime(str(child.FECHADESDESERVICIO),
                         '%d/%m/%Y').strftime('%Y-%m-%d')
        else:
            start_date = datetime.\
                strptime(str(child.FECHADESDEMATRICULA),
                         '%d/%m/%Y').strftime('%Y-%m-%d')
        self._create_student_school(child_partner, child, school, exp,
                                    start_date)

    @api.multi
    def _login_ise(self, client):
        token = client.service.loginISE(self.company_id.ise_login,
                                        self.company_id.ise_password,
                                        self.company_id.vat.replace("ES", ""))
        return token

    @api.multi
    def action_ise_load_childs(self, init_date):
        self.ensure_one()
        ise_url = self.env['ir.config_parameter'].\
            get_param('ise.webservice.url')
        client = Client(ise_url)
        token = self._login_ise(client)
        if not token:
            self.respose = u"Error de conexión"
            return
        self.token = token
        expedients = self.env["scat.expediente"].search([('company_id', '=',
                                                          self.company_id.id),
                                                         ('state', '=',
                                                          'open')])
        for exp in expedients:
            for school in exp.school_ids:
                cont = created = updated = 0
                child_data = client.service.infoAlumnos(exp.n_expediente,
                                                        exp.n_lote,
                                                        school.code,
                                                        token)
                xml = objectify.fromstring(child_data.encode('utf-8'))
                if xml.ERROR and "ERR-0" in str(xml.ERROR):
                    token = self._login_ise(client)
                    self.token = token
                    child_data = client.service.\
                        infoAlumnos(exp.n_expediente,
                                    exp.n_lote,
                                    school.code,
                                    token)
                    xml = objectify.fromstring(child_data.encode('utf-8'))
                if xml.ERROR:
                    self.fail = True
                    self.message_post(body=u"Error %s: procesando el colegio "
                                      u"%s para el expediente %s." %
                                      (xml.ERROR, school.name,
                                       exp.display_name),
                                      message_type='comment')
                elif not xml.ALUMNOS:
                    self.message_post(body=u"No se han encontrado niños "
                                           u"para el colegio %s." %
                                      school.name,
                                      message_type='comment')
                    continue
                else:
                    for child in xml.ALUMNOS.ALUMNODTO:
                        if init_date and child.FECHADESDESERVICIO:
                            start_date = datetime.\
                                strptime(str(child.FECHADESDESERVICIO),
                                         '%d/%m/%Y').strftime('%Y-%m-%d')
                            if start_date < init_date:
                                continue
                        cont += 1
                        exists = self.env["res.partner"].\
                            search([('x_ise_nie', '=', child.NIE)])
                        if not exists:
                            self.create_new_child(child, school, exp)
                            created += 1
                        else:
                            self.check_child_data(child, exists[0], school,
                                                  exp)
                            updated += 1
                    self.message_post(body=u"Para el colegio %s se han leído "
                                           u"%s niños, %s se han creado y"
                                           u" %s se han actualizado." %
                                      (school.name, cont, created, updated),
                                      message_type='comment')
        self.end_date = fields.Datetime.now()

    @api.multi
    def create_new_professor(self, professor, school, exp):
        pricelist_item = self._get_pricelist_item(professor)
        if not pricelist_item:
            self.fail = True
            return
        prof_vals = {'x_ise_nie': professor.DNI,
                     'x_ise_estado': 'usuario',
                     'is_company': True,
                     'customer': True,
                     'comensal_type': str(professor.ORIGEN),
                     'company_id': False,
                     'name': professor.APELLIDOS + u", " + professor.NOMBRE,
                     'phone': professor.TELEFONO,
                     'y_ise_factura_aut': True,
                     'y_ise_l': True,
                     'y_ise_m': True,
                     'y_ise_x': True,
                     'y_ise_j': True,
                     'y_ise_v': True,
                     'property_account_position_id':
                     exp.company_id.ise_fiscal_position_id.id,
                     'customer_payment_mode_id':
                     exp.company_id.ise_payment_mode_id.id,
                     'property_product_pricelist':
                     pricelist_item.pricelist_id.id}
        prof_partner = self.env['res.partner'].\
            with_context(force_company=exp.company_id.id).create(prof_vals)
        self.message_post(body=u"Se ha creado un nuevo profesor %s con DNI %s."
                               % (prof_partner.name, prof_partner.x_ise_nie),
                          message_type='notification')
        self._try_write_vat(prof_partner, False, professor.DNI)
        start_date = datetime.\
            strptime(str(professor.FECHADESDESERVICIO),
                     '%d/%m/%Y').strftime('%Y-%m-%d')
        self._create_student_school(prof_partner, professor, school, exp,
                                    start_date)

    @api.multi
    def check_professor_data(self, prof_data, professor, school, exp):
        start_date = datetime.\
            strptime(str(prof_data.FECHADESDESERVICIO),
                     '%d/%m/%Y').strftime('%Y-%m-%d')
        schools = self.env['scat.school.student'].\
            search([('student_id', '=', professor.id),
                    ('school_id', '=', school.id),
                    ('start_date', '=', start_date)])
        open_schools = professor.school_ids.filtered(lambda x: not x.end_date)
        send = False
        if not schools:
            if open_schools:
                for oschool in open_schools:
                    if oschool.school_id.id != school.id or \
                            not professor.not_update_date:
                        oschool.write({'end_date': start_date})
                        if not send:
                            self.\
                                message_post(body=u"Se ha finalizado un "
                                                  u"colegio para el profesor "
                                                  u"%s por cambio de colegio "
                                                  u"o fechas. Revisad el "
                                                  u"control de presencia "
                                                  u"actual y cread el nuevo"
                                                  % professor.name,
                                             message_type='comment')
                            send = True
            if not open_schools or send:
                self._create_student_school(professor, prof_data, school, exp,
                                            start_date)
        elif prof_data.FECHAHASTASERVICIO and open_schools:
            end_date = datetime.strptime(str(prof_data.FECHAHASTASERVICIO),
                                         '%d/%m/%Y').strftime('%Y-%m-%d')
            if end_date <= fields.Date.today():
                open_schools.write({'end_date': end_date})

        pricelist_item = self._get_pricelist_item(prof_data)
        if not pricelist_item:
            self.fail = True
            return
        professor_comp = self.env['res.partner'].\
            with_context(force_company=exp.company_id.id).browse(professor.id)
        if pricelist_item.pricelist_id.id != \
                professor_comp.property_product_pricelist.id:
            old_name = professor_comp.property_product_pricelist.name
            professor_comp.property_product_pricelist = \
                pricelist_item.pricelist_id.id
            self.message_post(body=u"Se ha actualizado la bonificación %s a %s"
                                   u" para el profesor %s desde el ISE, "
                                   u"revisad su facturación."
                                   % (old_name,
                                      pricelist_item.pricelist_id.name,
                                      professor.name),
                                   message_type='notification')
        update_vals = {}
        if not professor.phone:
            update_vals['phone'] = prof_data.TELEFONO
        if not professor.is_company:
            update_vals['is_company'] = True
        if professor.x_ise_estado != 'usuario':
            update_vals['x_ise_estado'] = 'usuario'
        if professor.comensal_type != prof_data.ORIGEN:
            update_vals['comensal_type'] = prof_data.ORIGEN
        if update_vals:
            professor.write(update_vals)

    @api.multi
    def action_ise_load_professors(self, init_date=False):
        self.ensure_one()
        ise_url = self.env['ir.config_parameter'].\
            get_param('ise.webservice.url')
        client = Client(ise_url)
        token = self._login_ise(client)
        if not token:
            self.respose = u"Error de conexión"
            return
        self.token = token
        expedients = self.env["scat.expediente"].search([('company_id', '=',
                                                          self.company_id.id),
                                                         ('state', '=',
                                                          'open')])
        for exp in expedients:
            for school in exp.school_ids:
                cont = created = updated = 0
                prof_data = client.service.infoDirectores(exp.n_expediente,
                                                          exp.n_lote,
                                                          school.code,
                                                          token)
                xml = objectify.fromstring(prof_data.encode('utf-8'))
                if xml.ERROR and "ERR-0" in str(xml.ERROR):
                    token = self._login_ise(client)
                    self.token = token
                    prof_data = client.service.\
                        infoDirectores(exp.n_expediente,
                                       exp.n_lote,
                                       school.code,
                                       token)
                    xml = objectify.fromstring(prof_data.encode('utf-8'))
                if xml.ERROR:
                    self.fail = True
                    self.message_post(body=u"Error %s: procesando el "
                                           u"colegio %s para el "
                                           u"expediente %s." %
                                      (xml.ERROR, school.name,
                                       exp.display_name),
                                      message_type='comment')
                elif not xml.COMENSALES:
                    self.message_post(body=u"No se han encontrado profesores "
                                           u"para el colegio %s." %
                                      school.name,
                                      message_type='comment')
                    continue
                else:
                    for professor in xml.COMENSALES.COMENSALDTO:
                        if init_date:
                            start_date = datetime.\
                                strptime(str(professor.FECHADESDESERVICIO),
                                         '%d/%m/%Y').strftime('%Y-%m-%d')
                            if start_date < init_date:
                                continue
                        cont += 1
                        exists = self.env["res.partner"].\
                            search([('x_ise_nie', '=', professor.DNI)])
                        if not exists:
                            self.create_new_professor(professor, school, exp)
                            created += 1
                        else:
                            self.check_professor_data(professor, exists[0],
                                                      school, exp)
                            updated += 1
                    self.message_post(body=u"Para el colegio %s se han leído "
                                           u"%s profesores, %s se han creado y"
                                           u" %s se han actualizado." %
                                      (school.name, cont, created, updated),
                                      message_type='comment')
        self.end_date = fields.Datetime.now()

    @api.model
    def action_sync_children(self, init_date=False):
        companies = self.env["res.company"].\
            search([('ise_login', '!=', False)])
        for company in companies:
            rec = self.create({'company_id': company.id,
                               'operation': "infoAlumnos"})
            rec.action_ise_load_childs(init_date)

    @api.model
    def action_sync_professor(self, init_date=False):
        companies = self.env["res.company"].\
            search([('ise_login', '!=', False)])
        for company in companies:
            rec = self.create({'company_id': company.id,
                               'operation': "infoDirectores"})
            rec.action_ise_load_professors(init_date)
