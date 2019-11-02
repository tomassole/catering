# -*- coding: utf-8 -*-

from odoo import models, api, exceptions


class ScatStudentIseInvoiceWzd(models.TransientModel):

    _name = "scat.student.ise.invoiced.wzd"
    _inherit = "scat.student.child.invoiced.wzd"

    @api.multi
    def action_invoice(self):
        obj = self[0]
        presencias = self.env['scat.student'].\
            search([('month', '=', obj.month), ('year', '=', str(obj.year)),
                    ('invoice_id', '!=', False),
                    ('invoice_ise_id', '=', False)],
                   order="expedient_id,school_id")
        if not presencias or len(presencias) == 1:
            raise exceptions.Warning("No se han encontrado controles de "
                                     "presencia pendientes de facturar")
        curr_expedient = False
        ise_lines = {}
        expedient_lines = []
        invoice = False
        ult_presencia = presencias[-1]
        presencias_facturadas = self.env['scat.student']
        for control in presencias:
            check = control == ult_presencia
            if control.expedient_id != curr_expedient or check:
                if check:
                    presencias_facturadas |= control
                expedient_lines = control.expedient_id.get_invoice_lines()
                for school in ise_lines:
                    school_id = self.env['scat.school'].browse(int(school))
                    school_amount = 0.0
                    for product in ise_lines[school]:
                        product = self.env['product.product'].\
                            with_context(force_company=
                                         curr_expedient.company_id.id).\
                            browse(int(product))
                        if product.property_account_income_id:
                            account = product.property_account_income_id.id
                        elif product.categ_id.property_account_income_categ_id:
                            account = product.categ_id.\
                                property_account_income_categ_id.id
                        else:
                            raise exceptions.\
                                UserError("No se ha encontrado una cuenta de "
                                          "ingreso para el producto %s" %
                                          product.name)
                        self.env['account.invoice.line'].\
                            create({'product_id': product.id,
                                    'price_unit':
                                    ise_lines[school][product.id][0],
                                    'name': product.name,
                                    'invoice_line_tax_ids':
                                    [(6, 0,
                                      product.taxes_id.
                                      filtered(lambda x: x.company_id ==
                                               curr_expedient.company_id).
                                      ids)],
                                    'account_id': account,
                                    'uom_id': product.uom_id.id,
                                    'quantity': 1,
                                    'invoice_id': invoice.id,
                                    'account_analytic_id':
                                    school_id.school_id.
                                    analytic_account_id.id})
                        school_amount += ise_lines[school][product.id][1]
                    if curr_expedient.canon_product_id and \
                            curr_expedient.canon_percent:
                        product = self.env['product.product'].\
                            with_context(force_company=
                                         curr_expedient.company_id.id).\
                            browse(curr_expedient.canon_product_id.id)
                        if product.property_account_expense_id:
                            account = product.property_account_expense_id.id
                        elif product.categ_id.\
                                property_account_expense_categ_id:
                            account = product.categ_id.\
                                property_account_expense_categ_id.id
                        else:
                            raise exceptions.\
                                UserError("No se ha encontrado una cuenta de "
                                          "gasto para el producto %s" %
                                          product.name)
                        self.env['account.invoice.line'].\
                            create({'product_id': product.id,
                                    'price_unit':
                                    -(school_amount *
                                      (curr_expedient.canon_percent / 100.0)),
                                    'name': product.name,
                                    'account_id': account,
                                    'uom_id': product.uom_id.id,
                                    'quantity': 1,
                                    'invoice_id': invoice.id,
                                    'account_analytic_id':
                                    school_id.school_id.
                                    analytic_account_id.id})
                if invoice:
                    invoice.compute_taxes()
                    presencias_facturadas.write({'invoice_ise_id': invoice.id})
                    presencias_facturadas = self.env['scat.student']

                if not check:
                    ise_lines = {}
                    curr_expedient = control.expedient_id
                    if not curr_expedient.journal_ise_id:
                        raise exceptions.\
                            Warning("El diario no está establecido en el "
                                    "exp: %s" %
                                    (curr_expedient.display_name))
                    partner = self.env['res.partner'].\
                        with_context(force_company=
                                     control.expedient_id.company_id.id).\
                        browse(control.expedient_id.partner_id.id)
                    invoice = self.env['scat.student'].\
                        crear_cabecera_factura(partner,
                                               journal=control.
                                               expedient_id.journal_ise_id,
                                               expedient=control.expedient_id,
                                               t='x')

            presencias_facturadas |= control
            if not ise_lines.get(control.school_id.id):
                ise_lines[control.school_id.id] = {}

            child = self.env['res.partner'].\
                with_context(force_company=
                             control.expedient_id.company_id.id).\
                browse(control.student_id.commercial_partner_id.id)
            for line in expedient_lines:
                discount = child.property_product_pricelist.item_ids[0].\
                    percent_price
                ise_price = control.total_ise * line['price_unit'] * \
                    (discount / 100.0)
                canon_price = control.total_ise * line['price_unit']
                if ise_lines[control.school_id.id].get(line['product_id']):
                    ise_lines[control.school_id.id][line['product_id']][0] += \
                        ise_price
                    ise_lines[control.school_id.id][line['product_id']][1] += \
                        canon_price
                else:
                    ise_lines[control.school_id.id][line['product_id']] = \
                        [ise_price, canon_price]
