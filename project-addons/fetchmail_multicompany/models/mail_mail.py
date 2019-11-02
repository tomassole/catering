# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class MailMail(models.Model):

    _inherit = "mail.mail"

    @api.model
    def create(self, vals):
        if vals.get('mail_server_id'):
            vals['email_from'] = self.env['ir.mail_server'].\
                browse(vals['mail_server_id']).smtp_user
        elif vals.get('mail_message_id'):
            mail = self.env['mail.message'].browse(vals['mail_message_id'])
            if mail.res_id and mail.model:
                obj = self.sudo().env[mail.model].browse(mail.res_id)
                if 'company_id' in dir(obj) and obj.company_id:
                    smtps = self.sudo().env['ir.mail_server'].\
                        search([('company_id', '=', obj.company_id.id)])
                    if smtps:
                        vals['email_from'] = smtps[0].smtp_user
        else:
            smtps = self.sudo().env['ir.mail_server'].\
                search([('company_id', '=', self.env.user.company_id.id)])
            if smtps:
                vals['email_from'] = smtps[0].smtp_user
        return super(MailMail, self).create(vals)
