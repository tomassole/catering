# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError


class scat_expediente(models.Model):

    _name = "scat.expediente"
    _rec_name = "display_name"

    n_expediente = fields.Char("Nº de expediente", required=True,
                               readonly=True,
                               states={'borrador': [('readonly', False)]})
    n_lote = fields.Char("Nº de lote", required=True, readonly=True,
                         states={'borrador': [('readonly', False)]})
    display_name = fields.Char("Referencia", compute="_get_display_name")
    partner_id = fields.Many2one('res.partner', 'Cliente', required=True,
                                 readonly=True,
                                 states={'borrador': [('readonly', False)]})
    start_date = fields.Date("Fecha inicio", required=True, readonly=True,
                             states={'borrador': [('readonly', False)]},
                             default=fields.Date.today, copy=False)
    end_date = fields.Date("Fecha de fin", readonly=True, copy=False,
                           states={'borrador': [('readonly', False)]})
    school_ids = fields.Many2many('scat.school',
                                  relation='scat_expediente_scat_school_rel',
                                  column2='scat_school_id',
                                  column1='scat_expediente_id',
                                  string="Colegio/s", readonly=True,
                                  states={'borrador': [('readonly', False)]})
    state = fields.Selection([("borrador", "Borrador"), ("open", "Abierto"),
                              ("close", "Cerrado")], "Estado",
                             default="borrador", readonly=True)
    company_id = fields.Many2one('res.company', 'Compañía', required=True,
                                 default=lambda s: s.env.user.company_id.id,
                                 readonly=True,
                                 states={'borrador': [('readonly', False)]})

    journal_kids_id = fields.Many2one("account.journal", "Diario Niños",
                                      domain=[("type", "=", "sale")],
                                      required=True)
    journal_ise_id = fields.Many2one("account.journal", "Diario Ise",
                                     domain=[("type", "=", "sale")],
                                     required=True)

    product_ids = fields.One2many('scat.expediente.product', 'expediente_id',
                                  "Productos", copy=True)
    canon_product_id = fields.Many2one('product.product', "Canon")
    canon_percent = fields.Float("% Canon", digits=(5, 2),
                                 help="Sobre 100")

    _sql_constraints = [('expedient_unique',
                         'UNIQUE(n_expediente, n_lote, start_date)',
                         u"El expediente debe ser único")]

    @api.multi
    def _get_display_name(self):
        for expedient in self:
            expedient.display_name = expedient.n_expediente + u"/" + \
                expedient.n_lote

    @api.multi
    def get_invoice_lines(self):
        self.ensure_one()
        res = []
        for line in self.product_ids:
            product = self.env['product.product'].\
                with_context(force_company=self.company_id.id).\
                browse(line.product_id.id)
            if product.property_account_income_id:
                account = product.property_account_income_id.id
            elif product.categ_id.property_account_income_categ_id:
                account = product.categ_id.property_account_income_categ_id.id
            else:
                raise UserError("No se ha encontrado una cuenta de ingreso "
                                "para el producto %s" % product.name)
            res.append({'product_id': product.id,
                        'price_unit': line.price_u,
                        'name': product.name,
                        'invoice_line_tax_ids': [(6, 0,
                                                  line.impuestos_ids.ids)],
                        'account_id': account,
                        'analytic_tag_ids': [(6, 0,
                                              line.analytic_tag_ids.ids)],
                        'uom_id': product.uom_id.id})
        return res

    @api.multi
    def abrir_expediente(self):
        for exp in self:
            new_state = "open"
            exp.state = new_state
            for school in exp.school_ids:
                expedientes = self.search([('id', '!=', exp.id),
                                           ('school_ids', 'in', [school.id]),
                                           ('state', '=', 'open')])
                if expedientes:
                    raise UserError("No se ha podido abrir el expediente "
                                    "porque el colegio %s se escuentra en "
                                    "otro expediente abierto %s" %
                                    (school.name, expedientes[0].display_name))
