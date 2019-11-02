# -*- coding: utf-8 -*-

from odoo import models, api, exceptions, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ScatMenu(models.Model):

    _inherit = "scat.menu"

    picking_ids = fields.One2many("stock.picking", "menu_id", readonly=True)

    @api.multi
    def action_view_delivery(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            action['views'] = [(self.env.ref('stock.view_picking_form').id,
                                'form')]
            action['res_id'] = pickings.id
        return action

    @api.multi
    def create_pickings(self):
        new_procs = self.env['procurement.order']
        for menu in self:
            schools = self.env['scat.school'].\
                search([('rotative_menu_ids', 'in',
                         [menu.rotative_line_id.rotative_id.id])])
            dt = datetime.strptime(menu.date, "%Y-%m-%d")
            for school in schools:
                active_expedients = school.expedient_ids.\
                    filtered(lambda r: r.state == 'open' and r.start_date <=
                             menu.date and (not r.end_date or r.end_date >=
                                            menu.date))
                if active_expedients:
                    exp = active_expedients[0]
                else:
                    continue
                products = {}
                presencias = self.env['scat.student'].\
                    search([('school_id', '=', school.id),
                            ('month', '=', str(dt.month)),
                            ('year', '=', str(dt.year)),
                            ('dia' + str(dt.day) + "_code", '=', "A")])
                partner = self.env['res.partner'].\
                    with_context(force_company=exp.company_id.id).\
                    browse(school.partner_id.id)
                group = self.env["procurement.group"].\
                    create({'name': u"Menú " + menu.date + u": " +
                            school.name,
                            'partner_id': partner.id})
                for presencia in presencias:
                    visited_moments = []
                    for line in menu.menu_line_ids:
                        include_line = False
                        if line.mode not in visited_moments:
                            conflict_allergens = line.\
                                mapped('mtype_ids.conflict_allergens_ids')
                            if presencia.student_id.allergens_ids:
                                if set(presencia.student_id.
                                       allergens_ids).\
                                        issubset(set(conflict_allergens)):
                                    include_line = True
                            else:
                                include_line = True
                        if include_line:
                            visited_moments.append(line.mode)
                            if not line.product_id:
                                raise exceptions.\
                                    Warning(u"La linea %s del menú no "
                                            u"puede procesarse porque no "
                                            u"tiene producto." % line.name)
                            if presencia.student_id.course_id:
                                qty = line.product_qty * \
                                    presencia.student_id.course_id.\
                                    ration_percentage
                            else:
                                qty = line.product_qty
                            if products.get(line.product_id.id):
                                products[line.product_id.id] += qty
                            else:
                                products[line.product_id.id] = qty

                for product_id in products:
                    prod = self.env["product.product"].\
                        browse(product_id)
                    proc_vals = {'name': prod.name,
                                 'origin': menu.name,
                                 'date_planned': menu.date,
                                 'product_id': prod.id,
                                 'product_qty': products[product_id],
                                 'product_uom': prod.uom_id.id,
                                 'company_id': exp.company_id.id,
                                 'menu_id': menu.id,
                                 'group_id': group.id,
                                 'location_id':
                                 partner.property_stock_customer.id,
                                 'warehouse_id': school.warehouse_id.id,
                                 'partner_dest_id': partner.id}
                    new_proc = self.env["procurement.order"].\
                        with_context(procurement_autorun_defer=True).\
                        create(proc_vals)
                    new_procs |= new_proc
        new_procs.run()

    @api.model
    def action_create_pickings_run(self, weeks=4, start_date=False):
        if not start_date:
            today = datetime.now()
        else:
            today = datetime.strptime(start_date, '%Y-%m-%d')
        next_month = today + relativedelta(weeks=weeks)
        menus = self.search([('state', '=', 'confirmed'),
                             ('date', '<=',
                              next_month.strftime("%Y-%m-%d")),
                             ('picking_ids', '=', False),
                             ('date', '>=',
                              today.strftime("%Y-%m-%d"))])
        menus.create_pickings()
