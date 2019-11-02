# -*- coding: utf-8 -*-
from odoo import api, fields, models
from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU, rrule, WEEKLY
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import calendar


class scat_student(models.Model):
    _name = "scat.student"
    _rec_name ='student_id'
    _order = "start_date desc,school_id"

    student_id = fields.Many2one('res.partner', string="Alumno", required=True)

    school_id = fields.Many2one('scat.school', string="Colegio", required=True)

    month = fields.Char(string="Mes", required=True)

    year = fields.Char(string="Año", required=True)
    start_date = fields.Date(readonly=True)

    @api.model
    def _get_default_day(self):
        return self.env.ref("scat_school_management.code_j").id


    dia1 = fields.Many2one("scat.student.state",string="Día 1", default=_get_default_day, required=True)
    dia1_code=fields.Char(related="dia1.code", readonly=True)

    dia2 = fields.Many2one("scat.student.state",string="Día 2", default=_get_default_day, required=True)
    dia2_code=fields.Char(related="dia2.code", readonly=True)

    dia3 = fields.Many2one("scat.student.state",string="Día 3", default=_get_default_day, required=True)
    dia3_code=fields.Char(related="dia3.code", readonly=True)

    dia4 = fields.Many2one("scat.student.state",string="Día 4", default=_get_default_day, required=True)
    dia4_code=fields.Char(related="dia4.code", readonly=True)

    dia5 = fields.Many2one("scat.student.state",string="Día 5", default=_get_default_day, required=True)
    dia5_code=fields.Char(related="dia5.code", readonly=True)

    dia6 = fields.Many2one("scat.student.state",string="Día 6", default=_get_default_day, required=True)
    dia6_code=fields.Char(related="dia6.code", readonly=True)

    dia7 = fields.Many2one("scat.student.state",string="Día 7", default=_get_default_day, required=True)
    dia7_code=fields.Char(related="dia7.code", readonly=True)

    dia8 = fields.Many2one("scat.student.state",string="Día 8", default=_get_default_day, required=True)
    dia8_code=fields.Char(related="dia8.code", readonly=True)

    dia9 = fields.Many2one("scat.student.state",string="Día 9", default=_get_default_day, required=True)
    dia9_code=fields.Char(related="dia9.code", readonly=True)

    dia10 = fields.Many2one("scat.student.state",string="Día 10", default=_get_default_day, required=True)
    dia10_code=fields.Char(related="dia10.code", readonly=True)

    dia11 = fields.Many2one("scat.student.state",string="Día 11", default=_get_default_day, required=True)
    dia11_code=fields.Char(related="dia11.code", readonly=True)

    dia12 = fields.Many2one("scat.student.state",string="Día 12", default=_get_default_day, required=True)
    dia12_code=fields.Char(related="dia12.code", readonly=True)

    dia13 = fields.Many2one("scat.student.state",string="Día 13", default=_get_default_day, required=True)
    dia13_code=fields.Char(related="dia13.code", readonly=True)

    dia14 = fields.Many2one("scat.student.state",string="Día 14", default=_get_default_day, required=True)
    dia14_code=fields.Char(related="dia14.code", readonly=True)

    dia15 = fields.Many2one("scat.student.state",string="Día 15", default=_get_default_day, required=True)
    dia15_code=fields.Char(related="dia15.code", readonly=True)

    dia16 = fields.Many2one("scat.student.state",string="Día 16", default=_get_default_day, required=True)
    dia16_code=fields.Char(related="dia16.code", readonly=True)

    dia17 = fields.Many2one("scat.student.state",string="Día 17", default=_get_default_day, required=True)
    dia17_code=fields.Char(related="dia17.code", readonly=True)

    dia18 = fields.Many2one("scat.student.state",string="Día 18", default=_get_default_day, required=True)
    dia18_code=fields.Char(related="dia18.code", readonly=True)

    dia19 = fields.Many2one("scat.student.state",string="Día 19", default=_get_default_day, required=True)
    dia19_code=fields.Char(related="dia19.code", readonly=True)

    dia20 = fields.Many2one("scat.student.state",string="Día 20", default=_get_default_day, required=True)
    dia20_code=fields.Char(related="dia20.code", readonly=True)

    dia21 = fields.Many2one("scat.student.state",string="Día 21", default=_get_default_day, required=True)
    dia21_code=fields.Char(related="dia21.code", readonly=True)

    dia22 = fields.Many2one("scat.student.state",string="Día 22", default=_get_default_day, required=True)
    dia22_code=fields.Char(related="dia22.code", readonly=True)

    dia23 = fields.Many2one("scat.student.state",string="Día 23", default=_get_default_day, required=True)
    dia23_code=fields.Char(related="dia23.code", readonly=True)

    dia24 = fields.Many2one("scat.student.state",string="Día 24", default=_get_default_day, required=True)
    dia24_code=fields.Char(related="dia24.code", readonly=True)

    dia25 = fields.Many2one("scat.student.state",string="Día 25", default=_get_default_day, required=True)
    dia25_code=fields.Char(related="dia25.code", readonly=True)

    dia26 = fields.Many2one("scat.student.state",string="Día 26", default=_get_default_day, required=True)
    dia26_code=fields.Char(related="dia26.code", readonly=True)

    dia27 = fields.Many2one("scat.student.state",string="Día 27", default=_get_default_day, required=True)
    dia27_code=fields.Char(related="dia27.code", readonly=True)

    dia28 = fields.Many2one("scat.student.state",string="Día 28", default=_get_default_day, required=True)
    dia28_code=fields.Char(related="dia28.code", readonly=True)

    dia29 = fields.Many2one("scat.student.state",string="Día 29", default=_get_default_day, required=True)
    dia29_code=fields.Char(related="dia29.code", readonly=True)

    dia30 = fields.Many2one("scat.student.state",string="Día 30", default=_get_default_day, required=True)
    dia30_code=fields.Char(related="dia30.code", readonly=True)

    dia31 = fields.Many2one("scat.student.state",string="Día 31", default=_get_default_day, required=True)
    dia31_code=fields.Char(related="dia31.code", readonly=True)

    total_ise=fields.Integer("Total ise", compute="_contador_asiste")
    total_child=fields.Integer("Total niño", compute="_contador_asiste")

    @api.depends('dia1','dia2','dia3','dia4','dia5','dia6','dia7','dia8','dia9','dia10','dia11','dia12','dia13','dia14','dia15',
                 'dia16','dia17','dia18','dia19','dia20','dia21','dia22','dia23','dia24','dia25','dia26','dia27','dia28','dia29','dia30','dia31')
    @api.multi
    def _contador_asiste(self):
        A=self.get_state_code("A")
        F=self.get_state_code("F")

        for registro in self:
            contadorA=0
            contadorF=0
            for dia in range(1,32):
                val=eval('registro.dia'+str(dia))

                if val.id == A:
                    contadorA +=1
                elif val.id == F:
                    contadorF +=1

            registro.total_ise=contadorA
            registro.total_child=contadorF+contadorA


    _sql_constraints = [
    ('calendar_unique',
     'UNIQUE(month, year, student_id)',
     "Ya hay un registro para ese alumno"),
    ]

    @api.model
    def get_next_month(self):

        today = datetime.now()
        today = today+relativedelta(months=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        first_day=datetime(today.year, today.month, 1)
        last_date = datetime(today.year, today.month, last_day)

        codes={ "A":self.get_state_code("A"),
                "F":self.get_state_code("F"),
                "J":self.get_state_code("J"),
                "S":self.get_state_code("S"),
                "D":self.get_state_code("D"),
                "H":self.get_state_code("H")}

        student_ticado=[]
        ticados=self.env['scat.student'].search([('month','=', str(today.month)),('year','=', str(today.year))])
        students=ticados.mapped('student_id')
        print ticados
        print students


        for school in self.env['scat.school'].search([]):


            dias_festivos=self.dias_festivos(first_day, last_date,school)

            for student_seleccionado in self.env['res.partner'].search([('active_school_id', '=', school.id), ('x_ise_estado', '=', 'usuario'), ('parent_id', '!=', False),
            '|','|','|','|','|','|', ('y_ise_factura_aut','=',True),('y_ise_l','=',True),('y_ise_m','=',True),('y_ise_x','=',True),
            ('y_ise_j','=',True),('y_ise_v','=',True),('y_ise_s','=',True),('id','not in',students.ids)]):
                vals={'student_id': student_seleccionado.id, 'school_id': school.id, 'month': str(today.month), 'year': str(today.year), 'start_date': first_day.strftime('%Y-%m-%d')}
                self.control_presencia(student_seleccionado, school, first_day, last_day, today, last_date, dias_festivos, vals, codes)

    def control_presencia(self, student_seleccionado, school, first_day, last_day, today, last_date, dias_festivos, vals, codes):
        if student_seleccionado.y_ise_s:
            self.create(vals)

        else:
            if student_seleccionado.y_ise_factura_aut:
                dias = [MO, TU, WE, TH, FR]
            else:
                dias = []
                if student_seleccionado.y_ise_l:
                    dias += [MO]
                if student_seleccionado.y_ise_m:
                    dias += [TU]
                if student_seleccionado.y_ise_x:
                    dias += [WE]
                if student_seleccionado.y_ise_j:
                    dias += [TH]
                if student_seleccionado.y_ise_v:
                    dias += [FR]

            date_list = list(rrule(WEEKLY, dtstart=first_day, until=last_date, byweekday=dias))
            lista_sabados = list(rrule(WEEKLY, dtstart=first_day, until=last_date, byweekday=SA))
            lista_domingos = list(rrule(WEEKLY, dtstart=first_day, until=last_date, byweekday=SU))
            days=set(date_list)-dias_festivos
            new_vals = dict(vals)

            for day in dias_festivos:
                new_vals['dia'+str(day.day)]=codes["H"]

            for day in lista_sabados:
                new_vals['dia'+str(day.day)]=codes["S"]

            for day in lista_domingos:
                new_vals['dia'+str(day.day)]=codes["D"]

            for day in days:
                new_vals['dia'+str(day.day)]=codes["A"]

            self.create(new_vals)

            #Funcion para cabecera de factura

            #crear_cabecera_factura(student_seleccionado)

            #Funcion para lineas de factura

            #crear_lineas_factura(student_seleccionado, total_ise, total_child)


    #def crear_cabecera_factura(self, student_seleccionado):

        #self.ensure_one()
        #res = {}
        #res = {
            #'name': self.name,
            #'sequence': self.sequence,
            #'origin': self.order_id.name,
            #'account_id': account.id,
            #'price_unit': self.price_unit,
            #'quantity': qty,
            #'discount': self.discount,
            #'uom_id': self.product_uom.id,
            #'product_id': self.product_id.id or False,
            #'layout_category_id': self.layout_category_id and self.layout_category_id.id or False,
            #'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
            #'account_analytic_id': self.order_id.project_id.id,
            #'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
        #}
        #return res


    #def crear_lineas_factura(self, student_seleccionado, total_ise, total_child):
        #self.ensure_one()
        #res = {}






    def get_state_code(self, code):

        return self.env.ref("scat_school_management.code_"+code.lower()).id


    def dias_festivos(self, first_day, last_date, school):

        domain=[('school_ids', 'in', [school.id]),('end_date', '>=', first_day.strftime('%Y-%m-%d')),('start_date','<=',last_date.strftime('%Y-%m-%d'))]


        lista_festivos=set()

        for festivo in self.env['scat.holidays'].search(domain):
            if festivo.end_date>last_date.strftime('%Y-%m-%d'):
                end_date=last_date
            else:
                end_date=datetime.strptime(festivo.end_date,'%Y-%m-%d')

            if festivo.start_date<first_day.strftime('%Y-%m-%d'):
                start_date=first_day
            else:
                start_date=datetime.strptime(festivo.start_date,'%Y-%m-%d')


            lista_fechas = [start_date + timedelta(days=d) for d in range((end_date - start_date).days + 1)]

            lista_festivos |= set(lista_fechas)



        return lista_festivos


