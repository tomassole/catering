# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
from datetime import datetime


class ScatMenuType(models.Model):

    _name = "scat.menu.type"

    name = fields.Char("Nombre", size=80, required=True)
    conflict_allergens_ids = fields.Many2many('scat.allergens',
                                              string=u"Alérgenos conflictivos")


class ScatMenuConfig(models.Model):

    _name = "scat.menu.config"

    name = fields.Char("Nombre", size=140, required=True,
                       states={'done': [('readonly', False)]})
    menu_line_ids = fields.One2many('scat.menu.config.line', "menu_config_id",
                                    "Lineas", copy=True,
                                    states={'done': [('readonly', False)]})
    state = fields.Selection([('draft', 'Borrador'), ('open', 'En progreso'),
                              ('done', 'Terminado')], "Estado", required=True,
                             default="draft", readonly=True)

    @api.multi
    def action_open(self):
        self.state = 'open'

    @api.multi
    def action_done(self):
        self.state = 'done'


class ScatMenuConfigLine(models.Model):

    _name = "scat.menu.config.line"
    _order = "sequence asc"

    product_id = fields.Many2one('product.product', 'Plato',
                                 domain=[('type', '!=', 'service')])
    name = fields.Char("Nombre", size=140, required=True)
    mtype_ids = fields.Many2many('scat.menu.type', string="Tipos",
                                 required=True)
    mode = fields.Selection([('fst_course', 'Primer plato'),
                             ('scnd_course', 'Segundo plato'),
                             ('garniture', u'Guarnición'),
                             ('bread', 'Pan'), ('dessert', 'Postre'),
                             ('drink', 'Bebida')],
                            'Momento', required=True)
    product_qty = fields.Float("Cant.", required=True, default=1.0)
    menu_config_id = fields.Many2one('scat.menu.config', u"Menú")
    sequence = fields.Integer("Sequence", default=1)

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name

    @api.constrains('product_id', 'mtype_ids')
    def _check_allergens(self):
        for line in self:
            if line.product_id and line.product_id.allergens_ids:
                for typ in line.mtype_ids.filtered('conflict_allergens_ids'):
                    res = set(typ.conflict_allergens_ids.ids).\
                        intersection(line.product_id.allergens_ids.ids)
                    if res:
                        raise exceptions.\
                            ValidationError(u"Este plato %s es incompatible "
                                            u"con el tipo de menú, revise "
                                            u"los alérgenos." %
                                            line.product_id.name)

    @api.constrains('mode', 'mtype_ids')
    def _check_mode_mtype_config(self):
        for line in self:
            if line.menu_config_id:
                for mtype in line.mtype_ids:
                    res = self.search([('menu_config_id', '=',
                                        line.menu_config_id.id),
                                       ('id', '!=', line.id),
                                       ('mode', '=', line.mode),
                                       ('mtype_ids', 'in', [mtype.id])])
                    if res:
                        raise exceptions.\
                            ValidationError(u"No se puede repetir el tipo de "
                                            u"menú para el mismo momento")


