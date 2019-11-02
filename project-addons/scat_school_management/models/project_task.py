# -*- coding: utf-8 -*-
from odoo import models, api


class ProjectTask(models.Model):

    _inherit = 'project.task'

    @api.multi
    def action_view_ticado(self):
        self.ensure_one()
        commercial_partner_id = self.partner_id.commercial_partner_id.id
        if commercial_partner_id:

            domain = [('student_id', 'child_of', [commercial_partner_id])]

            return {
                'name': 'Control de presencia',
                'domain': domain,
                'res_model': 'scat.student',
                'type': 'ir.actions.act_window',
                'view_id': False,
                'view_mode': 'tree,form',
                'view_type': 'form'
            }
