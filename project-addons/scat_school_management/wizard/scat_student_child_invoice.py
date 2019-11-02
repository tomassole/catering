# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta
import time
import logging

_logger = logging.getLogger(__name__)


class ScatStudentChildInvoiceWzd(models.TransientModel):

    _name = "scat.student.child.invoiced.wzd"

    year = fields.Integer("Año", required=True,
                          default=lambda *a: int(time.strftime("%Y")))
    month = fields.Selection([('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'),
                              ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
                              ('7', 'Julio'), ('8', 'Agosto'),
                              ('9', 'Septiembre'), ('10', 'Octubre'),
                              ('11', 'Noviembre'), ('12', 'Diciembre')], 'Mes',
                             required=True,
                             default=lambda *a: str(int(time.strftime("%m"))))

    @api.multi
    def action_invoice(self):
        obj = self[0]
        presencias = self.env['scat.student'].\
            search([('month', '=', obj.month), ('year', '=', str(obj.year)),
                    ('invoice_id', '=', False)], order="expedient_id")
        if not presencias:
            raise UserError("No se han encontrado controles de "
                            "presencia pendientes de facturar")
        curr_expedient = False
        # Verificación previa de que los diarios están establecidos
        for control in presencias:
            if control.expedient_id != curr_expedient:
                curr_expedient = control.expedient_id
                if not curr_expedient.journal_kids_id:
                    raise UserError(
                        "El diario no está establecido en el exp: %s" %
                        curr_expedient.display_name)

        # modificamos cron para lanzar proceso
        try:
            cron = self.env.ref('scat_school_management.ir_cron_invoice_wizard')
        except ValueError:
            raise UserError("No se ha encontrado la tarea cron!!!!")
        cron_args = '(' + obj.month + ', ' + str(obj.year) + ')'
        next_call = (datetime.now() + timedelta(seconds=60)).strftime(
            DEFAULT_SERVER_DATETIME_FORMAT)
        cron_data = {
            'active': True,
            'numbercall': 1,
            'args': cron_args,
            'nextcall': next_call,
        }
        cron.sudo().write(cron_data)