class ScatMenuRotative(models.Model):

    _name = "scat.menu.rotative"

    name = fields.Char("Nombre", required=True,
                       states={'done': [('readonly', False)]})
    line_ids = fields.One2many("scat.menu.rotative.line", "rotative_id",
                               u"Menús", copy=True,
                               states={'done': [('readonly', False)]})
    last_created_menu_id = fields.Many2one('scat.menu', u"Últ. menú",
                                           compute="_get_last_menu_data")
    last_created_menu_sequence = fields.Integer(u"Últ. secuencia menú",
                                                compute="_get_last_menu_data")
    start_date = fields.Date("Fecha de inicio", required=True,
                             states={'done': [('readonly', False)]})
    end_date = fields.Date("Fecha de fin", copy=False,
                           states={'done': [('readonly', False)]})
    state = fields.Selection([('draft', 'Borrador'), ('open', 'En progreso'),
                              ('done', 'Finalizado')], "Estado", required=True,
                             readonly=True, default="draft")

    @api.multi
    def action_open(self):
        self.state = 'open'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def _get_last_menu_data(self):
        for rotative in self:
            last_menu = self.env['scat.menu'].\
                search([('rotative_line_id', 'in',
                         rotative.line_ids.ids)], limit=1)
            if last_menu:
                rotative.last_created_menu_id = last_menu.id
                rotative.last_created_menu_sequence = \
                    last_menu.rotative_line_id.sequence

    @api.model
    def _get_dates_between(self, holidays):
        lista_festivos = set()

        for holiday in holidays:
            start_date = datetime.strptime(holiday.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(holiday.end_date, "%Y-%m-%d")
            lista_fechas = [start_date + relativedelta(days=d)
                            for d in range((end_date - start_date).days + 1)]

            lista_festivos.update(lista_fechas)

        return list(lista_festivos)

    @api.model
    def _generate_menus(self, weeks=4, start_date=False):
        def next_sequence():
            line = self.env['scat.menu.rotative.line'].\
                search([('sequence', '>', last_sequence),
                        ('rotative_id', '=', rotative.id)], limit=1)
            if line:
                return line
            else:
                line = self.env['scat.menu.rotative.line'].\
                    search([('rotative_id', '=', rotative.id)], limit=1)
                return line

        if not start_date:
            today = datetime.now()
        else:
            today = datetime.strptime(start_date, '%Y-%m-%d')
        next_month = today + relativedelta(weeks=weeks)
        rotatives = self.search([('state', '=', 'open'),
                                 ('start_date', '<=',
                                  next_month.strftime("%Y-%m-%d")),
                                 '|', ('end_date', '=', False),
                                 ('end_date', '>=',
                                  today.strftime("%Y-%m-%d"))])
        for rotative in rotatives:
            if rotative.last_created_menu_id:
                last_date = rotative.last_created_menu_id.date
                last_sequence = rotative.last_created_menu_sequence
            else:
                last_date = (datetime.strptime(rotative.start_date,
                                               '%Y-%m-%d') -
                             relativedelta(days=1)).strftime("%Y-%m-%d")
                last_sequence = 0
            final_date = next_month.strftime("%Y-%m-%d")
            if rotative.end_date and final_date > rotative.end_date:
                final_date = rotative.end_date
            national_holidays = self.env['scat.holidays'].\
                search([('holiday_type', '=', 'nacional'),
                        ('end_date', '>=', last_date),
                        ('start_date', '<=', final_date)])
            lista_festivos = self._get_dates_between(national_holidays)
            while last_date < final_date:
                last_date = datetime.strptime(last_date, '%Y-%m-%d') + \
                    relativedelta(days=1)
                if last_date.weekday() < 5 and last_date not in lista_festivos:
                    next_line = next_sequence()
                    last_sequence = next_line.sequence
                    last_date = last_date.strftime("%Y-%m-%d")
                    menu = self.env['scat.menu'].\
                        create({'name': u"[%s] %s" %
                                (next_line.rotative_id.name,
                                 next_line.menu_id.name),
                                'date': last_date,
                                'menu_config_id': next_line.menu_id.id,
                                'state': 'confirmed',
                                'rotative_line_id': next_line.id})
                    menu.load_lines()
                else:
                    last_date = last_date.strftime("%Y-%m-%d")


class ScatMenuRotativeLine(models.Model):

    _name = "scat.menu.rotative.line"
    _order = "sequence asc"

    menu_id = fields.Many2one('scat.menu.config', "Menú", required=True,
                              domain=[('state', '=', 'open')])
    sequence = fields.Integer("Secuencia", required=True, default=1)
    rotative_id = fields.Many2one('scat.menu.rotative', 'Rotativo')

    _sql_constraints = [('rotative_seq_unique',
                         'UNIQUE(rotative_id, sequence)',
                         "Las secuencias no pueden repetirse")]

    @api.multi
    def open_menu_history(self):
        self.ensure_one()
        action = self.env.ref('scat_menu.scat_menu_act').read()[0]
        action['domain'] = [('rotative_line_id', '=', self.id)]
        return action

    @api.model
    def default_get(self, fields=None):
        defaults = super(ScatMenuRotativeLine, self).default_get(fields)
        sequence = 0
        if self.env.context.get('line_ids'):
            for rec in self.env.context['line_ids']:
                if rec[1]:
                    rec_o = self.browse(rec[1])
                    if rec_o.sequence > sequence:
                        sequence = rec_o.sequence
                elif rec[2].get('sequence'):
                    if rec[2]['sequence'] > sequence:
                        sequence = rec[2]['sequence']
            defaults['sequence'] = sequence + 1
        return defaults


class ScatMenu(models.Model):

    _name = "scat.menu"
    _order = "date desc"

    name = fields.Char("Nombre", required=True)
    date = fields.Date("Fecha", required=True)
    menu_config_id = fields.Many2one('scat.menu.config', 'Config.',
                                     required=True)
    state = fields.Selection([('draft', 'Borrador'),
                              ('confirmed', 'Confirmado')], "Estado",
                             readonly=True, required=True, default="draft")
    menu_line_ids = fields.One2many("scat.menu.line", "menu_id", u"Menús",
                                    copy=True)
    rotative_line_id = fields.Many2one('scat.menu.rotative.line', "Rotativo")

    @api.multi
    def action_confirm(self):
        self.state = "confirmed"

    @api.multi
    def load_lines(self):
        for menu in self:
            lines = self.env['scat.menu.config.line'].\
                search([('menu_config_id', '=', menu.menu_config_id.id)])
            lines_data = lines.read([], load='_classic_write')
            for dt in lines_data:
                del dt['id']
                del dt['menu_config_id']
                dt['menu_id'] = menu.id
                dt['mtype_ids'] = [(6, 0, dt['mtype_ids'])]
                self.env['scat.menu.line'].create(dt)


class ScatMenuLine(models.Model):

    _inherit = "scat.menu.config.line"
    _name = "scat.menu.line"
    _order = "sequence asc"

    menu_id = fields.Many2one("scat.menu", u"Menú")

    @api.constrains('mode', 'mtype_ids')
    def _check_mode_mtype(self):
        for line in self:
            if line.menu_id:
                for mtype in line.mtype_ids:
                    res = self.search([('menu_id', '=',
                                        line.menu_id.id),
                                       ('id', '!=', line.id),
                                       ('mode', '=', line.mode),
                                       ('mtype_ids', 'in', [mtype.id])])
                    if res:
                        raise exceptions.\
                            ValidationError(u"No se puede repetir el tipo de "
                                            u"menú para el mismo momento")
